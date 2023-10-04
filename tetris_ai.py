#Hello tetris_ai.py
from tetris import Tetris

def rotate_matrix(matrix):  
    return [[matrix[y][x]  
            for y in range(len(matrix))]  
            for x in range(len(matrix[0]) - 1, -1, -1)]

def check_collision(x, y, piece, board):  
    for i, row in enumerate(piece):  
        for j, cell in enumerate(row):  
            if cell:  
                if x + j < 0 or x + j >= len(board[0]) or \
                   y + i < 0 or y + i >= len(board) or \
                   board[y + i][x + j] != 0:
                    return True  
    return False  


def aggregate_height(board):
    height_sum = 0
    for col in range(len(board[0])):
        for row in range(len(board)):
            if board[row][col] == 1:  # Found a block in the column
                height_sum += len(board) - row  # Height is counted from the bottom
                break
    return height_sum

def complete_lines(board):
    # Compute and return the number of complete lines in the board.
    return sum(1 for row in board if all(cell == 1 for cell in row))

def holes(board):
    # Compute and return the number of holes in the board.
    hole_count = 0
    for col in range(len(board[0])):
        block_found = False
        for row in range(len(board)):
            if board[row][col] == 1:
                block_found = True
            elif block_found and board[row][col] == 0:  # Empty space below a block
                hole_count += 1
    return hole_count

def bumpiness(board):
    # Compute and return the bumpiness of the board.
    column_heights = []
    for col in range(len(board[0])):
        for row in range(len(board)):
            if board[row][col] == 1:
                column_heights.append(len(board) - row)
                break
        else:
            column_heights.append(0)
    
    bumpiness_sum = sum(abs(column_heights[i] - column_heights[i+1]) for i in range(len(column_heights)-1))
    return bumpiness_sum

def evaluate_board(board):
    # Use the heuristics to compute a score for the board.
    a, b, c, d = -0.5, 0.75, -0.35, -0.18  # Example weights, can be adjusted
    return a * aggregate_height(board) + b * complete_lines(board) + c * holes(board) + d * bumpiness(board)

def best_move(board, tetrimino):  
    # Evaluate all possible moves of the tetrimino on the board.  
    # Return the best rotation and position (x-coordinate) for the tetrimino.  
    best_score = float('-inf')  # Start with the worst possible score  
    best_position = (0, 0)  # (x, rotation)  
    rotations = [tetrimino]  # Starting rotation  
  
    # Generate all possible rotations of the tetrimino  
    for _ in range(3):  
        rotations.append(rotate_matrix(rotations[-1]))
  
    for rotation_index, rotated_tetrimino in enumerate(rotations):  
        for x in range(len(board[0]) - len(rotated_tetrimino[0]) + 1):  # Ensure tetrimino fits within board width  
            temp_board = [row[:] for row in board]  # Deep copy of the board  
  
            # Check if the move is valid before proceeding  
            y = 0  
            if check_collision(x, y, rotated_tetrimino, board):  
                continue
              
            # Find the drop position for the tetrimino  
            while not check_collision(x, y + 1, rotated_tetrimino, board):
                y += 1  
  
            # Place the tetrimino on the temp board  
            for i, row in enumerate(rotated_tetrimino):  
                for j, cell in enumerate(row):  
                    if cell:  
                        temp_board[y + i][x + j] = 1  
  
            # Evaluate the board state  
            score = evaluate_board(temp_board)  
            if score > best_score:  
                best_score = score  
                best_position = (x, rotation_index)  

    print ("best position: ", best_position)
    return best_position

if __name__ == "__main__":
    # Mock board with a hole and bumpiness
    mock_board_1 = [
        [0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 0, 0, 1, 1],
    ] + [[0] * 10 for _ in range(16)]  # Fill the rest with empty rows

    print("Testing mock_board_1:")
    print("Aggregate Height:", aggregate_height(mock_board_1))
    print("Complete Lines:", complete_lines(mock_board_1))
    print("Holes:", holes(mock_board_1))
    print("Bumpiness:", bumpiness(mock_board_1))
    print("Board Evaluation:", evaluate_board(mock_board_1))
    print()

    # Add more mock boards as needed and repeat the above testing pattern.
    mock_board_2 = [
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ] + [[0] * 10 for _ in range(16)]  # Fill the rest with empty rows

    print("Testing mock_board_2:")
    print("Aggregate Height:", aggregate_height(mock_board_2))
    print("Complete Lines:", complete_lines(mock_board_2))
    print("Holes:", holes(mock_board_2))
    print("Bumpiness:", bumpiness(mock_board_2))
    print("Board Evaluation:", evaluate_board(mock_board_2))
    print()
