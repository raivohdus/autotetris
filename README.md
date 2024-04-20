
## Files

- **game.py**  
  Contains the main game logic for Tetris, including board definition, collision detection, and matrix rotation.

- **game_defs.py**  
  Contains helper functions and constants used in the game, such as board dimensions, matrix rotation, and collision checking.

- **tetris_ai.py**  
  Contains the AI implementation for Tetris, which uses various heuristics to evaluate the board state and determine the best move for the current tetrimino.

- **high_score.txt**  
  Stores the high score for the game.

- **music/**  
  Contains music files used in the game.

- **without_ai/**  
  Contains a version of the Tetris game without the AI implementation.

- **learner/**  
  Contains a version of the Tetris game which can be used to run the genetic algorithm which searches for best possible heuristics. Low performance but gets the job done. Requires patience. :D

## How to Run

1. Install Python 3.
2. Navigate to the project directory (`autotetris`).
3. Install the requirements: `pip install -r requirements.txt`
4. Run the game with AI by executing: `python game.py`
5. Run the game without AI by navigating to the `without_ai` directory and executing: `python game.py`

## AI Heuristics

The AI uses the following heuristics to evaluate the board state:

- **Aggregate Height**: The sum of the height of each column.
- **Complete Lines**: The number of complete lines on the board.
- **Holes**: The number of empty spaces below a block in each column.
- **Bumpiness**: The sum of the absolute differences in heights between adjacent columns.

These heuristics are combined using weights to compute a score for the board, which the AI uses to decide the best move for the current tetrimino. The weights can be adjusted to fine-tune the AI's performance.
