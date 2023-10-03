import pygame
import sys
import random
from tetris_ai import best_move
from game_defs import rotate_matrix
from game_defs import check_collision
from game_defs import board_height
from game_defs import board_width
from game_defs import board
#from game_defs import extra_rows

pygame.init()
pygame.mixer.init()

# Window size
window_size = (370, 400)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

# Define Tetris pieces, board, and other game variables here

tetriminos = {
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

tetrimino_colors = {
    'I': (0, 255, 255),     # Cyan
    'O': (255, 255, 0),     # Yellow
    'T': (128, 0, 128),     # Purple
    'S': (0, 255, 0),       # Green
    'Z': (255, 0, 0),       # Red
    'J': (0, 0, 255),       # Blue
    'L': (255, 165, 0)      # Orange
}

current_tetrimino = None
current_position = (0, 0)  # (x, y) coordinates on the board
next_tetrimino = random.choice(list(tetriminos.keys()))

# Key mechanics

def move_piece(dx, dy, ignore_collision=False):  
    global current_position  
  
    # Compute the new position  
    new_x = current_position[0] + dx  
    new_y = current_position[1] + dy  
  
    # Check if the move is valid  
    if not check_collision(new_x, new_y, tetriminos[current_tetrimino]) or ignore_collision:  
        current_position = (new_x, new_y)  
    else:  
        if dy == 1:  # If it's a downwards move and there's a collision  
            #print(f"Illegal downward move attempted at position {current_position} with tetrimino {current_tetrimino}")
            place_piece()
            clear_lines()
            if not spawn_new_tetrimino():
                display_game_over(screen)
                pygame.mixer.music.stop()
                return False  # Game over
            return True  # Tetrimino was placed
        #else:
        #    print(f"Illegal move attempted at position {current_position} with direction (dx={dx}, dy={dy}) and tetrimino {current_tetrimino}")
    return False  # Tetrimino was not placed


def rotate_piece():
    global current_tetrimino

    # Rotate the tetrimino
    rotated = rotate_matrix(tetriminos[current_tetrimino])

    if not check_collision(current_position[0], current_position[1], rotated):
        tetriminos[current_tetrimino] = rotated
    #else:
    #    print(f"Illegal rotation attempted at position {current_position} with tetrimino {current_tetrimino}")


def place_piece():
    global board

    for i, row in enumerate(tetriminos[current_tetrimino]):
        for j, cell in enumerate(row):
            if cell:
                board[current_position[1] + i][current_position[0] + j] = 1

def hard_drop():
    global current_position
    dy = 1
    while not check_collision(current_position[0], current_position[1] + dy, tetriminos[current_tetrimino]):
        dy += 1
    move_piece(0, dy - 1)  # Move the tetrimino down by dy - 1 units

score = 0
# New variable to keep track of total cleared rows
cleared_rows_count = 0

def clear_lines():
    global board, score, cleared_rows_count

    lines_cleared = 0
    lines_to_clear = [i for i, row in enumerate(board) if all(cell != 0 for cell in row)]
    lines_cleared += len(lines_to_clear)
    cleared_rows_count += lines_cleared  # Increase the cleared rows count

    for i in lines_to_clear:
        del board[i]
        board.insert(0, [0 for _ in range(board_width)])

    # Implementing scoring multiplier
    multiplier = lines_cleared ** 2  # n^2 multiplier
    score += lines_cleared * 100 * multiplier  # score for clearing n lines = n^2 * 100

# Spawn Tetrimino and check immediately for collision
def spawn_new_tetrimino():
    global current_tetrimino, next_tetrimino, current_position
    current_tetrimino = next_tetrimino  # Set the current tetrimino to the next one
    next_tetrimino = random.choice(list(tetriminos.keys()))  # Select a new next tetrimino
    current_position = (board_width // 2, 0)
    if check_collision(current_position[0], current_position[1], tetriminos[current_tetrimino]):
        return False  # Game over
    return True

pygame.mixer.music.load('D:\\code\\AI\\tetris2\\music\\techno-tetris-theme.mp3')
pygame.mixer.music.play(-1)

def draw_next_tetrimino(screen):
    block_size = 20
    x_position = board_width * block_size + 30
    y_position = 160  # Adjusted this from 160 to 180 to ensure there's space for the text

    # Render the "Next Piece:" text and blit it on the screen
    next_piece_text = font.render("Next Piece:", True, (255, 255, 255))
    screen.blit(next_piece_text, (x_position, y_position - 45))  # placing the text 40 units above the tetrimino

    color = tetrimino_colors[next_tetrimino]  # get the color of the next tetrimino
    for y, row in enumerate(tetriminos[next_tetrimino]):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, color, (x_position + x * block_size, y_position + y * block_size, block_size, block_size))

def draw_next_tetrimino_boundaries(screen):
    block_size = 20
    x_position = board_width * block_size + 30
    y_position = 160
    width = max([len(row) for row in tetriminos[next_tetrimino]]) * block_size
    height = len(tetriminos[next_tetrimino]) * block_size

    # Draw the boundaries
    pygame.draw.rect(screen, (255, 255, 255), (x_position - 5, y_position - 25, width + 10, height + 30), 2)

#Draw Static blocks (optional for AI)
def draw_board(screen):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, (255, 255, 255), (x*20, y*20, 20, 20))

