#tetris_ai.py
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

def wells(board):  
    well_depth = 0  
    column_heights = []  
  
    # Calculate the height of each column  
    for col in range(len(board[0])):  
        for row in range(len(board)):  
            if board[row][col] == 1:  
                column_heights.append(len(board) - row)  
                break  
        else:  
            column_heights.append(0)  
  
    # Calculate the well depth  
    for i in range(1, len(column_heights) - 1):  
        left_diff = column_heights[i - 1] - column_heights[i]  
        right_diff = column_heights[i + 1] - column_heights[i]  
  
        if left_diff > 1:  
            well_depth += left_diff - 1  
        if right_diff > 1:  
            well_depth += right_diff - 1  
  
    return well_depth  


def evaluate_board(board, heuristics):  
    # Use the heuristics to compute a score for the board.  
    a, b, c, d, e = heuristics  # Use the provided heuristics instead of hardcoded weights  
    return a * aggregate_height(board) + b * complete_lines(board) + c * holes(board) + d * bumpiness(board) + e * wells(board)  

def best_move(board, current_tetrimino, next_tetrimino, heuristics):  
    best_score = float('-inf')  # Start with the worst possible score  
    best_position = (0, 0)  # (x, rotation)  
  
    # Get all possible moves for the current tetrimino  
    for curr_x, curr_rotation in possible_moves(board, current_tetrimino):  
        temp_board = place_tetrimino(board, current_tetrimino, curr_x, curr_rotation)  
  
        next_possible_moves = [evaluate_board(place_tetrimino(temp_board, next_tetrimino, next_x, next_rotation), heuristics)  
            for next_x, next_rotation in possible_moves(temp_board, next_tetrimino)]  
        
        next_best_score = max(next_possible_moves) if next_possible_moves else float('-inf')  
  
        # Combine scores  
        combined_score = evaluate_board(temp_board, heuristics) + next_best_score  
  
        if combined_score > best_score:  
            best_score = combined_score  
            best_position = (curr_x, curr_rotation)  
  
    return best_position  



def possible_moves(board, tetrimino):
    # This function returns all possible (x, rotation) for the given tetrimino on the board
    possible_positions = []

    rotations = [tetrimino]  # Starting rotation
    for _ in range(3):  # Generate all possible rotations of the tetrimino
        rotations.append(rotate_matrix(rotations[-1]))

    for rotation_index, rotated_tetrimino in enumerate(rotations):
        for x in range(len(board[0]) - len(rotated_tetrimino[0]) + 1):  # Ensure tetrimino fits within board width
            y = 0
            if check_collision(x, y, rotated_tetrimino, board):
                continue
            possible_positions.append((x, rotation_index))

    return possible_positions

def place_tetrimino(board, tetrimino, x, rotation):
    # This function places the tetrimino on the board and returns the resultant board
    temp_board = [row[:] for row in board]  # Deep copy of the board

    rotated_tetrimino = tetrimino
    for _ in range(rotation):  # Apply rotation
        rotated_tetrimino = rotate_matrix(rotated_tetrimino)

    y = 0  # Find the drop position for the tetrimino
    while not check_collision(x, y + 1, rotated_tetrimino, board):
        y += 1

    # Place the tetrimino on the temp board
    for i, row in enumerate(rotated_tetrimino):
        for j, cell in enumerate(row):
            if cell:
                temp_board[y + i][x + j] = 1

    return temp_board

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