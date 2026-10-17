# Development specification — Redstone Run

1. **Concept:** An original, compact 2D block-world cave adventure. The player mines ore, crafts a beacon core, and escapes through a portal while avoiding cave slimes.
2. **Core loop:** Explore a small tile map → mine nearby ore → collect the recipe materials → visit the workbench → craft the core → reach the portal.
3. **Controls:** WASD/arrow keys move one tile; F or Space mines an adjacent ore block; E crafts beside the workbench; Esc pauses/resumes; Enter starts/restarts; H opens help; Q exits.
4. **States:** Menu, help, playing, paused, game over, and victory.
5. **Entities:** Explorer, cave slimes, tile world, workbench, ore veins, and the portal.
6. **Collision and movement:** The explorer and slimes move on grid coordinates. A movement is accepted only if the destination tile is inside the map and is not a wall. Slime contact costs one heart and grants a brief invulnerability window.
7. **Scoring and failure:** Mineable ore adds points, crafting adds a bonus, and a quick escape adds a time bonus. Three hearts are available; losing them ends the run. The best score is saved locally.
8. **Progression:** The route passes rocky shelves, ore types have distinct values, and slimes shorten their step interval as the run continues.
9. **Save system:** `redstone_best.json` stores a single best-score value using `json` and `pathlib`. Missing or corrupt data is handled safely.
10. **Dependencies:** Python 3 and Pygame. All graphics are drawn from original code using Pygame shapes; no image or sound files are needed.
11. **File structure:** `game.py` contains the game, `test_game.py` checks core rules, `requirements.txt` lists Pygame, and `README.md`, `FAQ.md`, and the NotebookLM files explain the project.

## Class XI IP connections

- Tile rows and active slimes use **lists** and iteration.
- The inventory and recipe use **dictionaries** with key/value pairs.
- **Variables, data types, arithmetic, comparisons, and Boolean conditions** control score, movement, crafting, health, and state changes.
- Small methods organize the program into explainable **functions**; classes model the explorer, slimes, and game.
- **JSON file handling** stores the best score, and exception handling protects startup from missing or malformed data.
- Original pixel-style visuals are drawn from code rather than downloaded assets.

The game demonstrates Python programming topics from CBSE Class XI Informatics Practices. It is not presented as a complete demonstration of the syllabus units on computer systems, relational databases/SQL, or emerging trends.
