import pygame  
import sys  
import random  
import os  
from tetris_ai import best_move  
from game_defs import rotate_matrix  
from game_defs import check_collision  
from game_defs import board_height  
from game_defs import board_width  
from game_defs import board  
  
pygame.init()  
pygame.mixer.init()  
  
window_size = (370, 400)  
screen = pygame.display.set_mode(window_size)  
pygame.display.set_caption("Tetris")  
  
clock = pygame.time.Clock()  
  
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
  
def move_piece(dx, dy, ignore_collision=False):    
    global current_position    
    
    new_x = current_position[0] + dx    
    new_y = current_position[1] + dy    
    
    if not check_collision(new_x, new_y, tetriminos[current_tetrimino]) or ignore_collision:    
        current_position = (new_x, new_y)    
    else:    
        if dy == 1:  
            place_piece()  
            clear_lines()  
            if not spawn_new_tetrimino():  
                display_game_over(screen)  
                pygame.mixer.music.stop()  
                return False  # Game over  
            return True  # Tetrimino was placed  
    return False  # Tetrimino was not placed  
  
def rotate_piece():  
    global current_tetrimino  
  
    rotated = rotate_matrix(tetriminos[current_tetrimino])  
  
    if not check_collision(current_position[0], current_position[1], rotated):  
        tetriminos[current_tetrimino] = rotated  
  
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
cleared_rows_count = 0  
  
def clear_lines():  
    global board, score, cleared_rows_count  
  
    lines_cleared = 0  
    lines_to_clear = [i for i, row in enumerate(board) if all(cell != 0 for cell in row)]  
    lines_cleared += len(lines_to_clear)  
    cleared_rows_count += lines_cleared  
  
    for i in lines_to_clear:  
        del board[i]  
        board.insert(0, [0 for _ in range(board_width)])  
  
    multiplier = lines_cleared ** 2  
    score += lines_cleared * 100 * multiplier  
  
def spawn_new_tetrimino():  
    global current_tetrimino, next_tetrimino, current_position  
    current_tetrimino = next_tetrimino  
    next_tetrimino = random.choice(list(tetriminos.keys()))  
    current_position = (board_width // 2, 0)  
    if check_collision(current_position[0], current_position[1], tetriminos[current_tetrimino]):  
        return False  # Game over  
    return True  
  
script_dir = os.path.dirname(os.path.abspath(__file__))  
music_file = os.path.join(script_dir, 'music', 'techno-tetris-theme.mp3')  
pygame.mixer.music.load(music_file)  
pygame.mixer.music.play(-1)  
  
def draw_next_tetrimino(screen):  
    block_size = 20  
    x_position = board_width * block_size + 30  
    y_position = 160  
  
    next_piece_text = font.render("Next Piece:", True, (255, 255, 255))  
    screen.blit(next_piece_text, (x_position, y_position - 45))  
  
    color = tetrimino_colors[next_tetrimino]  
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
  
    pygame.draw.rect(screen, (255, 255, 255), (x_position - 5, y_position - 25, width + 10, height + 30), 2)  
  
def draw_board(screen):  
    for y, row in enumerate(board):  
        for x, cell in enumerate(row):  
            if cell:  
                pygame.draw.rect(screen, (255, 255, 255), (x*20, y*20, 20, 20))  
  
def draw_tetrimino(screen, position, tetrimino):  
    block_size = 20  
    color = tetrimino_colors[current_tetrimino]  
    for y, row in enumerate(tetrimino):  
        for x, cell in enumerate(row):  
            if cell:    
                pygame.draw.rect(screen, color, (position[0] * block_size + x * block_size, position[1] * block_size + y * block_size, block_size, block_size))  
  
font = pygame.font.SysFont(None, 24)  
  
def display_game_over(screen):  
    game_over_text = font.render("Game Over", True, (255, 0, 0))  
    screen.blit(game_over_text, (window_size[0] // 2 - game_over_text.get_width() // 2, window_size[1] // 2 - game_over_text.get_height() // 2))  
    pygame.display.flip()  
    pygame.time.wait(2000)  
  
def draw_score(screen):  
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))  
    difficulty_level = base_gravity_timer_threshold - adjusted_gravity_timer_threshold  
    difficulty_text = font.render(f"Difficulty Level: {difficulty_level}", True, (255, 255, 255))  
  
    x_position = board_width * 20 + 10  
  
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
  
base_gravity_timer_threshold = 0.3  
gravity_timer = 0  
high_score = load_high_score()  
spawn_new_tetrimino()  
  
running = True  
ai_move_made = False  
  
try:  
    while running:  
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                running = False  
  
        if not ai_move_made:  
            x_position, rotation = best_move(board, tetriminos[current_tetrimino])  
              
            while current_position[0] < x_position:    
                move_piece(1, 0, ignore_collision=True)    
            while current_position[0] > x_position:    
                move_piece(-1, 0, ignore_collision=True)    
              
            for _ in range(rotation):  
                rotate_piece()  
              
            ai_move_made = True  
  
        gravity_timer += 1  
        adjusted_gravity_timer_threshold = base_gravity_timer_threshold - cleared_rows_count  
        adjusted_gravity_timer_threshold = max(0.05, adjusted_gravity_timer_threshold)  
  
        if score > high_score:  
            high_score = score  
            save_high_score(high_score)  
  
        if gravity_timer > adjusted_gravity_timer_threshold:  
            tetrimino_placed = move_piece(0, 1)  
            if tetrimino_placed:  
                ai_move_made = False  
            elif not running:  
                running = False  
            gravity_timer = 0  
  
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
  
pygame.quit()  
sys.exit()  
