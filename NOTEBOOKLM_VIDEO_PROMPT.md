# NotebookLM Video Overview Prompt — Signal Bloom

Use this prompt with the NotebookLM source document **Signal Bloom — NotebookLM Project Brief**.

> Create a clear, friendly 2–3 minute classroom video overview of the Python school project **Signal Bloom** for classmates and a computer-science teacher. Explain what the player is trying to do, the controls, how collecting twelve orbs opens the center beacon, how a three-charge pulse stuns pursuing drones, how lives and scoring work, and how difficulty increases over time. Then briefly explain the Python ideas visible in the project: the main game loop, event handling, game states, classes for player/drones/orbs, list-based object updates, distance-based collision checks, random variation, and JSON high-score saving with safe error handling.

> Use only facts supported by the source document. Do not invent features, code, assets, online play, or claims about a teacher's grading. Describe the implementation as original project work and say that official Python and Pygame documentation was used to understand library concepts. Keep the explanation student-friendly and technically accurate. Spell the title **Signal Bloom** consistently. Use on-screen labels for the six states: Menu, Instructions, Playing, Paused, Game Over, and Victory. Show the control legend accurately: WASD or arrow keys to move; Space for a pulse when at least three charges are available; P or Esc to pause/resume; Enter to start/restart; H for instructions from the menu or ending screens; Esc to return from instructions; Q or the window close button to quit. End by summarizing the objective and inviting viewers to try to restore the beacon.

## Suggested visual sequence

1. Title card: **Signal Bloom — a Python/Pygame arcade project**.
2. Arena overview: identify the player, green signal orbs, drones, and center beacon.
3. Show the objective: collect twelve orbs, then reach the center.
4. Show controls and the pulse rule: three charges stun nearby drones.
5. Explain lives, points, the completion bonus, and the rising difficulty.
6. Show a simple diagram of the loop: events → update → collisions/scoring → draw.
7. Close with the project concepts, offline requirement (Python plus Pygame), and originality/reference note.

## Narration style

Use a calm, upbeat student-presenter voice. Prefer short sentences, define technical words once, and keep the visuals readable. Avoid rapid cuts, fake gameplay footage, tiny code text, or unsupported claims. If a screenshot or recording of the game is not available as a source, use simple labeled diagrams rather than pretending to show real gameplay.
