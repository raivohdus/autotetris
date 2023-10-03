# Board
board_width = 10
board_height = 20
board = [[0 for _ in range(board_width)] for _ in range(board_height)]

def rotate_matrix(matrix):
    # Return the rotated matrix
    return [ [ matrix[y][x]
            for y in range(len(matrix)) ]
            for x in range(len(matrix[0]) - 1, -1, -1) ]

def check_collision(x, y, piece):
    for i, row in enumerate(piece):
        for j, cell in enumerate(row):
            if cell:
                if x + j < 0 or x + j >= board_width or \
                   y + i < 0 or y + i >= board_height or \
                   board[y + i][x + j] != 0:
                    return True
    return False