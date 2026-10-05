# Development specification — Signal Bloom

1. **Concept:** A compact top-down arcade game about restoring a beacon in a damaged garden station while evading security drones.
2. **Core loop:** Move through the arena, collect signal orbs to restore the beacon and charge a pulse, stun nearby drones with the pulse, and reach the beacon after collecting enough orbs. Drones become faster and more numerous over time.
3. **Controls:** WASD or arrow keys to move; Space to use a charged pulse; P or Esc to pause; Enter to confirm/start/restart; H for help; Esc to return from help.
4. **Game states:** Main menu, instructions, playing, paused, game over, victory.
5. **Entities:** Player, pursuing drones, signal orbs, visual particles, and the exit beacon.
6. **Collision system:** Pygame rectangles/circles and squared-distance checks for orb pickup, drone contact, pulse radius, and beacon arrival.
7. **Scoring:** Orbs add points; surviving time adds a small bonus. Best score is retained locally.
8. **Difficulty:** Drone spawn interval and movement speed increase in timed stages, with a cap to keep the game manageable.
9. **Save system:** `highscore.json` beside the Python file, read/written with `json` and `pathlib`; invalid or missing data falls back safely.
10. **Dependencies:** Python 3 and Pygame. Sound effects are synthesized at runtime and degrade gracefully if audio is unavailable.
11. **File structure:** `game.py` contains the understandable game implementation; `requirements.txt` lists Pygame; `README.md` explains setup, rules, concepts, and verification; `DESIGN_SPEC.md` records this development plan.
