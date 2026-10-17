"""Small non-visual checks for Redstone Run's game rules."""

import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

import game
from game import BENCH, COLS, GOAL, PORTAL, ROWS, WALL, Explorer, RedstoneRun, Slime, load_best, save_best


class RedstoneRunTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.run = RedstoneRun()
        self.run.state = "playing"

    def test_world_is_a_rectangular_list_of_lists(self):
        self.assertEqual(len(self.run.world), ROWS)
        self.assertTrue(all(len(row) == COLS for row in self.run.world))
        self.assertEqual(self.run.world[13][2], BENCH)
        self.assertEqual(self.run.world[13][23], PORTAL)

    def test_wall_blocks_player(self):
        self.run.player = Explorer(2, 2)
        self.run.world[2][3] = WALL
        self.run.move_player(1, 0)
        self.assertEqual(self.run.player.tile, (2, 2))

    def test_ore_is_solid_until_mined(self):
        self.run.player = Explorer(6, 3)
        self.run.world[3][7] = "r"
        self.run.move_player(1, 0)
        self.assertEqual(self.run.player.tile, (6, 3))
        self.run.mine()
        self.assertEqual(self.run.world[3][7], ".")

    def test_mining_updates_inventory_world_and_score(self):
        self.run.player = Explorer(6, 3)
        self.run.world[3][7] = "r"
        self.run.mine()
        self.assertEqual(self.run.inventory["redstone"], 1)
        self.assertEqual(self.run.world[3][7], ".")
        self.assertEqual(self.run.score, 50)

    def test_crafting_requires_workbench_and_recipe_items(self):
        self.run.player = Explorer(2, 12)
        self.run.inventory.update(redstone=4, iron=2)
        self.run.craft()
        self.assertEqual(self.run.inventory["beacon_core"], 1)
        self.assertEqual(self.run.inventory["redstone"], 0)
        self.assertEqual(self.run.inventory["iron"], 0)

    def test_crafting_without_recipe_does_not_consume_items(self):
        self.run.player = Explorer(2, 12)
        self.run.inventory.update(redstone=3, iron=2)
        self.run.craft()
        self.assertEqual(self.run.inventory["redstone"], 3)
        self.assertEqual(self.run.inventory["beacon_core"], 0)

    def test_portal_requires_core_then_wins(self):
        self.run.player = Explorer(22, 13)
        self.run.move_player(1, 0)
        self.assertEqual(self.run.state, "playing")
        self.run.inventory["beacon_core"] = 1
        self.run.player = Explorer(22, 13)
        self.run.move_cooldown = 0
        self.run.move_player(1, 0)
        self.assertEqual(self.run.state, "victory")

    def test_slime_contact_costs_health_once_during_immunity(self):
        self.run.slimes = [Slime(2, 2)]
        self.run.update_slimes(0.01)
        self.assertEqual(self.run.player.health, 2)
        self.run.update_slimes(0.01)
        self.assertEqual(self.run.player.health, 2)

    def test_pause_restart_and_quit_keys(self):
        self.run.handle_key(pygame.K_ESCAPE)
        self.assertEqual(self.run.state, "paused")
        self.run.handle_key(pygame.K_RETURN)
        self.assertEqual(self.run.state, "playing")
        self.run.finish("game_over")
        self.run.handle_key(pygame.K_RETURN)
        self.assertEqual(self.run.state, "playing")
        self.assertFalse(self.run.handle_key(pygame.K_q))

    def test_best_score_handles_bad_data_and_round_trips(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "best.json"
            self.assertEqual(load_best(path), 0)
            path.write_text("broken", encoding="utf-8")
            self.assertEqual(load_best(path), 0)
            save_best(780, path)
            self.assertEqual(load_best(path), 780)

    def test_every_screen_draws(self):
        for state in ("menu", "help", "playing", "paused", "game_over", "victory"):
            self.run.state = state
            self.run.draw()

    def test_window_close_event_exits_normally(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        self.run.run()
        self.assertFalse(pygame.display.get_init())
        pygame.init()
        pygame.display.set_mode((960, 720))

    def test_world_has_enough_mineable_recipe_ore(self):
        redstone = sum(tile == "r" for row in self.run.world for tile in row)
        iron = sum(tile == "i" for row in self.run.world for tile in row)
        self.assertGreaterEqual(redstone, GOAL["redstone"])
        self.assertGreaterEqual(iron, GOAL["iron"])


if __name__ == "__main__":
    unittest.main()
