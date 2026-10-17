"""Redstone Run: an original block-world adventure and Class XI IP project."""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

import pygame


WIDTH, HEIGHT = 960, 720
TILE = 32
COLS, ROWS = 26, 16
WORLD_X, WORLD_Y = (WIDTH - COLS * TILE) // 2, 118
FPS = 60
SAVE_PATH = Path(__file__).with_name("redstone_best.json")
GOAL = {"redstone": 4, "iron": 2}
RECIPE = {"redstone": 4, "iron": 2}

INK = (17, 21, 28)
PANEL = (34, 40, 49)
WHITE = (242, 244, 238)
MUTED = (172, 181, 182)
MINT = (91, 220, 151)
GOLD = (255, 205, 97)
RED = (226, 84, 79)
BLUE = (93, 173, 232)

FLOOR = "."
WALL = "#"
BENCH = "B"
PORTAL = "P"
ORE = {"r": "redstone", "i": "iron", "c": "coal"}
ORE_COLORS = {"redstone": (227, 62, 67), "iron": (195, 176, 146), "coal": (83, 91, 99)}


def load_best(path: Path = SAVE_PATH) -> int:
    """Read the best score, treating missing or invalid save data as zero."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return max(0, int(data.get("best", 0)))
    except (OSError, ValueError, TypeError, AttributeError, json.JSONDecodeError):
        return 0


def save_best(score: int, path: Path = SAVE_PATH) -> None:
    try:
        path.write_text(json.dumps({"best": int(score)}, indent=2), encoding="utf-8")
    except OSError:
        pass


def make_world() -> list[list[str]]:
    """Build a small tile map (a list of rows, each row a list of tile codes)."""
    world = [[WALL if x in (0, COLS - 1) or y in (0, ROWS - 1) else FLOOR
              for x in range(COLS)] for y in range(ROWS)]
    # Broken rocky shelves make short, readable routes through the cave.
    for x in range(5, 15):
        if x not in (9, 10):
            world[4][x] = WALL
    for x in range(12, 22):
        if x not in (16, 17):
            world[8][x] = WALL
    for x in range(3, 11):
        if x not in (6, 7):
            world[11][x] = WALL
    for y in range(5, 8):
        world[y][19] = WALL
    for y in range(9, 12):
        if y != 10:
            world[y][5] = WALL

    world[13][2] = BENCH
    world[13][23] = PORTAL
    ore_spots = {
        "r": ((7, 3), (17, 5), (10, 9), (21, 12), (13, 13), (3, 8)),
        "i": ((17, 2), (4, 13), (22, 6)),
        "c": ((3, 5), (15, 6), (22, 10), (8, 13)),
    }
    for tile_code, points in ore_spots.items():
        for x, y in points:
            world[y][x] = tile_code
    return world


def tile_center(tile_pos: tuple[int, int]) -> tuple[float, float]:
    return tile_pos[0] + 0.5, tile_pos[1] + 0.5


class Explorer:
    """Player data: position and health are simple, explainable attributes."""

    def __init__(self, x: int = 2, y: int = 2) -> None:
        self.x, self.y = x, y
        self.health = 3
        self.invulnerable = 0.0

    @property
    def tile(self) -> tuple[int, int]:
        return self.x, self.y


class Slime:
    """A small cave creature that takes one simple step toward the explorer."""

    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y
        self.move_timer = random.uniform(0.0, 0.5)

    @property
    def tile(self) -> tuple[int, int]:
        return self.x, self.y


class RedstoneRun:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Redstone Run | Class XI IP")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 29)
        self.small = pygame.font.Font(None, 22)
        self.title_font = pygame.font.Font(None, 72)
        self.best = load_best()
        self.state = "menu"
        self.message = "Mine ore, craft a beacon core, and find the portal."
        self.message_timer = 0.0
        self.reset_run()

    def reset_run(self) -> None:
        self.world = make_world()
        self.player = Explorer()
        self.slimes = [Slime(22, 2), Slime(14, 13)]
        self.inventory = {"redstone": 0, "iron": 0, "coal": 0, "beacon_core": 0}
        self.score = 0
        self.elapsed = 0.0
        self.move_cooldown = 0.0
        self.mine_cooldown = 0.0
        self.enemy_clock = 0.0
        self.message = "Mine redstone and iron. A workbench is near the lower-left."
        self.message_timer = 4.0

    def inside(self, x: int, y: int) -> bool:
        return 0 <= x < COLS and 0 <= y < ROWS

    def walkable(self, x: int, y: int) -> bool:
        return self.inside(x, y) and self.world[y][x] != WALL and self.world[y][x] not in ORE

    def announce(self, message: str) -> None:
        self.message = message
        self.message_timer = 2.5

    def nearby(self, tile_code: str) -> bool:
        return any(self.inside(self.player.x + dx, self.player.y + dy)
                   and self.world[self.player.y + dy][self.player.x + dx] == tile_code
                   for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)))

    def move_player(self, dx: int, dy: int) -> None:
        if self.state != "playing" or self.move_cooldown > 0:
            return
        nx, ny = self.player.x + dx, self.player.y + dy
        if self.walkable(nx, ny):
            self.player.x, self.player.y = nx, ny
            self.move_cooldown = 0.115
            if self.world[ny][nx] == PORTAL:
                self.check_portal()

    def mine(self) -> None:
        if self.state != "playing" or self.mine_cooldown > 0:
            return
        self.mine_cooldown = 0.20
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            x, y = self.player.x + dx, self.player.y + dy
            if not self.inside(x, y) or self.world[y][x] not in ORE:
                continue
            material = ORE[self.world[y][x]]
            self.world[y][x] = FLOOR
            self.inventory[material] += 1
            self.score += 25 if material == "coal" else 50
            self.announce(f"Mined {material}! {self.inventory[material]} in your inventory.")
            return
        self.announce("No ore beside you. Move next to a colored block and press F.")

    def craft(self) -> None:
        if self.state != "playing":
            return
        if not self.nearby(BENCH):
            self.announce("Find the workbench (brown blocks) and stand beside it.")
            return
        if self.inventory["beacon_core"]:
            self.announce("Beacon core crafted. Reach the purple portal!")
            return
        if all(self.inventory[item] >= count for item, count in RECIPE.items()):
            for item, count in RECIPE.items():
                self.inventory[item] -= count
            self.inventory["beacon_core"] = 1
            self.score += 150
            self.announce("Beacon core crafted! Reach the purple portal.")
        else:
            self.announce("Recipe: 4 redstone + 2 iron. Mine the bright ore veins.")

    def check_portal(self) -> None:
        if self.inventory["beacon_core"]:
            self.score += max(0, 300 - int(self.elapsed))
            self.finish("victory")
        else:
            self.announce("The portal is dark. Craft a beacon core at the workbench first.")

    def damage_player(self) -> None:
        if self.player.invulnerable > 0:
            return
        self.player.health -= 1
        self.player.invulnerable = 1.1
        self.announce("A cave slime bumped you! Keep moving.")
        if self.player.health <= 0:
            self.finish("game_over")

    def update_slimes(self, dt: float) -> None:
        for slime in self.slimes:
            slime.move_timer -= dt
            if slime.move_timer > 0:
                continue
            slime.move_timer = max(0.22, 0.72 - self.elapsed / 150)
            choices = [(self.player.x - slime.x, self.player.y - slime.y)]
            if abs(choices[0][0]) and abs(choices[0][1]):
                choices = [(choices[0][0], 0), (0, choices[0][1])]
                random.shuffle(choices)
            if choices[0] == (0, 0):
                continue
            for dx, dy in choices:
                sx = 0 if dx == 0 else (1 if dx > 0 else -1)
                sy = 0 if dy == 0 else (1 if dy > 0 else -1)
                if self.walkable(slime.x + sx, slime.y + sy):
                    slime.x += sx
                    slime.y += sy
                    break
        if self.player.invulnerable <= 0 and any(slime.tile == self.player.tile for slime in self.slimes):
            self.damage_player()

    def update(self, dt: float) -> None:
        if self.state != "playing":
            return
        self.elapsed += dt
        self.move_cooldown = max(0.0, self.move_cooldown - dt)
        self.mine_cooldown = max(0.0, self.mine_cooldown - dt)
        self.player.invulnerable = max(0.0, self.player.invulnerable - dt)
        self.message_timer = max(0.0, self.message_timer - dt)
        self.enemy_clock += dt
        if self.enemy_clock >= 0.2:
            self.enemy_clock = 0.0
            self.update_slimes(0.2)

    def finish(self, result: str) -> None:
        self.state = result
        if self.score > self.best:
            self.best = self.score
            save_best(self.best)

    def handle_key(self, key: int) -> bool:
        if key == pygame.K_q:
            return False
        if self.state == "menu":
            if key in (pygame.K_RETURN, pygame.K_SPACE):
                self.reset_run()
                self.state = "playing"
            elif key == pygame.K_h:
                self.state = "help"
        elif self.state == "help":
            if key in (pygame.K_ESCAPE, pygame.K_h):
                self.state = "menu"
        elif self.state == "playing":
            if key == pygame.K_ESCAPE:
                self.state = "paused"
            elif key in (pygame.K_f, pygame.K_SPACE):
                self.mine()
            elif key == pygame.K_e:
                self.craft()
            elif key in (pygame.K_w, pygame.K_UP):
                self.move_player(0, -1)
            elif key in (pygame.K_s, pygame.K_DOWN):
                self.move_player(0, 1)
            elif key in (pygame.K_a, pygame.K_LEFT):
                self.move_player(-1, 0)
            elif key in (pygame.K_d, pygame.K_RIGHT):
                self.move_player(1, 0)
        elif self.state == "paused":
            if key in (pygame.K_ESCAPE, pygame.K_RETURN):
                self.state = "playing"
        elif self.state in ("game_over", "victory") and key in (pygame.K_RETURN, pygame.K_SPACE):
            self.reset_run()
            self.state = "playing"
        return True

    def draw_text(self, text: str, font: pygame.font.Font, color: tuple[int, int, int],
                  x: int, y: int, center: bool = False) -> None:
        image = font.render(text, True, color)
        rect = image.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(image, rect)

    def draw_block(self, x: int, y: int, tile: str) -> None:
        px, py = WORLD_X + x * TILE, WORLD_Y + y * TILE
        rect = pygame.Rect(px, py, TILE, TILE)
        if tile == WALL:
            pygame.draw.rect(self.screen, (77, 82, 88), rect)
            pygame.draw.rect(self.screen, (93, 100, 105), (px, py, TILE, 6))
            pygame.draw.line(self.screen, (55, 61, 67), (px, py + 21), (px + TILE, py + 21), 2)
            pygame.draw.line(self.screen, (55, 61, 67), (px + 16, py + 6), (px + 16, py + 21), 2)
        else:
            pygame.draw.rect(self.screen, (91, 66, 48), rect)
            pygame.draw.rect(self.screen, (94, 123, 72), (px, py, TILE, 8))
            pygame.draw.line(self.screen, (78, 57, 43), (px, py + 22), (px + TILE, py + 22), 2)
            pygame.draw.line(self.screen, (78, 57, 43), (px + 20, py + 8), (px + 20, py + 22), 2)
            if tile in ORE:
                material = ORE[tile]
                color = ORE_COLORS[material]
                for ox, oy in ((7, 13), (21, 11), (13, 24), (25, 25)):
                    pygame.draw.rect(self.screen, color, (px + ox, py + oy, 4, 4))
            elif tile == BENCH:
                pygame.draw.rect(self.screen, (129, 83, 48), (px + 4, py + 10, 24, 18))
                pygame.draw.line(self.screen, (225, 179, 92), (px + 6, py + 14), (px + 26, py + 14), 2)
                pygame.draw.line(self.screen, (72, 48, 38), (px + 11, py + 18), (px + 11, py + 26), 2)
            elif tile == PORTAL:
                pulse = (self.elapsed % 1.0) * 3
                pygame.draw.rect(self.screen, (46, 36, 99), (px + 5, py + 3, 22, 28))
                pygame.draw.rect(self.screen, (152, 98, 241), (px + 9, py + 5, 14, 24), 2)
                pygame.draw.rect(self.screen, (89, 218, 237), (px + 12, py + 8, 8, max(4, 18 - int(pulse))), 2)
        pygame.draw.rect(self.screen, (0, 0, 0, 35), rect, 1)

    def draw_explorer(self) -> None:
        x = WORLD_X + self.player.x * TILE
        y = WORLD_Y + self.player.y * TILE
        if self.player.invulnerable and int(self.elapsed * 12) % 2:
            return
        pygame.draw.rect(self.screen, (52, 114, 185), (x + 7, y + 15, 18, 14))
        pygame.draw.rect(self.screen, (224, 172, 124), (x + 8, y + 4, 16, 14))
        pygame.draw.rect(self.screen, (103, 68, 42), (x + 6, y + 2, 20, 7))
        pygame.draw.rect(self.screen, INK, (x + 18, y + 9, 3, 3))
        pygame.draw.rect(self.screen, (41, 65, 108), (x + 8, y + 26, 6, 5))
        pygame.draw.rect(self.screen, (41, 65, 108), (x + 19, y + 26, 6, 5))

    def draw_slime(self, slime: Slime) -> None:
        x, y = WORLD_X + slime.x * TILE, WORLD_Y + slime.y * TILE
        pygame.draw.rect(self.screen, (64, 165, 104), (x + 4, y + 10, 24, 19))
        pygame.draw.rect(self.screen, (92, 208, 127), (x + 8, y + 5, 16, 7))
        pygame.draw.rect(self.screen, INK, (x + 9, y + 13, 4, 4))
        pygame.draw.rect(self.screen, INK, (x + 20, y + 13, 4, 4))

    def draw_hud(self) -> None:
        pygame.draw.rect(self.screen, (29, 35, 43), (0, 0, WIDTH, 106))
        self.draw_text("REDSTONE RUN", self.font, MINT, 22, 17)
        self.draw_text(f"SCORE {self.score:04d}", self.font, WHITE, 245, 17)
        self.draw_text(f"BEST {self.best:04d}", self.font, GOLD, 415, 17)
        self.draw_text(f"HP {max(0, self.player.health)}/3", self.font, RED, 600, 17)
        self.draw_text(f"DEPTH {1 + int(self.elapsed // 30)}", self.small, BLUE, 775, 21)
        inventory_text = (f"REDSTONE {self.inventory['redstone']}/{GOAL['redstone']}    "
                          f"IRON {self.inventory['iron']}/{GOAL['iron']}    "
                          f"COAL {self.inventory['coal']}    "
                          f"CORE {'YES' if self.inventory['beacon_core'] else 'NO'}")
        self.draw_text(inventory_text, self.small, WHITE, 22, 65)

    def draw_world(self) -> None:
        self.screen.fill((28, 31, 36))
        self.draw_hud()
        for y, row in enumerate(self.world):
            for x, tile in enumerate(row):
                self.draw_block(x, y, tile)
        for slime in self.slimes:
            self.draw_slime(slime)
        self.draw_explorer()
        hint = self.message if self.message_timer > 0 else "WASD/Arrows move  •  F mine  •  E craft beside workbench  •  Esc pause"
        pygame.draw.rect(self.screen, (29, 35, 43), (0, 646, WIDTH, 74))
        self.draw_text(hint, self.small, GOLD if self.message_timer > 0 else MUTED, WIDTH // 2, 665, True)
        self.draw_text("Ore veins: red = redstone   tan = iron   dark = coal", self.small, MUTED, WIDTH // 2, 694, True)

    def draw_panel(self, title: str, lines: list[str], color: tuple[int, int, int]) -> None:
        self.screen.fill((28, 31, 36))
        # A tiny block landscape gives the menu a handmade pixel-world identity.
        for x in range(0, WIDTH, TILE):
            self.draw_block(x // TILE, 14, WALL if x % 96 == 0 else FLOOR)
        panel = pygame.Rect(100, 95, 760, 500)
        pygame.draw.rect(self.screen, (38, 45, 53), panel, border_radius=12)
        pygame.draw.rect(self.screen, color, panel, 3, border_radius=12)
        self.draw_text(title, self.title_font, color, WIDTH // 2, 165, True)
        for index, line in enumerate(lines):
            self.draw_text(line, self.font, WHITE if index == 0 else MUTED,
                           WIDTH // 2, 245 + index * 42, True)

    def draw(self) -> None:
        if self.state == "playing":
            self.draw_world()
        elif self.state == "menu":
            self.draw_panel("REDSTONE RUN", [
                "A tiny block-world adventure in Python + Pygame",
                "Mine ore. Craft a beacon core. Outsmart cave slimes.",
                "WASD / arrows move     F mine     E craft at workbench",
                "[ ENTER ]  START ADVENTURE       [ H ]  HOW TO PLAY",
                f"PERSONAL BEST  {self.best:04d}       Made from code-drawn visuals",
            ], MINT)
        elif self.state == "help":
            self.draw_panel("FIELD GUIDE", [
                "Mine colored ore beside you with F (or Space).",
                "Collect 4 redstone + 2 iron; coal is bonus score.",
                "Stand beside the brown workbench and press E to craft.",
                "Reach the purple portal with the beacon core to win.",
                "Cave slimes chase you. Three hearts; avoid contact.",
                "Esc pauses during play. Enter restarts after an ending.",
                "IP ideas: lists, dictionaries, loops, conditions, JSON.",
            ], GOLD)
        else:
            title = "PAUSED" if self.state == "paused" else ("CAVE CLEARED!" if self.state == "victory" else "RUN ENDED")
            if self.state == "victory":
                lines = [f"Score: {self.score}   Best: {self.best}", "Beacon core activated the portal.", "Press Enter to explore again."]
            elif self.state == "game_over":
                lines = [f"Score: {self.score}   Best: {self.best}", "The cave slimes caught up.", "Press Enter to try again."]
            else:
                lines = ["Your world is waiting.", "Press Esc or Enter to continue.", "Press Q to quit."]
            self.draw_panel(title, lines, GOLD if self.state == "paused" else (MINT if self.state == "victory" else RED))
        pygame.display.flip()

    def run(self) -> None:
        running = True
        while running:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.05)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    running = self.handle_key(event.key)
            self.update(dt)
            self.draw()
        pygame.quit()


def main() -> None:
    try:
        RedstoneRun().run()
    except pygame.error as error:
        print(f"Could not start Redstone Run: {error}", file=sys.stderr)
        pygame.quit()


if __name__ == "__main__":
    main()
