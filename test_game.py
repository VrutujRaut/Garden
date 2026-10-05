"""Fast, non-visual checks for Signal Bloom's important game rules."""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

import game as game_module
from game import ARENA, Drone, Orb, Player, SignalBloomGame, load_high_score, save_high_score


class GameLogicTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pygame.init()

    @classmethod
    def tearDownClass(cls) -> None:
        pygame.quit()

    def setUp(self) -> None:
        self.game = SignalBloomGame()
        self.game.start_game()

    def tearDown(self) -> None:
        del self.game

    def test_player_stays_inside_arena(self) -> None:
        player = Player()

        class RightDownKeys:
            def __getitem__(self, key: int) -> bool:
                return key in (pygame.K_d, pygame.K_s, pygame.K_RIGHT, pygame.K_DOWN)

        player.x = 900
        player.y = 600
        player.move(RightDownKeys(), 2.0)
        self.assertLessEqual(player.x, ARENA.right - player.radius)
        self.assertLessEqual(player.y, ARENA.bottom - player.radius)

    def test_orb_collection_increases_score_and_pulse_charge(self) -> None:
        self.game.drones.clear()
        self.game.orbs = [Orb(self.game.player.x, self.game.player.y)]
        self.game.update(0.01)
        self.assertEqual(self.game.orbs_collected, 1)
        self.assertEqual(self.game.player.charge, 1)
        self.assertGreaterEqual(self.game.score, 100)

    def test_pulse_spends_charge_and_stuns_nearby_drone(self) -> None:
        self.game.player.charge = 3
        drone = Drone(self.game.player.x + 50, self.game.player.y, 100)
        self.game.drones = [drone]
        self.game.use_pulse()
        self.assertEqual(self.game.player.charge, 0)
        self.assertGreater(drone.stunned, 0)

    def test_contact_costs_one_life_and_grants_brief_immunity(self) -> None:
        drone = Drone(self.game.player.x + 30, self.game.player.y, 100)
        self.game.hit_player(drone)
        self.assertEqual(self.game.player.lives, 2)
        self.assertGreater(self.game.player.invulnerable, 0)
        self.game.hit_player(drone)
        self.assertEqual(self.game.player.lives, 2)

    def test_pause_and_resume(self) -> None:
        self.game.handle_key(pygame.K_p)
        self.assertEqual(self.game.state, "paused")
        self.game.handle_key(pygame.K_ESCAPE)
        self.assertEqual(self.game.state, "playing")

    def test_difficulty_stage_increases_drone_speed(self) -> None:
        self.game.drones = [Drone(ARENA_LEFT, ARENA_TOP, 0)]
        self.game.orbs.clear()
        self.game.update(0.01)
        early_speed = self.game.drones[0].speed
        self.game.elapsed = 22
        self.game.update(0.01)
        self.assertGreater(self.game.drones[0].speed, early_speed)

    def test_last_life_ends_run_and_enter_restarts(self) -> None:
        self.game.player.lives = 1
        self.game.hit_player(Drone(self.game.player.x + 30, self.game.player.y, 100))
        self.assertEqual(self.game.state, "game_over")
        self.game.handle_key(pygame.K_RETURN)
        self.assertEqual(self.game.state, "playing")
        self.assertEqual(self.game.player.lives, 3)
        self.assertEqual(self.game.orbs_collected, 0)

    def test_reaching_beacon_after_goal_wins(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "highscore.json"
            with patch.object(game_module, "SAVE_PATH", path):
                self.game.drones.clear()
                self.game.orbs.clear()
                self.game.orbs_collected = 12
                self.game.player.x, self.game.player.y = ARENA_CENTER
                self.game.update(0.01)
        self.assertEqual(self.game.state, "victory")

    def test_missing_and_corrupt_high_score_and_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "highscore.json"
            self.assertEqual(load_high_score(path), 0)
            path.write_text("not valid json", encoding="utf-8")
            self.assertEqual(load_high_score(path), 0)
            save_high_score(345, path)
            self.assertEqual(load_high_score(path), 345)

    def test_finishing_with_a_record_saves_it(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "highscore.json"
            with patch.object(game_module, "SAVE_PATH", path):
                self.game.high_score = 0
                self.game.score = 420
                self.game.finish("victory")
            self.assertEqual(load_high_score(path), 420)
            self.assertTrue(self.game.new_record)

    def test_all_screens_draw_without_display_errors(self) -> None:
        for state in ("menu", "help", "playing", "paused", "game_over", "victory"):
            self.game.state = state
            self.game.draw()

    def test_window_close_event_exits_game_loop(self) -> None:
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        self.game.run()
        self.assertFalse(pygame.display.get_init())
        pygame.display.init()
        pygame.display.set_mode((960, 640))


# Keep test coordinates tied to the same playfield constants as the game.
ARENA_LEFT = ARENA.left + 40
ARENA_TOP = ARENA.top + 40
ARENA_CENTER = (ARENA.centerx, ARENA.centery)


if __name__ == "__main__":
    unittest.main()