# Drawing functions (optional for AI)
def draw_tetrimino(screen, position, tetrimino):
    block_size = 20
    color = tetrimino_colors[current_tetrimino]  # get the color of the current tetrimino
    for y, row in enumerate(tetrimino):
        for x, cell in enumerate(row):
            if cell:  
                pygame.draw.rect(screen, color, (position[0] * block_size + x * block_size, position[1] * block_size + y * block_size, block_size, block_size))

font = pygame.font.SysFont(None, 24)  # Define this outside your main loop, preferably near the top of your code

def display_game_over(screen):
    game_over_text = font.render("Game Over", True, (255, 0, 0))  # Red text for "Game Over"
    screen.blit(game_over_text, (window_size[0] // 2 - game_over_text.get_width() // 2, window_size[1] // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)  # Wait for 2 seconds

def draw_score(screen):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    difficulty_level = base_gravity_timer_threshold - adjusted_gravity_timer_threshold
    difficulty_text = font.render(f"Difficulty Level: {difficulty_level}", True, (255, 255, 255))

    x_position = board_width * 20 + 10  # Slightly reduced padding

    # Adjusted vertical positioning for score, high score, and difficulty level
    screen.blit(score_text, (x_position, 30))
    screen.blit(high_score_text, (x_position, 60))
    screen.blit(difficulty_text, (x_position, 90))

def draw_boundaries(screen):
    block_size = 20
    top_left = (0, 0)
    top_right = (board_width * block_size, 0)
    bottom_left = (0, board_height * block_size)
    bottom_right = (board_width * block_size, board_height * block_size)

    pygame.draw.line(screen, (255, 255, 255), top_left, top_right)
    pygame.draw.line(screen, (255, 255, 255), bottom_left, bottom_right)
    pygame.draw.line(screen, (255, 255, 255), top_left, bottom_left)
    pygame.draw.line(screen, (255, 255, 255), top_right, bottom_right)

def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.readline())
    except (FileNotFoundError, ValueError):
        return 0

def save_high_score(new_high_score):
    with open("high_score.txt", "w") as file:
        file.write(str(new_high_score))

# Game loop
base_gravity_timer_threshold = 0.3  # initial value for the gravity timer threshold
gravity_timer = 0
high_score = load_high_score()
spawn_new_tetrimino()

running = True
ai_move_made = False  # A flag to ensure the AI makes one move per tetrimino

# AI plays:

try:
    while running:
        # Always service the event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Uncomment below if you want to allow manual control
            #elif event.type == pygame.KEYDOWN:
                #if event.key == pygame.K_LEFT:
                #    move_piece(-1, 0)  # Move left
                #elif event.key == pygame.K_RIGHT:
                #    move_piece(1, 0)  # Move right
                #elif event.key == pygame.K_DOWN:
                #    move_piece(0, 1)  # Move down
                #elif event.key == pygame.K_UP:
                #    rotate_piece()
                #elif event.key == pygame.K_SPACE:
                #    hard_drop()
        #print("AI move started")
        if not ai_move_made:
            x_position, rotation = best_move(board, tetriminos[current_tetrimino])
            
            # Apply the AI's suggested x-position  
            while current_position[0] < x_position:  
                move_piece(1, 0, ignore_collision=True)  
            while current_position[0] > x_position:  
                move_piece(-1, 0, ignore_collision=True)  
            
            # Apply the AI's suggested rotation
            for _ in range(rotation):
                rotate_piece()
            
            ai_move_made = True
        #print("AI move completed")

        gravity_timer += 1
        adjusted_gravity_timer_threshold = base_gravity_timer_threshold - cleared_rows_count  # Decrement the threshold by the cleared_rows_count
        adjusted_gravity_timer_threshold = max(0.05, adjusted_gravity_timer_threshold)  # Set a minimum limit so it doesn't become too fast

        # Update the high score if needed
        if score > high_score:
            high_score = score
            save_high_score(high_score)

        #print("Gravity timer:", gravity_timer)
        if gravity_timer > adjusted_gravity_timer_threshold:
            #print("Gravity tick")
            tetrimino_placed = move_piece(0, 1)
            if tetrimino_placed:
                ai_move_made = False
            elif not running:
                running = False
            gravity_timer = 0


        #print("Drawing to screen")
        screen.fill((0, 0, 0))
        draw_board(screen)
        draw_tetrimino(screen, current_position, tetriminos[current_tetrimino])
        draw_score(screen)
        draw_boundaries(screen)
        draw_next_tetrimino(screen)
        draw_next_tetrimino_boundaries(screen)

        pygame.display.flip()
        clock.tick(60)

except Exception as e:
    print(f"Error occurred: {e}")
    # Optionally, print the current board state or any other relevant information here

pygame.quit()
sys.exit()
