#genetic_algorithm.py
import random  
from tetris_ai import best_move
from tetris import Tetris
import concurrent.futures  


population_size = 50  
elitism_size = 10  
mutation_rate = 0.1  
num_generations = 100  
  
def run_game_with_heuristics(heuristics):    
    tetris_game = Tetris()    
    base_gravity_timer_threshold = 0.05  
    gravity_timer = 0  
    tetris_game.spawn_new_tetrimino()    
  
    running = True  
    ai_move_made = False  
  
    while running:    
        if not ai_move_made:  
            current_piece = tetris_game.tetriminos[tetris_game.current_tetrimino]  
            next_piece = tetris_game.tetriminos[tetris_game.next_tetrimino]  
            x_position, rotation = best_move(tetris_game.board, current_piece, next_piece, heuristics)  
  
            for _ in range(rotation):  
                tetris_game.rotate_piece()  
  
            while tetris_game.current_position[0] < x_position:  
                tetris_game.move_piece(1, 0, ignore_collision=True)  
            while tetris_game.current_position[0] > x_position:  
                tetris_game.move_piece(-1, 0, ignore_collision=True)  
  
            ai_move_made = True  
  
        gravity_timer += 1  
        adjusted_gravity_timer_threshold = base_gravity_timer_threshold - tetris_game.cleared_rows_count  
        adjusted_gravity_timer_threshold = max(0.05, adjusted_gravity_timer_threshold)  
  
        if gravity_timer > adjusted_gravity_timer_threshold:  
            game_status = tetris_game.move_piece(0, 1)  
            if game_status is not None:  
                if game_status:  
                    ai_move_made = False  
                else:  
                    running = False  
  
    # Print score and cleared lines for the current individual  
    print(f"Score: {tetris_game.score}, Cleared lines: {tetris_game.cleared_rows_count}")  

    return tetris_game.score, tetris_game.cleared_rows_count  


def create_individual():  
    return [random.uniform(-10, 10) for _ in range(5)]  # 5 heuristics with random values  
  
def create_population(size):  
    return [create_individual() for _ in range(size)]  
  
import concurrent.futures  
  
def evaluate_individual(individual):  
    score, cleared_lines = run_game_with_heuristics(individual)  
    return score + cleared_lines  
  
def rank_population(population):  
    with concurrent.futures.ThreadPoolExecutor() as executor:  
        # Evaluate each individual in the population using multiple threads  
        performances = list(executor.map(evaluate_individual, population))  
  
    # Sort the population based on their performances  
    return sorted(population, key=lambda x: performances[population.index(x)], reverse=True)  

def crossover(parent1, parent2):  
    crossover_point = random.randint(1, len(parent1) - 1)  
    child1 = parent1[:crossover_point] + parent2[crossover_point:]  
    child2 = parent2[:crossover_point] + parent1[crossover_point:]  
    return child1, child2  
  
def mutate(individual, mutation_rate):  
    for i in range(len(individual)):  
        if random.random() < mutation_rate:  
            individual[i] += random.uniform(-1, 1)  
    return individual  
  
def create_new_generation(population, elitism_size, mutation_rate):  
    ranked_population = rank_population(population)  
    new_population = ranked_population[:elitism_size]  # Keep the top-performing individuals  
  
    # Generate offspring through crossover and mutation  
    while len(new_population) < len(population):  
        parent1, parent2 = random.sample(ranked_population[:elitism_size], 2)  
        child1, child2 = crossover(parent1, parent2)  
        new_population.extend([mutate(child1, mutation_rate), mutate(child2, mutation_rate)])  
  
    return new_population  

population = create_population(population_size)  
  
for generation in range(num_generations):  
    print(f"Generation {generation + 1}")  
    population = create_new_generation(population, elitism_size, mutation_rate)  
    best_individual = rank_population(population)[0]  
    print(f"Best heuristics: {best_individual}")  
