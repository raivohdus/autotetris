#tetris.py
import random

class Tetris:  
    def __init__(self, board_width=10, board_height=20):  
        self.board_width = board_width  
        self.board_height = board_height  
        self.board = [[0 for _ in range(board_width)] for _ in range(board_height)]  
        self.current_tetrimino = None  
        self.current_position = (0, 0)  
  
        self.tetriminos = {  
            'I': [  
                [1, 1, 1, 1]  
            ],  
            'O': [  
                [1, 1],  
                [1, 1]  
            ],  
            'T': [  
                [0, 1, 0],  
                [1, 1, 1]  
            ],  
            'S': [  
                [0, 1, 1],  
                [1, 1, 0]  
            ],  
            'Z': [  
                [1, 1, 0],  
                [0, 1, 1]  
            ],  
            'J': [  
                [1, 0, 0],  
                [1, 1, 1]  
            ],  
            'L': [  
                [0, 0, 1],  
                [1, 1, 1]  
            ]  
        }  
  
        self.next_tetrimino = random.choice(list(self.tetriminos.keys()))  

        self.cleared_rows_count = 0  # Keep this line  
        self.score = 0  # Add this line    
  
    def check_collision(self, x, y, piece):  
        for i, row in enumerate(piece):  
            for j, cell in enumerate(row):  
                if cell:  
                    if x + j < 0 or x + j >= self.board_width or \
                       y + i < 0 or y + i >= self.board_height or \
                       self.board[y + i][x + j] != 0:
                        return True
        return False

    def rotate_matrix(self, matrix):  
        # Return the rotated matrix  
        return [[matrix[y][x]  
                for y in range(len(matrix))]  
                for x in range(len(matrix[0]) - 1, -1, -1)]  
  
    def check_collision(self, x, y, piece):  
        for i, row in enumerate(piece):  
            for j, cell in enumerate(row):  
                if cell:  
                    if x + j < 0 or x + j >= self.board_width or \
                       y + i < 0 or y + i >= self.board_height or \
                       self.board[y + i][x + j] != 0:
                        return True
        return False
  
    # Add other game methods (e.g., move_piece, rotate_piece, etc.) as class methods  
    def move_piece(self, dx, dy, ignore_collision=False):  
        # Compute the new position      
        new_x = self.current_position[0] + dx      
        new_y = self.current_position[1] + dy      
            
        # Check if the move is valid      
        if not self.check_collision(new_x, new_y, self.tetriminos[self.current_tetrimino]) or ignore_collision:      
            self.current_position = (new_x, new_y)      
        else:      
            #print(f"Illegal move attempted at position ({new_x}, {new_y}) with tetrimino {self.current_tetrimino}")  # Debugging printout
            if dy == 1:  # If it's a downwards move and there's a collision      
                self.place_piece()    
                self.clear_lines()    
                if not self.spawn_new_tetrimino():    
                    return False  # Game over  
                #print(f"Tetrimino placed at position ({new_x}, {new_y}) with tetrimino {self.current_tetrimino}")  # Debugging printout
                return True  # Tetrimino was placed    
        return None  # Tetrimino was not placed, game continues  

    def rotate_piece(self):
        # Rotate the tetrimino
        rotated = self.rotate_matrix(self.tetriminos[self.current_tetrimino])

        if not self.check_collision(self.current_position[0], self.current_position[1], rotated):
            self.tetriminos[self.current_tetrimino] = rotated
        else:
            print(f"Illegal rotation attempted at position {self.current_position} with tetrimino {self.current_tetrimino}")

    def place_piece(self):  
        for i, row in enumerate(self.tetriminos[self.current_tetrimino]):  
            for j, cell in enumerate(row):  
                if cell:  
                    if 0 <= self.current_position[1] + i < self.board_height and 0 <= self.current_position[0] + j < self.board_width:  
                        self.board[self.current_position[1] + i][self.current_position[0] + j] = 1  

    def clear_lines(self):

        lines_cleared = 0
        lines_to_clear = [i for i, row in enumerate(self.board) if all(cell != 0 for cell in row)]
        lines_cleared += len(lines_to_clear)
        self.cleared_rows_count += lines_cleared  # Increase the cleared rows count

        for i in lines_to_clear:
            del self.board[i]
            self.board.insert(0, [0 for _ in range(self.board_width)])

        # Print score and cleared lines whenever a line is cleared  
        if lines_cleared > 0:  
            print(f"Score: {self.score}, Cleared lines: {self.cleared_rows_count}") 

        # Implementing scoring multiplier
        multiplier = lines_cleared ** 2  # n^2 multiplier
        self.score += lines_cleared * 100 * multiplier  # score for clearing n lines = n^2 * 100

    def spawn_new_tetrimino(self):  
        self.current_tetrimino = self.next_tetrimino  
        self.current_position = (self.board_width // 2 - 1, 0)  
        self.next_tetrimino = random.choice(list(self.tetriminos.keys()))  
    
        # Check for collision immediately after spawning a new Tetrimino  
        if self.check_collision(self.current_position[0], self.current_position[1], self.tetriminos[self.current_tetrimino]):  
            return False  # Game over  
    
        return True  
