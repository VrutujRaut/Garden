# Redstone Run — NotebookLM Project Brief

This source describes the current school project implementation in `game.py`.

## Project overview

Redstone Run is an original, offline 2D block-world adventure made with Python and Pygame. It uses a top-down tile cave with an original pixel-like style drawn from Pygame primitives. It is inspired by broad mining-and-crafting ideas, not a reproduction of Minecraft code, maps, or artwork.

## Goal and gameplay

The explorer starts in a cave with three hearts. Cave slimes take steps toward the explorer. The player mines colored ore blocks that are next to them, collecting four redstone and two iron. Coal is optional bonus score. The player then stands beside a brown workbench and presses E to craft a beacon core. Finally, the explorer reaches the purple portal. The portal only completes the run after the core is crafted. Losing all three hearts ends the run.

Mining ore, crafting the core, and finishing quickly award points. The best score is stored locally in `redstone_best.json`. Slimes gradually shorten their step timer as the run continues. A short invulnerability period follows contact to prevent rapid repeated damage.

## Controls

| Input | Action |
| --- | --- |
| WASD or arrow keys | Move one tile |
| F or Space | Mine an adjacent ore block |
| E | Craft beside the workbench |
| Esc | Pause or resume |
| Enter | Start or restart |
| H from the menu | Open the field guide |
| Q or window close | Quit |

## Game states

Menu, field guide, playing, paused, game over, and victory are selected by a state string. The main game loop handles Pygame events, updates timers and entities, and draws the active screen.

## Programming concepts from CBSE Class XI IP

- **Lists:** `world` is a list of tile rows; each row is a list of character tile codes. Loops traverse the map for collision and rendering.
- **Dictionaries:** The `inventory` dictionary maps material names to counts. The `RECIPE` dictionary maps materials to crafting amounts.
- **Variables and data types:** Integer grid positions, scores, inventory counts, text tile codes, Boolean conditions, and floating-point timers control gameplay.
- **Operators and conditions:** Arithmetic computes scores and positions; comparisons and Boolean logic check walls, recipe requirements, health, and game state.
- **Loops:** The main loop repeats event handling and rendering; `for` loops traverse rows, tiles, and enemies.
- **Functions and classes:** Methods split movement, mining, crafting, enemy updates, scoring, and drawing. `Explorer`, `Slime`, and `RedstoneRun` keep related data and actions together.
- **File handling and exceptions:** JSON stores the best score. Missing, corrupt, or inaccessible data is handled without a crash.
- **Randomness:** Slime movement timers vary at the start of a run.

This project demonstrates selected Python programming concepts. It does not cover the entire Class XI IP syllabus, including every computer-system, RDBMS/SQL, and emerging-trend topic.

## Dependencies and offline use

Python 3.10+ and Pygame are required. Install with `python -m pip install -r requirements.txt`, then run `python game.py`. The game does not access the internet while running and uses no external art or sound files.

## Testing

`test_game.py` contains small checks for the list-based world, wall collision, mining, recipe checks, portal progression, slime damage, pause/restart, high-score file handling, and rendering every screen. Run it with `python -m unittest -v` after installing Pygame.

## Originality and references

The source code, game rules, tile map, characters, and visuals were made specifically for this assignment. No existing game code, maps, or assets were copied. Official Python/Pygame references informed API usage. The official CBSE IP syllabus was used to map the programming examples:

- [CBSE Class XI Informatics Practices syllabus, 2026–27](https://cbseacademic.nic.in/web_material/CurriculumMain27/SecPart2/Informatics_Practices_SecP2_2026-27.pdf)
- [Python JSON documentation](https://docs.python.org/3/library/json.html)
- [Pygame drawing documentation](https://www.pygame.org/docs/ref/draw.html)
