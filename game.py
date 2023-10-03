import pygame
import sys
import random
from tetris import Tetris
from tetris_ai import best_move


pygame.init()
pygame.mixer.init()
tetris_game = Tetris()

# Window size
window_size = (370, 400)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

# Define Tetris pieces, tetris_game.board, and other game variables here



tetrimino_colors = {
    'I': (0, 255, 255),     # Cyan
    'O': (255, 255, 0),     # Yellow
    'T': (128, 0, 128),     # Purple
    'S': (0, 255, 0),       # Green
    'Z': (255, 0, 0),       # Red
    'J': (0, 0, 255),       # Blue
    'L': (255, 165, 0)      # Orange
}

tetris_game.current_tetrimino = None
tetris_game.current_position = (0, 0)  # (x, y) coordinates on the tetris_game.board
tetris_game.next_tetrimino = random.choice(list(tetris_game.tetriminos.keys()))

# Key mechanics



tetris_game.score = 0
# New variable to keep track of total cleared rows
tetris_game.cleared_rows_count = 0

pygame.mixer.music.load('music\\techno-tetris-theme.mp3')
pygame.mixer.music.play(-1)

def draw_next_tetrimino(screen):
    block_size = 20
    x_position = tetris_game.board_width * block_size + 30
    y_position = 160  # Adjusted this from 160 to 180 to ensure there's space for the text

    # Render the "Next Piece:" text and blit it on the screen
    next_piece_text = font.render("Next Piece:", True, (255, 255, 255))
    screen.blit(next_piece_text, (x_position, y_position - 45))  # placing the text 40 units above the tetrimino

    color = tetrimino_colors[tetris_game.next_tetrimino]  # get the color of the next tetrimino
    for y, row in enumerate(tetris_game.tetriminos[tetris_game.next_tetrimino]):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, color, (x_position + x * block_size, y_position + y * block_size, block_size, block_size))

def draw_next_tetrimino_boundaries(screen):
    block_size = 20
    x_position = tetris_game.board_width * block_size + 30
    y_position = 160
    width = max([len(row) for row in tetris_game.tetriminos[tetris_game.next_tetrimino]]) * block_size
    height = len(tetris_game.tetriminos[tetris_game.next_tetrimino]) * block_size

    # Draw the boundaries
    pygame.draw.rect(screen, (255, 255, 255), (x_position - 5, y_position - 25, width + 10, height + 30), 2)

#Draw Static blocks (optional for AI)
def draw_board(screen):
    for y, row in enumerate(tetris_game.board):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, (255, 255, 255), (x*20, y*20, 20, 20))

# Drawing functions (optional for AI)
def draw_tetrimino(screen, position, tetrimino):
    block_size = 20
    color = tetrimino_colors[tetris_game.current_tetrimino]  # get the color of the current tetrimino
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
    score_text = font.render(f"Score: {tetris_game.score}", True, (255, 255, 255))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    difficulty_level = base_gravity_timer_threshold - adjusted_gravity_timer_threshold
    difficulty_text = font.render(f"Difficulty Level: {difficulty_level}", True, (255, 255, 255))

    x_position = tetris_game.board_width * 20 + 10  # Slightly reduced padding

    # Adjusted vertical positioning for score, high score, and difficulty level
    screen.blit(score_text, (x_position, 30))
    screen.blit(high_score_text, (x_position, 60))
    screen.blit(difficulty_text, (x_position, 90))

def draw_boundaries(screen):
    block_size = 20
    top_left = (0, 0)
    top_right = (tetris_game.board_width * block_size, 0)
    bottom_left = (0, tetris_game.board_height * block_size)
    bottom_right = (tetris_game.board_width * block_size, tetris_game.board_height * block_size)

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
tetris_game.spawn_new_tetrimino()

running = True
ai_move_made = False  # A flag to ensure the AI makes one move per tetrimino

# AI plays:  
  
try:  
    while running:  
        # Always service the event loop  
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                running = False  
  
        if not ai_move_made:  
            x_position, rotation = best_move(tetris_game.board, tetris_game.tetriminos[tetris_game.current_tetrimino])  
  
            # Apply the AI's suggested x-position    
            while tetris_game.current_position[0] < x_position:    
                tetris_game.move_piece(1, 0, ignore_collision=True)    
            while tetris_game.current_position[0] > x_position:    
                tetris_game.move_piece(-1, 0, ignore_collision=True)    
              
            # Apply the AI's suggested rotation  
            for _ in range(rotation):  
                tetris_game.rotate_piece()  
              
            ai_move_made = True  
  
        gravity_timer += 1  
        adjusted_gravity_timer_threshold = base_gravity_timer_threshold - tetris_game.cleared_rows_count  # Decrement the threshold by the tetris_game.cleared_rows_count  
        adjusted_gravity_timer_threshold = max(0.05, adjusted_gravity_timer_threshold)  # Set a minimum limit so it doesn't become too fast  
  
        # Update the high score if needed  
        if tetris_game.score > high_score:  
            high_score = tetris_game.score  
            save_high_score(high_score)  
  
  
        if gravity_timer > adjusted_gravity_timer_threshold:  
            game_status = tetris_game.move_piece(0, 1)  
            if game_status is not None:  
                if game_status:  
                    ai_move_made = False  
                else:  
                    running = False  
                    display_game_over(screen)  
            gravity_timer = 0  




        screen.fill((0, 0, 0))  
        draw_board(screen)  
        draw_tetrimino(screen, tetris_game.current_position, tetris_game.tetriminos[tetris_game.current_tetrimino])  
        draw_score(screen)  
        draw_boundaries(screen)  
        draw_next_tetrimino(screen)  
        draw_next_tetrimino_boundaries(screen)  
  
        pygame.display.flip()  
        clock.tick(60)  
  
except Exception as e:  
    print(f"Error occurred: {e}")  
    # Optionally, print the current tetris_game.board state or any other relevant information here  

pygame.quit()
sys.exit()
