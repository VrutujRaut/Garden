# Redstone Run — Frequently Asked Questions

1. **What is the objective?** Mine four redstone and two iron, craft a beacon core at the workbench, then step onto the portal.
2. **How do I move?** Use WASD or the arrow keys. Movement advances one tile at a time.
3. **How do I mine?** Stand beside a colored ore block and press F or Space.
4. **How do I craft?** Stand beside the brown workbench and press E. The recipe is four redstone and two iron.
5. **What does coal do?** Coal is optional and gives bonus score when mined.
6. **What happens if I reach the portal without a core?** The portal remains inactive and the game displays a reminder.
7. **How many hearts do I have?** Three. A slime collision takes one heart.
8. **Can I take repeated damage instantly?** No. A short invulnerability timer follows a hit.
9. **How do I pause?** Press Esc while playing. Press Esc or Enter to resume.
10. **How do I restart?** Press Enter after winning or losing.
11. **How do I see the controls?** Press H on the title screen.
12. **How do I quit?** Press Q or close the game window.
13. **What makes the slimes dangerous?** They take steps toward the player and gradually move more quickly as the run continues.
14. **How does the map work?** It is a two-dimensional list of rows, with a one-character code for each tile.
15. **Where are lists used?** The tile map and collections of entities use lists, which the program traverses with loops.
16. **Where are dictionaries used?** The inventory stores item counts by name, and the crafting recipe stores material requirements.
17. **Which Python topics appear?** Variables, data types, operators, conditions, loops, lists, dictionaries, functions/methods, classes, file handling, and exceptions.
18. **How is the high score saved?** A small JSON object is read from and written to `redstone_best.json` beside `game.py`.
19. **Will a missing or corrupt score file crash the game?** No. Loading errors safely fall back to a best score of zero.
20. **Are the graphics separate image files?** No. All game visuals are drawn from Python with Pygame shapes and lines.
21. **Does it need internet while playing?** No. Internet is only needed to install Pygame if it is not already installed.
22. **What packages are required?** Python and Pygame. See `requirements.txt`.
23. **How do I install the dependency?** Run `python -m pip install -r requirements.txt` or, on many Windows systems, `py -m pip install -r requirements.txt`.
24. **How do I run it?** Run `python game.py` (or `py game.py` on Windows) from the project folder.
25. **Is the game a full Minecraft clone?** No. It is an original, small block-world adventure inspired by mining and crafting ideas. It has its own code, map, characters, and visuals.
26. **Is this affiliated with Mojang or Microsoft?** No. Minecraft is a trademark of its respective owner; this student project is unofficial.
27. **Is the whole CBSE IP syllabus represented?** No. The game illustrates selected Python programming ideas. It does not cover all computer-system, database/SQL, and emerging-trend topics.
28. **How can I run the checks?** Run `python -m unittest -v` after installing Pygame.
29. **What should I explain in an evaluation?** Explain how the grid list stores tiles, how movement checks walls, how the inventory and recipe dictionaries work, and how the loop updates and draws the game.
30. **Where did the syllabus mapping come from?** The official CBSE Class XI IP syllabus for 2026–27 was consulted, alongside official Python and Pygame documentation. Links are in `README.md`.
