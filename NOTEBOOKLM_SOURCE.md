# Signal Bloom — NotebookLM Project Brief

Use this file as a source document for learning about and presenting the school project. The statements below describe the current implementation in `game.py`.

## Project at a glance

Signal Bloom is an original, offline, top-down arcade game implemented in Python with Pygame. A player restores a garden station's beacon by collecting signal orbs while avoiding security drones. The program is intended to be understandable as a school computer-science assignment.

## Objective and play loop

The player moves around one bounded arena. Green orbs appear around the arena and can be collected by touching them. Collecting twelve orbs activates the beacon at the center. The player must reach that beacon to win. Pink drones chase the player, and larger amber drones that weave toward the player may appear later. Contact costs a life. The run ends after the player's three lives are used.

Each orb gives 100 points and one pulse charge. Time survived also contributes two points per second. A successful beacon visit adds a 500-point bonus. Pressing Space spends three charges and stuns all drones within range for 2.8 seconds. A player can hold at most nine charges. Drones increase in speed and spawn frequency as the run continues; progression has caps.

## Controls

| Input | Action |
| --- | --- |
| W, A, S, D or arrow keys | Move |
| Space | Spend three charges to stun nearby drones |
| P or Esc during a run | Pause or resume |
| Enter | Start or restart |
| H on title or ending screen | Open instructions |
| Esc on instructions | Return to title |
| Q or window close button | Quit |

## Screens and program flow

The game uses six states: title menu, instructions, playing, paused, game over, and victory. The main loop processes Pygame events, updates gameplay using elapsed frame time, draws the current screen, and refreshes the display. Pause stops gameplay updates while keeping the screen visible. Enter begins a new run from the menu or either ending screen.

## Important Python structures

- `SignalBloomGame` coordinates state, input, object updates, collision responses, scoring, drawing, and the main loop.
- `Player` stores movement, lives, invulnerability time, and pulse charge.
- `Drone` stores position, movement speed, type, and stun time.
- `Orb` stores a collectible's position and animation phase.
- `Particle` stores a short-lived visual effect.
- Lists hold the active drones, orbs, and particles.
- Constants define window dimensions, arena bounds, lives, the orb goal, and pulse settings.

## Collision, timing, and difficulty

Circular collisions are checked with squared distance between two positions. This avoids a square root for simple overlap checks. Square roots are used when movement needs a normalized direction. The frame loop caps elapsed frame time so a long pause between frames cannot cause a single enormous movement step.

Difficulty stages advance every 22 seconds. Higher stages raise drone speed, shorten the spawn interval, and raise the maximum number of active drones, up to caps. A second drone type adds a weaving movement pattern.

## Saving and recovery

The best score is read from and written to `highscore.json` next to `game.py`, using Python's `json` and `pathlib` modules. If the file is missing, corrupt, or inaccessible, the game uses a score of zero or continues without saving. The local score file is listed in `.gitignore` so it is not included in the public source repository.

## Libraries and assets

The game uses Python standard-library modules `json`, `math`, `random`, `sys`, `pathlib`, and `array`, plus the installable Pygame package. Shapes, stars, and particles are drawn in code; simple sound effects are synthesized at runtime. No external art or audio files, network service, online account, or internet connection during play is required.

## How to install and run

Install Python 3.10 or later, then install Pygame with `py -m pip install pygame` on Windows (or `python -m pip install pygame`). From the project folder, launch with `py game.py` (or `python game.py`).

## Verification

The project has 12 automated checks in `test_game.py`. They cover movement bounds, orb collection and charge, pulse and stun behavior, life loss, difficulty progression, pause and resume, restart, victory, score load/save and invalid data, rendering every game screen, and responding to a normal window-close event. Both Python source files were syntax-compiled, and the desktop window was launched and closed successfully during development.

## Originality and references

The source code, game rules, and game-specific visuals were developed for this school assignment. Existing game source code and art assets were not copied. Official documentation was used to understand Python and Pygame concepts:

- [Python 3.12 `json` module](https://docs.python.org/3.12/library/json.html)
- [Pygame display module](https://www.pygame.org/docs/ref/display.html)
- [Pygame drawing module](https://www.pygame.org/docs/ref/draw.html)

## Vocabulary

- **Game loop:** The repeating cycle that handles events, updates objects, and draws frames.
- **State:** A label describing which screen or phase is active.
- **Collision detection:** A calculation that determines whether two objects overlap.
- **Procedural visual:** A visual drawn by program instructions instead of loaded artwork.
- **High score:** The largest score saved between runs on the same computer.
