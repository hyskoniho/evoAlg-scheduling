from Fitting import *
import random
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count


def generate_individual(requirements: dict, length: int = 120):
# Individual generator
    return ''.join(random.choices([
        'M',  # Matemática
        'T',  # Tecnologia (Mind Makers)
        'F',  # Ed. Financeira
        'L',  # Língua Portuguesa
        'H',  # História
        'G',  # Geografia
        'R',  # Ensino Religioso
        'A',  # Artes
        'C',  # Ciências
        'I',  # Inglês
        'U',  # Música
        'E',  # Educação Física
    ], k=length))



def generate_population(size):
# Population generator
    return [generate_individual() for _ in range(size)]



def special_generate_population(
# Function to generate a special population (with predefined minimum
# requirements)
        size: int,
        turmas: int = 4,
        requirements: dict = REQUISITOS):
    population: list = []
    for _ in range(size):
        iv = list(''.join(f'{key}' * (value * turmas)
                  for key, value in requirements.items()))
        random.shuffle(iv)
        population.append(''.join(iv))
    return population



def evaluate_individual(individual: str) -> int | float:
# Apply the fitting function to the individual
    return fitting(individual)



def evaluate_population(
# Apply the fitting function to all the individuals in the population
        population: list[str | list[str]]) -> dict[str, int | float]:
    return {individual: evaluate_individual(
        individual) for individual in population}



def async_evaluate_population(
# Async version of the evaluate_population function
        population: list[str | list[str]]) -> dict[str, int | float]:
    results = {}
    with ProcessPoolExecutor(max_workers=min(4, cpu_count())) as executor:
        futures = {
            executor.submit(
                evaluate_individual,
                individual): individual for individual in population}
        for future in as_completed(futures):
            individual = futures[future]
            results[individual] = future.result()
    return results



def tournament_selection(scores: list[tuple], tournament_size=5):
# Select the parents for the next generation using the tournament
# selection method
    score_list = [score[1] for score in scores]
    individuals = [individual[0] for individual in scores]
    selected = random.sample(range(len(individuals)), tournament_size)
    best = min(selected, key=lambda idx: score_list[idx])
    return individuals[best]



def crossover(parent1, parent2, mate_rate):
# Standard crossover function
    if random.random() > mate_rate:
        crossover_point = random.randint(1, len(parent1) - 1)
        return random.choice([parent1, parent2])
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child



def special_crossover(parent1, parent2, mate_rate, N=3):
    # Crossover function with multiple crossover points
    if random.random() > mate_rate:
        return parent1, parent2  # Retorna os dois pais se a probabilidade não for atingida

    N = min(N, len(parent1) - 1)
    
    crossover_points = sorted(random.sample(range(1, len(parent1)), N))
    child1 = []
    child2 = []
    start = 0
    
    for i in range(N):
        end = crossover_points[i]
        if i % 2 == 0:
            child1 += parent1[start:end]
            child2 += parent2[start:end]
        else:
            child1 += parent2[start:end]
            child2 += parent1[start:end]
        start = end

    if N % 2 == 0:
        child1 += parent1[start:]
        child2 += parent2[start:]
    else:
        child1 += parent2[start:]
        child2 += parent1[start:]

    return ''.join(child1) if isinstance(child1, list) else child1, ''.join(child2) if isinstance(child2, list) else child2



def mutate(individual, mutation_rate):
# Function to mutate an individual with random genes
    mutated = ''.join(
        char if random.random() > mutation_rate else random.choice(list(REQUISITOS.keys()))
        for char in individual
    )
    return mutated


def special_mutate(individual, mutation_rate):
# Function to mutate an individual with a random gene swap
    individual = list(individual)
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(individual) - 1)
            individual[i], individual[j] = individual[j], individual[i]
    return ''.join(individual)


def genetic_algorithm(pop_size: int,
                      num_generations: int,
                      base_mutation_rate: float,
                      mutation_adjustment: float,
                      mutation_rate: float,
                      mating_rate: float,
                      special_insert: None | list[str] = None) -> tuple[str | list[str],
                                                                        int | float]:
    population = special_generate_population(pop_size)

    if special_insert:
        random_pos = random.choices(
            range(
                len(population)),
            k=len(special_insert))
        for pos, individual in zip(random_pos, special_insert):
            population[pos] = individual

    stuck_count: int = 0
    evolve_count: int = 1
    best_score: int | float = float('inf')
    best_individual: str = None

    for generation in range(num_generations):
        if stuck_count != 0 and stuck_count % evolve_count == 0:
            if mutation_rate >= base_mutation_rate * 5:
                print(f"[G-{generation}] Stopping Genetic Algorithm!")
                return best_individual, best_score

            else:
                mutation_rate = round(mutation_rate + mutation_adjustment, 4)
                print(
                    f"[G-{generation}] Mutation rate adjusted to {mutation_rate}!")

        scores: dict = evaluate_population(population)
        scores: list[tuple] = sorted(scores.items(), key=lambda x: x[1])

        if scores[0][1] < best_score:
            best_score = scores[0][1]
            best_individual = scores[0][0]

            print(
                f"[G-{generation}] Fit: {best_score} | Individual: {best_individual}")
            evolve_count = max(stuck_count,
                               (evolve_count // 2) if evolve_count > 1 else 1)
            stuck_count = 0
            mutation_rate = base_mutation_rate

            if best_score <= 0:
                print(
                    f"[G-{generation}] Best individual found!")
                return best_individual, best_score

        else:
            stuck_count += 1

        new_population = []
        while len(new_population) < pop_size:
            parent1 = tournament_selection(scores, 80)
            parent2 = tournament_selection(scores, 80)
            children = special_crossover(
                parent1, parent2, N=3, mate_rate=mating_rate
            )
            children = [special_mutate(child, mutation_rate) for child in children]
            new_population.extend(children)

        population = new_population
