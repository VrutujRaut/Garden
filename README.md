# Signal Bloom

**Signal Bloom** is an original top-down arcade game made in Python with Pygame. Restore a small garden station's beacon while avoiding its security drones.

## Objective

Collect 12 green signal orbs to activate the beacon in the center of the arena. Reach the beacon to finish the run. Drones pursue the player, and their speed and spawn rate increase as time passes. You have three lives.

## Gameplay and controls

| Key | Action |
| --- | --- |
| W A S D or arrow keys | Move |
| Space | Spend 3 collected charges to stun nearby drones |
| P or Esc | Pause or resume during a run |
| Enter | Start or restart |
| H | Open instructions from the title or end screen |
| Esc | Return to the title from instructions |
| Q | Quit |

Each orb is worth 100 points and grants one pulse charge (up to nine). A pulse stuns every drone within range for a short time. Score also increases slowly while surviving, and reaching the beacon grants a completion bonus. Your personal best is saved in `highscore.json` beside `game.py`.

## Features

- Keyboard-driven title and instructions screens, pause, victory, game over, and restart
- Pursuing drones with a second, weaving drone type later in a run
- Orb collection, pulse charge, beacon objective, three lives, and invulnerability after a hit
- Gradually increasing spawn rate and drone speed
- Pygame-drawn visuals, animation particles, and synthesized sound effects (no external assets)
- Local high-score save that handles missing, malformed, or unwritable save files safely
- Runs offline after Python and Pygame are installed

## Python modules and dependencies

- Python standard library: `json`, `math`, `random`, `sys`, `pathlib`, and `array`
- External package: Pygame

No web server, browser, API, or online account is used by the game.

## Installation and running

1. Install Python 3.10 or later.
2. In a terminal in this folder, install the dependency:

   ```sh
   python -m pip install -r requirements.txt
   ```

3. Start the game:

   ```sh
   python game.py
   ```

On some systems the Python launcher is named `py`; use `py -m pip install -r requirements.txt` and `py game.py` if needed.

## Files

```text
game.py            Game loop, screens, entities, gameplay, effects, and save handling
requirements.txt   Pygame dependency
README.md          Setup, rules, and project explanation
DESIGN_SPEC.md     Short development specification
FAQ.md             30 common questions and answers about the game and code
NOTEBOOKLM_SOURCE.md  Fact sheet for studying or explaining this project in NotebookLM
NOTEBOOKLM_VIDEO_PROMPT.md  Ready-to-use NotebookLM video overview instructions
test_game.py       12 non-visual game-logic and screen checks
.gitignore         Keeps local save data and Python cache files out of Git
highscore.json     Created automatically after a new best score
```

For NotebookLM, add `NOTEBOOKLM_SOURCE.md` as a source, then use the prompt in `NOTEBOOKLM_VIDEO_PROMPT.md` to guide a classroom-friendly video overview. See [FAQ.md](FAQ.md) for common questions and answers.

## Programming concepts to explain

- **Game loop and events:** The main loop handles window and keyboard events, updates the game, and draws a frame at a controlled rate.
- **Classes and objects:** `Player`, `Drone`, `Orb`, `Particle`, and `SignalBloomGame` keep related data and behavior together.
- **Conditions and states:** A state variable selects the menu, instructions, active game, pause overlay, or ending screen.
- **Lists and loops:** Lists hold drones, orbs, and particles; loops update and draw those objects.
- **Collision and mathematics:** Squared distance compares two positions without needing a square root for every collision. `math.hypot` normalizes movement and pulse knockback.
- **Randomness:** Orb positions, drone edges, and particle bursts vary from run to run.
- **File handling and exceptions:** JSON stores the best score. Missing, invalid, or inaccessible data is handled without crashing gameplay.
- **Functions and constants:** Reusable methods split movement, collision, drawing, saving, and progression into explainable pieces; constants make tuning straightforward.

## Testing performed

Run the automated checks with:

```sh
python -m unittest -v
```

Twelve automated checks passed for movement bounds, orb collection and score, pulse charge and stun, drone contact and lives, difficulty progression, pause/resume, restart, victory, high-score saving/loading, corrupt or missing save data, drawing every screen, and closing through the normal window event. `py_compile` also passed for both Python files. I launched the game on the desktop, confirmed the `Signal Bloom` window opened, and closed it through its normal close event. Audio is optional and is disabled gracefully if unavailable.

## Originality and references

The source code, game rules, visuals, and game-specific implementation were developed for this project. No existing game source or art assets were copied. Python and Pygame documentation were consulted for programming and library concepts: [Python `json` documentation](https://docs.python.org/3.12/library/json.html), [Pygame display documentation](https://www.pygame.org/docs/ref/display.html), and [Pygame drawing documentation](https://www.pygame.org/docs/ref/draw.html).
