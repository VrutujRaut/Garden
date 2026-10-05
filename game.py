"""Signal Bloom: restore the station beacon and outsmart its security drones."""

from __future__ import annotations

import json
import math
import random
import sys
from array import array
from pathlib import Path

import pygame


# Window, playfield, and progression settings are kept together for easy tuning.
WIDTH, HEIGHT = 960, 640
ARENA = pygame.Rect(24, 92, WIDTH - 48, HEIGHT - 112)
FPS = 60
GOAL_ORBS = 12
STARTING_LIVES = 3
PULSE_COST = 3
PULSE_RADIUS = 155
SAVE_PATH = Path(__file__).with_name("highscore.json")

BG = (8, 16, 31)
PANEL = (15, 29, 49)
GRID = (22, 43, 64)
WHITE = (229, 243, 251)
MUTED = (139, 164, 184)
CYAN = (73, 224, 224)
GOLD = (255, 205, 102)
PINK = (255, 106, 139)
GREEN = (117, 239, 165)


def load_high_score(path: Path = SAVE_PATH) -> int:
    """Load the best score; missing, malformed, or unexpected data is harmless."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        score = data.get("high_score", 0)
        return max(0, int(score))
    except (OSError, ValueError, TypeError, AttributeError, json.JSONDecodeError):
        return 0


def save_high_score(score: int, path: Path = SAVE_PATH) -> None:
    """Save the best score without allowing a file error to close the game."""
    try:
        path.write_text(json.dumps({"high_score": int(score)}, indent=2), encoding="utf-8")
    except OSError:
        pass


def distance_squared(a: tuple[float, float], b: tuple[float, float]) -> float:
    dx, dy = a[0] - b[0], a[1] - b[1]
    return dx * dx + dy * dy


class SoundBank:
    """Small synthesized effects; the game still works if audio cannot initialize."""

    def __init__(self) -> None:
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
            self.sounds = {
                "collect": self._tone(720, 0.10, 0.20),
                "pulse": self._tone(250, 0.24, 0.28, sweep=520),
                "hit": self._tone(145, 0.22, 0.25, sweep=75),
                "open": self._tone(560, 0.34, 0.18, sweep=920),
            }
        except (pygame.error, OSError):
            self.sounds = {}

    @staticmethod
    def _tone(start_hz: float, duration: float, volume: float, sweep: float = 0) -> pygame.mixer.Sound:
        rate = 22050
        samples = array("h")
        for index in range(int(rate * duration)):
            t = index / rate
            progress = t / duration
            frequency = start_hz + sweep * progress
            envelope = min(1.0, t * 35) * max(0.0, 1.0 - progress) ** 1.4
            value = int(32767 * volume * envelope * math.sin(2 * math.pi * frequency * t))
            samples.append(value)
        return pygame.mixer.Sound(buffer=samples.tobytes())

    def play(self, name: str) -> None:
        sound = self.sounds.get(name)
        if sound:
            try:
                sound.play()
            except pygame.error:
                pass


class Player:
    def __init__(self) -> None:
        self.x, self.y = ARENA.left + 120, ARENA.centery + 40
        self.radius = 13
        self.speed = 245
        self.lives = STARTING_LIVES
        self.invulnerable = 0.0
        self.charge = 0

    @property
    def position(self) -> tuple[float, float]:
        return self.x, self.y

    def move(self, keys: pygame.key.ScancodeWrapper, dt: float) -> None:
        dx = float(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - float(keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = float(keys[pygame.K_s] or keys[pygame.K_DOWN]) - float(keys[pygame.K_w] or keys[pygame.K_UP])
        if dx and dy:
            length = math.hypot(dx, dy)
            dx, dy = dx / length, dy / length
        self.x += dx * self.speed * dt
        self.y += dy * self.speed * dt
        self.x = max(ARENA.left + self.radius, min(ARENA.right - self.radius, self.x))
        self.y = max(ARENA.top + self.radius, min(ARENA.bottom - self.radius, self.y))
        self.invulnerable = max(0.0, self.invulnerable - dt)

    def draw(self, surface: pygame.Surface) -> None:
        if self.invulnerable > 0 and int(self.invulnerable * 14) % 2 == 0:
            return
        center = (round(self.x), round(self.y))
        pygame.draw.circle(surface, (19, 85, 110), center, self.radius + 7)
        pygame.draw.circle(surface, CYAN, center, self.radius)
        pygame.draw.circle(surface, WHITE, (center[0] - 3, center[1] - 4), 4)
        pygame.draw.circle(surface, (35, 143, 163), center, self.radius, 2)


class Drone:
    def __init__(self, x: float, y: float, speed: float, variant: int = 0) -> None:
        self.x, self.y = x, y
        self.speed = speed
        self.radius = 14 if variant == 0 else 17
        self.stunned = 0.0
        self.variant = variant
        self.phase = random.random() * math.tau

    def update(self, target: tuple[float, float], dt: float, elapsed: float) -> None:
        self.stunned = max(0.0, self.stunned - dt)
        self.phase += dt * 3
        if self.stunned > 0:
            return
        dx, dy = target[0] - self.x, target[1] - self.y
        length = max(1.0, math.hypot(dx, dy))
        # Larger amber drones drift from side to side, giving them a distinct approach.
        weave = math.sin(self.phase) * (0.30 if self.variant else 0.10)
        vx, vy = dx / length - dy / length * weave, dy / length + dx / length * weave
        norm = max(1.0, math.hypot(vx, vy))
        self.x += vx / norm * self.speed * dt
        self.y += vy / norm * self.speed * dt

    def draw(self, surface: pygame.Surface) -> None:
        center = (round(self.x), round(self.y))
        color = (117, 137, 151) if self.stunned else (GOLD if self.variant else PINK)
        pygame.draw.circle(surface, (*color[:3],), center, self.radius + 5, 1)
        pygame.draw.circle(surface, color, center, self.radius)
        pygame.draw.circle(surface, BG, center, max(3, self.radius // 3))
        if self.stunned:
            for offset in (-8, 0, 8):
                pygame.draw.circle(surface, WHITE, (center[0] + offset, center[1] - self.radius - 4), 2)


class Orb:
    def __init__(self, x: float, y: float) -> None:
        self.x, self.y = x, y
        self.phase = random.random() * math.tau

    def draw(self, surface: pygame.Surface, elapsed: float) -> None:
        radius = 7 + int((math.sin(elapsed * 5 + self.phase) + 1) * 1.5)
        center = (round(self.x), round(self.y))
        pygame.draw.circle(surface, (40, 103, 104), center, radius + 6)
        pygame.draw.circle(surface, GREEN, center, radius)
        pygame.draw.circle(surface, WHITE, (center[0] - 2, center[1] - 2), 2)


class Particle:
    def __init__(self, x: float, y: float, color: tuple[int, int, int], burst_speed: float = 110) -> None:
        angle = random.random() * math.tau
        speed = random.uniform(burst_speed * 0.35, burst_speed)
        self.x, self.y = x, y
        self.vx, self.vy = math.cos(angle) * speed, math.sin(angle) * speed
        self.color = color
        self.life = self.max_life = random.uniform(0.25, 0.58)
        self.size = random.randint(2, 4)

    def update(self, dt: float) -> None:
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt

    def draw(self, surface: pygame.Surface) -> None:
        if self.life > 0:
            pygame.draw.circle(surface, self.color, (round(self.x), round(self.y)), max(1, int(self.size * self.life / self.max_life)))


class SignalBloomGame:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Signal Bloom")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.fonts = {
            "tiny": pygame.font.Font(None, 20),
            "small": pygame.font.Font(None, 25),
            "body": pygame.font.Font(None, 30),
            "title": pygame.font.Font(None, 74),
            "sub": pygame.font.Font(None, 38),
        }
        self.sounds = SoundBank()
        self.high_score = load_high_score()
        self.state = "menu"
        self.elapsed = 0.0
        self.score = 0
        self.orbs_collected = 0
        self.player = Player()
        self.drones: list[Drone] = []
        self.orbs: list[Orb] = []
        self.particles: list[Particle] = []
        self.spawn_timer = 0.0
        self.pulse_flash = 0.0
        self.beacon_flash = 0.0
        self.new_record = False
        self.background_stars = [
            (random.randrange(0, WIDTH), random.randrange(0, HEIGHT), random.choice((1, 1, 2)))
            for _ in range(70)
        ]

    def start_game(self) -> None:
        self.player = Player()
        self.elapsed = 0.0
        self.score = 0
        self.orbs_collected = 0
        self.drones = []
        self.orbs = []
        self.particles = []
        self.spawn_timer = 0.0
        self.pulse_flash = self.beacon_flash = 0.0
        self.new_record = False
        for _ in range(5):
            self.spawn_orb()
        self.spawn_drone(initial=True)
        self.spawn_drone(initial=True)
        self.state = "playing"

    def spawn_orb(self) -> None:
        for _ in range(40):
            x = random.uniform(ARENA.left + 36, ARENA.right - 36)
            y = random.uniform(ARENA.top + 36, ARENA.bottom - 36)
            if distance_squared((x, y), self.player.position) > 95**2:
                self.orbs.append(Orb(x, y))
                return
        self.orbs.append(Orb(ARENA.centerx, ARENA.centery))

    def spawn_drone(self, initial: bool = False) -> None:
        side = random.randrange(4)
        margin = 24
        if side == 0:
            x, y = random.uniform(ARENA.left, ARENA.right), ARENA.top + margin
        elif side == 1:
            x, y = ARENA.right - margin, random.uniform(ARENA.top, ARENA.bottom)
        elif side == 2:
            x, y = random.uniform(ARENA.left, ARENA.right), ARENA.bottom - margin
        else:
            x, y = ARENA.left + margin, random.uniform(ARENA.top, ARENA.bottom)
        stage = int(self.elapsed // 22)
        speed = min(112 + stage * 13, 190) if initial else min(105 + stage * 13, 184)
        variant = 1 if self.elapsed > 48 and random.random() < 0.32 else 0
        self.drones.append(Drone(x, y, speed, variant))

    def burst(self, x: float, y: float, color: tuple[int, int, int], count: int = 12, speed: float = 120) -> None:
        self.particles.extend(Particle(x, y, color, speed) for _ in range(count))

    def use_pulse(self) -> None:
        if self.player.charge < PULSE_COST:
            return
        self.player.charge -= PULSE_COST
        self.pulse_flash = 0.34
        self.sounds.play("pulse")
        self.burst(self.player.x, self.player.y, CYAN, 24, 215)
        radius_sq = PULSE_RADIUS * PULSE_RADIUS
        for drone in self.drones:
            if distance_squared(self.player.position, (drone.x, drone.y)) <= radius_sq:
                drone.stunned = 2.8
                dx, dy = drone.x - self.player.x, drone.y - self.player.y
                length = max(1.0, math.hypot(dx, dy))
                drone.x += dx / length * 36
                drone.y += dy / length * 36
                self.burst(drone.x, drone.y, GOLD, 8, 85)

    def hit_player(self, drone: Drone) -> None:
        if self.player.invulnerable > 0:
            return
        self.player.lives -= 1
        self.player.invulnerable = 1.5
        self.sounds.play("hit")
        self.burst(self.player.x, self.player.y, PINK, 18, 160)
        dx, dy = self.player.x - drone.x, self.player.y - drone.y
        length = max(1.0, math.hypot(dx, dy))
        self.player.x = max(ARENA.left + 18, min(ARENA.right - 18, self.player.x + dx / length * 52))
        self.player.y = max(ARENA.top + 18, min(ARENA.bottom - 18, self.player.y + dy / length * 52))
        drone.stunned = 0.55
        if self.player.lives <= 0:
            self.finish("game_over")

    def finish(self, state: str) -> None:
        self.state = state
        if self.score > self.high_score:
            self.high_score = self.score
            self.new_record = True
            save_high_score(self.high_score, SAVE_PATH)

    def update(self, dt: float) -> None:
        if self.state != "playing":
            return
        self.elapsed += dt
        self.score = self.orbs_collected * 100 + int(self.elapsed * 2)
        self.player.move(pygame.key.get_pressed(), dt)
        self.pulse_flash = max(0.0, self.pulse_flash - dt)
        self.beacon_flash = max(0.0, self.beacon_flash - dt)

        stage = int(self.elapsed // 22)
        spawn_interval = max(3.4, 8.0 - stage * 0.85)
        self.spawn_timer += dt
        if self.spawn_timer >= spawn_interval and len(self.drones) < min(3 + stage, 8):
            self.spawn_timer = 0.0
            self.spawn_drone()

        for drone in self.drones:
            drone.speed = min((105 if drone.variant == 0 else 88) + stage * 12, 184)
            drone.update(self.player.position, dt, self.elapsed)
            if distance_squared(self.player.position, (drone.x, drone.y)) <= (self.player.radius + drone.radius) ** 2:
                self.hit_player(drone)
                if self.state != "playing":
                    return

        for orb in self.orbs[:]:
            if distance_squared(self.player.position, (orb.x, orb.y)) <= (self.player.radius + 12) ** 2:
                self.orbs.remove(orb)
                self.orbs_collected += 1
                self.player.charge = min(9, self.player.charge + 1)
                self.score = self.orbs_collected * 100 + int(self.elapsed * 2)
                self.sounds.play("collect")
                self.burst(orb.x, orb.y, GREEN, 12)
                if self.orbs_collected == GOAL_ORBS:
                    self.sounds.play("open")
                    self.beacon_flash = 1.0
                if self.orbs_collected < GOAL_ORBS and len(self.orbs) < 5:
                    self.spawn_orb()

        if self.orbs_collected >= GOAL_ORBS and distance_squared(
            self.player.position, (ARENA.centerx, ARENA.centery)
        ) <= 31**2:
            self.score += 500
            self.finish("victory")

        for particle in self.particles:
            particle.update(dt)
        self.particles = [particle for particle in self.particles if particle.life > 0]

    def handle_key(self, key: int) -> bool:
        if key in (pygame.K_q,):
            return False
        if key == pygame.K_h and self.state == "menu":
            self.state = "help"
        elif key == pygame.K_ESCAPE and self.state == "help":
            self.state = "menu"
        elif key in (pygame.K_p, pygame.K_ESCAPE) and self.state == "playing":
            self.state = "paused"
        elif key in (pygame.K_p, pygame.K_ESCAPE) and self.state == "paused":
            self.state = "playing"
        elif key == pygame.K_SPACE and self.state == "playing":
            self.use_pulse()
        elif key in (pygame.K_RETURN, pygame.K_SPACE) and self.state == "menu":
            self.start_game()
        elif key in (pygame.K_RETURN, pygame.K_SPACE) and self.state in ("game_over", "victory"):
            self.start_game()
        elif key == pygame.K_h and self.state in ("game_over", "victory"):
            self.state = "help"
        return True

    def draw_text(self, text: str, font: pygame.font.Font, color: tuple[int, int, int], x: int, y: int, align: str = "center") -> None:
        image = font.render(text, True, color)
        rect = image.get_rect()
        alignment = "midright" if align == "right" else align
        setattr(rect, alignment, (x, y))
        self.screen.blit(image, rect)

    def draw_background(self) -> None:
        self.screen.fill(BG)
        for x, y, size in self.background_stars:
            pygame.draw.circle(self.screen, (31, 57, 77), (x, y), size)
        pygame.draw.rect(self.screen, PANEL, ARENA, border_radius=14)
        for x in range(ARENA.left + 24, ARENA.right, 36):
            pygame.draw.line(self.screen, GRID, (x, ARENA.top + 1), (x, ARENA.bottom - 1), 1)
        for y in range(ARENA.top + 20, ARENA.bottom, 36):
            pygame.draw.line(self.screen, GRID, (ARENA.left + 1, y), (ARENA.right - 1, y), 1)
        pygame.draw.rect(self.screen, (37, 71, 91), ARENA, 2, border_radius=14)

    def draw_beacon(self) -> None:
        center = (ARENA.centerx, ARENA.centery)
        active = self.orbs_collected >= GOAL_ORBS
        color = GREEN if active else (54, 97, 111)
        radius = 28 + int(self.beacon_flash * 7)
        pygame.draw.circle(self.screen, (*color,), center, radius + 12, 2)
        pygame.draw.circle(self.screen, color, center, radius, 2)
        pygame.draw.circle(self.screen, color if active else (34, 67, 80), center, 10)
        if active:
            self.draw_text("EXIT", self.fonts["tiny"], GREEN, center[0], center[1] + 41)

    def draw_hud(self) -> None:
        pygame.draw.rect(self.screen, PANEL, (0, 0, WIDTH, 78))
        self.draw_text("SIGNAL BLOOM", self.fonts["small"], CYAN, 26, 20, "topleft")
        self.draw_text(f"SCORE  {self.score:05d}", self.fonts["body"], WHITE, 27, 48, "topleft")
        self.draw_text(f"ORBS  {self.orbs_collected:02d}/{GOAL_ORBS}", self.fonts["body"], GREEN, 310, 34, "center")
        self.draw_text(f"PULSE  {self.player.charge}/{PULSE_COST}", self.fonts["small"], CYAN if self.player.charge >= PULSE_COST else MUTED, 558, 35, "center")
        self.draw_text("♥ " * self.player.lives, self.fonts["body"], PINK, 755, 34, "center")
        self.draw_text(f"BEST {self.high_score:05d}", self.fonts["small"], GOLD, 922, 35, "right")

    def draw_playfield(self) -> None:
        self.draw_background()
        self.draw_beacon()
        for orb in self.orbs:
            orb.draw(self.screen, self.elapsed)
        for drone in self.drones:
            drone.draw(self.screen)
        for particle in self.particles:
            particle.draw(self.screen)
        if self.pulse_flash > 0:
            radius = int(PULSE_RADIUS * (1 - self.pulse_flash / 0.34))
            pygame.draw.circle(self.screen, CYAN, (round(self.player.x), round(self.player.y)), max(8, radius), 2)
        self.player.draw(self.screen)
        self.draw_hud()
        if self.orbs_collected >= GOAL_ORBS:
            self.draw_text("BEACON RESTORED  •  REACH THE CENTER", self.fonts["small"], GREEN, WIDTH // 2, HEIGHT - 10)
        else:
            self.draw_text("COLLECT SIGNAL ORBS  •  SPACE: PULSE  •  P: PAUSE", self.fonts["tiny"], MUTED, WIDTH // 2, HEIGHT - 10)

    def draw_overlay(self, title: str, subtitle: str, accent: tuple[int, int, int], lines: list[str]) -> None:
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((4, 10, 22, 208))
        self.screen.blit(shade, (0, 0))
        self.draw_text(title, self.fonts["title"], accent, WIDTH // 2, 170)
        self.draw_text(subtitle, self.fonts["body"], WHITE, WIDTH // 2, 225)
        for index, line in enumerate(lines):
            self.draw_text(line, self.fonts["small"], MUTED if index else WHITE, WIDTH // 2, 300 + index * 39)

    def draw_menu(self) -> None:
        self.draw_background()
        flower_center = (WIDTH // 2, 187)
        for petal in range(6):
            angle = petal * math.tau / 6
            petal_center = (
                round(flower_center[0] + math.cos(angle) * 13),
                round(flower_center[1] + math.sin(angle) * 13),
            )
            pygame.draw.circle(self.screen, GREEN if petal % 2 == 0 else CYAN, petal_center, 8)
        pygame.draw.circle(self.screen, GOLD, flower_center, 5)
        self.draw_text("SIGNAL BLOOM", self.fonts["title"], WHITE, WIDTH // 2, 275)
        self.draw_text("A little station. A lot of security drones.", self.fonts["body"], MUTED, WIDTH // 2, 323)
        self.draw_text("[ ENTER ]   BEGIN", self.fonts["sub"], CYAN, WIDTH // 2, 409)
        self.draw_text("[ H ]  HOW TO PLAY", self.fonts["small"], WHITE, WIDTH // 2, 456)
        self.draw_text(f"PERSONAL BEST   {self.high_score:05d}", self.fonts["small"], GOLD, WIDTH // 2, 514)
        self.draw_text("WASD / ARROWS MOVE     •     SPACE PULSE     •     P PAUSE", self.fonts["tiny"], MUTED, WIDTH // 2, 600)

    def draw_help(self) -> None:
        self.draw_background()
        self.draw_overlay("HOW TO PLAY", "Restore the garden station's beacon.", CYAN, [
            "Move with WASD or the arrow keys.",
            "Collect 12 green signal orbs to charge the beacon.",
            "Every orb also adds one charge to your pulse.",
            "Press SPACE with 3 charges to stun nearby drones.",
            "Reach the glowing center after the beacon opens.",
            "Avoid drones. You have 3 lives; the pace rises over time.",
            "P or Esc pauses. Esc returns here to the menu.",
            "Press Esc to return to the title screen.",
        ])

    def draw(self) -> None:
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "help":
            self.draw_help()
        else:
            self.draw_playfield()
            if self.state == "paused":
                self.draw_overlay("PAUSED", "Take a breath, ranger.", GOLD, ["Press P or Esc to continue.", "Press Q or close the window to quit."])
            elif self.state == "game_over":
                title = "NEW PERSONAL BEST" if self.new_record else "RUN ENDED"
                self.draw_overlay(title, f"Final score: {self.score:05d}     •     Orbs: {self.orbs_collected}/{GOAL_ORBS}", PINK, [
                    f"Personal best: {self.high_score:05d}",
                    "Press Enter to try again.",
                    "Press H to view instructions.",
                ])
            elif self.state == "victory":
                self.draw_overlay("BEACON RESTORED", f"You brought the garden back to life!   Score: {self.score:05d}", GREEN, [
                    f"Personal best: {self.high_score:05d}",
                    "Press Enter to play again.",
                    "Press H to view instructions.",
                ])
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
        SignalBloomGame().run()
    except pygame.error as error:
        print(f"Could not start Signal Bloom: {error}", file=sys.stderr)
        pygame.quit()


if __name__ == "__main__":
    main()
