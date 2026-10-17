# Redstone Run

**Redstone Run** is an original, Minecraft-inspired 2D cave adventure written in Python with Pygame. Explore a small block world, mine ore, craft a beacon core, and reach the portal before the cave slimes catch you.

## Objective and gameplay

Collect **4 redstone and 2 iron** by mining nearby ore veins. Find the brown workbench and craft a beacon core. Then travel to the purple portal and step onto it to escape. Coal is optional bonus score. Cave slimes move toward you; three hearts are available. Mining, crafting, and finishing quickly add points. The best score is saved locally.

## Controls

| Key | Action |
| --- | --- |
| W, A, S, D or arrow keys | Move one tile |
| F or Space | Mine an ore block beside you |
| E | Craft at a nearby workbench |
| Esc | Pause or resume |
| Enter | Start or restart |
| H | Open the help screen from the menu |
| Q or window close button | Quit |

## Features

- Original block-style tile cave with ore veins, rocky shelves, workbench, and portal
- Mining and crafting objective with a dictionary-based recipe and inventory
- Cave slimes that pursue the player, hearts, invulnerability time, and game over
- Menu, instructions, playing, pause, victory, and game-over screens
- Scoring, time bonus, local high score, restart, and difficulty that gradually rises
- All visuals drawn in Python using Pygame primitives; no separate art assets required
- Works offline after Pygame is installed

## Class XI Informatics Practices connections

This project is an illustrative Python project, not a replacement for the full syllabus. It shows lists (tile-map rows and entity collections), dictionaries (inventory and crafting recipe), variables and data types, operators, conditions, loops, functions/methods, classes, random movement timing, event handling, and JSON file handling with exception handling. The game does not claim to teach all syllabus units such as computer systems, relational databases and SQL, or emerging trends.

## Python modules and dependency

- Python standard library: `json`, `random`, `sys`, and `pathlib`
- Installable package: Pygame (`pygame>=2.5,<3`)

## Installation and run

1. Install Python 3.10 or later.
2. In a terminal in this folder, install Pygame:

   ```sh
   python -m pip install -r requirements.txt
   ```

   On Windows, `py -m pip install -r requirements.txt` may be used instead.

3. Start the game:

   ```sh
   python game.py
   ```

   On Windows, `py game.py` may be used instead.

## File structure

```text
game.py                  Game loop, world, entities, controls, drawing, and saves
test_game.py             Small non-visual checks for game rules
requirements.txt         Pygame dependency
DESIGN_SPEC.md           Concept and implementation specification
FAQ.md                   Common questions and answers
NOTEBOOKLM_SOURCE.md     Project brief to add as a NotebookLM source
NOTEBOOKLM_VIDEO_PROMPT.md  Classroom video overview prompt
redstone_best.json       Local best score, created while playing (ignored by Git)
```

## Important programming ideas

- **Game loop:** Repeatedly checks events, updates the world, and draws the current screen.
- **Grid and lists:** The map is a list of rows. Each row is a list containing one-character tile codes. Loops draw and inspect these tiles.
- **Dictionary:** `inventory` maps item names to counts. `RECIPE` maps material names to the amounts needed to craft the core.
- **Conditions and operators:** The game checks map bounds, walls, inventory requirements, health, and portal state before changing values.
- **Functions and classes:** Methods split movement, mining, crafting, collisions, and drawing into parts. `Explorer`, `Slime`, and `RedstoneRun` group related data and behavior.
- **File handling:** JSON stores the best score. Missing, corrupt, or inaccessible data does not prevent play.
- **Procedural visuals:** Pygame rectangles and lines create a blocky visual style in code. There are no downloaded image assets.

## Testing

Run the logic checks with:

```sh
python -m unittest -v
```

The 13 checks cover map dimensions, walls and ore collision, mining, recipe checks, portal progression, slime damage, pause/restart, saving, drawing each screen, and a normal close event. They passed under Python 3.12.14 and Pygame 2.6.1. `py_compile` also passed. I launched the Pygame window and inspected generated menu and gameplay renders; all visuals are drawn from code. A full hands-on playthrough was not recorded as an automated test.

## Originality and references

The game code, game rules, and code-drawn visuals were created for this project. No source code, sprites, textures, sounds, or game-specific logic were copied from an existing game. The block-world theme is an original school-project interpretation and is not affiliated with Mojang or Microsoft. The official CBSE Class XI Informatics Practices syllabus was consulted to map the Python examples accurately; official Python and Pygame documentation was consulted for library concepts.

- [CBSE Class XI Informatics Practices syllabus, 2026–27 (official PDF)](https://cbseacademic.nic.in/web_material/CurriculumMain27/SecPart2/Informatics_Practices_SecP2_2026-27.pdf)
- [Python `json` module documentation](https://docs.python.org/3/library/json.html)
- [Pygame drawing module documentation](https://www.pygame.org/docs/ref/draw.html)
- [Pygame event module documentation](https://www.pygame.org/docs/ref/event.html)
