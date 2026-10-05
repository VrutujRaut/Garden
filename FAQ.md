# Signal Bloom — Frequently Asked Questions

## About the game

### 1. What is Signal Bloom?
Signal Bloom is an original top-down arcade game written in Python with Pygame. You restore a garden station's beacon while avoiding security drones.

### 2. What is the goal?
Collect 12 green signal orbs, then reach the beacon in the center of the arena.

### 3. How do I move?
Use **W, A, S, D** or the **arrow keys**. Diagonal movement is normalized so it is not faster than straight movement.

### 4. How do I start or restart?
Press **Enter** on the title screen to start. Press **Enter** after a win or game over to begin a fresh run.

### 5. How do I see the instructions?
Press **H** on the title screen or an ending screen. Press **Esc** on the instructions screen to return to the title.

### 6. How do I pause?
Press **P** or **Esc** while playing. Press either key again to resume.

### 7. What does Space do?
Space spends three pulse charges to stun drones near the player for a short time.

### 8. How do I earn pulse charges?
Each collected orb adds one charge. The player can hold at most nine charges.

### 9. How many lives do I get?
You start with three lives. A drone collision removes one life. A brief invulnerability period follows each hit.

### 10. What happens when I lose all my lives?
The run ends and the game-over screen shows your score and best score. Press Enter to restart.

### 11. How does scoring work?
Each orb is worth 100 points, surviving time adds two points per second, and reaching the beacon adds a 500-point completion bonus.

### 12. Does the game get harder?
Yes. Every 22 seconds the drones become faster and arrive more often. The number of active drones also increases, up to a limit.

### 13. Are there different kinds of drones?
Yes. Pink drones pursue directly. Later in the run, some larger amber drones weave as they approach.

### 14. What happens after I collect the twelfth orb?
The center beacon opens. Reach it to win the run.

### 15. Can I keep playing after winning?
The victory screen ends that run. Press Enter to start another one.

### 16. How do I quit?
Press **Q** or close the game window.

## Installation and files

### 17. What do I need to install?
Install Python 3.10 or later and Pygame. Pygame can be installed directly with `py -m pip install pygame` on Windows.

### 18. How do I run the game?
From the project folder, run `py game.py` on Windows, or `python game.py` on systems using the `python` command.

### 19. Does the game need internet access?
No. After Python and Pygame are installed, gameplay is offline. The game does not use a server, online account, API, or cloud service.

### 20. Does it need downloaded artwork or sound files?
No. The visuals use Pygame shapes and particles. Simple sound effects are synthesized by the program; audio is optional if the device cannot initialize it.

### 21. Where is my high score stored?
The best score is stored in `highscore.json` beside `game.py`. Missing, invalid, or unwritable save data will not stop the game from running.

### 22. Why is `highscore.json` not in the public repository?
It is personal playthrough data, so `.gitignore` keeps it on the local computer instead of publishing it.

## Programming and project

### 23. What programming language is used?
The game's implementation is Python. Pygame is the Python library used for the window, keyboard input, drawing, and optional audio.

### 24. Which Python concepts does the game demonstrate?
It uses variables, constants, conditions, loops, functions, classes, lists, random numbers, file handling, exception handling, event handling, and basic geometry.

### 25. What are the main classes?
`Player`, `Drone`, `Orb`, and `Particle` describe game objects. `SignalBloomGame` manages the game states, events, rules, drawing, and main loop.

### 26. What are the game states?
The states are title menu, instructions, playing, paused, game over, and victory.

### 27. How does collision detection work?
The game compares squared distances between circular objects. It only calculates a square root when it needs a direction or normalized movement.

### 28. How is difficulty controlled?
Elapsed time selects a difficulty stage. That stage changes drone speed, spawn interval, and the allowed number of drones, with caps to keep values bounded.

### 29. What does the test file check?
`test_game.py` has 12 automated checks for movement bounds, collecting orbs, pulse behavior, damage, difficulty, pause, restart, victory, score saving/loading, screen drawing, and normal closing.

### 30. Is the project based on a copied game or tutorial?
No. The source code, game rules, and game-specific visuals were developed for this assignment. Official Python and Pygame documentation was used to understand library concepts; see the references in `README.md`.
