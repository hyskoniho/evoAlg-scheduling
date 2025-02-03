import random, os, sys
from ptymer import Timer

# Medidas drásticas tomadas aqui. Não faça isso em casa!
try:
    from fitting import *
    from aux_tools import *
    
except ModuleNotFoundError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../fitting')))
    from fitting_function import *
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../aux_tools')))
    from hr_format import *

# Parâmetros do algoritmo
POPULATION_SIZE = 200  # Tamanho da população
NUM_GENERATIONS = 100000  # Número de gerações
MATE_RATE = 0.7  # Taxa de cruzamento
BASE_MUTATION_RATE = 0.01  # Taxa de mutação inicial
MUTATION_RATE = BASE_MUTATION_RATE  # Taxa de mutação variável
MUTATION_ADJUSTMENT = 0.0025  # Ajuste dinâmico da taxa de mutação
EUGENY = int(POPULATION_SIZE*0.05)  # Número de indivíduos que passam para a próxima geração
BEST_DUDE = ''  # Melhor indivíduo

# Função para gerar um indivíduo
def generate_individual(length=120):
    return ''.join(random.choices([
        'M', # Matemática
        'T', # Tecnologia (Mind Makers)
        'F', # Ed. Financeira
        'L', # Língua Portuguesa
        'H', # História
        'G', # Geografia
        'R', # Ensino Religioso
        'A', # Artes
        'C', # Ciências
        'I', # Inglês
        'U', # Música
        'E', # Educação Física
    ], k=length))

# Função para gerar a população inicial
def generate_population(size=POPULATION_SIZE):
    return [generate_individual() for _ in range(size)]

# Função para gerar uma população especial (com os requisitos mínimos já definidos)
def special_generate_population(size=POPULATION_SIZE): 
    lis = []
    for _ in range(size):
        iv = list(''.join(f'{key}' * value for key, value in REQUISITOS.items()))
        random.shuffle(iv)
        lis.append(''.join(iv))
    return lis

# Função de avaliação de um indivíduo
def evaluate_individual(individual):
    return fitting(individual)

# Função para avaliar a população inteira
def evaluate_population(population):
    return [evaluate_individual(individual) for individual in population]

# Função de seleção por torneio
def tournament_selection(population, scores, tournament_size=5):
    selected = random.sample(range(len(population)), tournament_size)
    best = min(selected, key=lambda idx: scores[idx])
    return population[best]

# Função de cruzamento (crossover)
def crossover(parent1, parent2, mate_rate=MATE_RATE):
    crossover_point = random.randint(1, len(parent1) - 1)
    if random.random() > mate_rate:
        return random.choice([parent1, parent2])
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

# Função de mutação
def mutate(individual, mutation_rate=MUTATION_RATE):
    mutated = ''.join(
        char if random.random() > mutation_rate else random.choice([
            'M', # Matemática
            'T', # Tecnologia (Mind Makers)
            'F', # Ed. Financeira
            'L', # Língua Portuguesa
            'H', # História
            'G', # Geografia
            'R', # Ensino Religioso
            'A', # Artes
            'C', # Ciências
            'I', # Inglês
            'U', # Música
            'E', # Educação Física
        ])
        for char in individual
    )
    return mutated

# Loop de execução principal
def genetic_algorithm():
    population = generate_population()
    stuck_count = 0
    evolve_count = 1
    best_score = float('inf')
    best_individual = None
    
    for generation in range(NUM_GENERATIONS):
        scores = evaluate_population(population)
        
        # Ajuste dinâmico da taxa de mutação
        global MUTATION_RATE
        if stuck_count != 0 and stuck_count % evolve_count == 0:
            MUTATION_RATE += MUTATION_ADJUSTMENT
            print(f"[G-{generation}] Taxa de mutação ajustada para {MUTATION_RATE}!")
        # else:
        #     MUTATION_RATE = max(0.01, MUTATION_RATE - MUTATION_ADJUSTMENT)

        new_population = []
        for _ in range(POPULATION_SIZE - EUGENY):
            parent1 = tournament_selection(population, scores)
            parent2 = tournament_selection(population, scores)
            child = crossover(parent1, parent2)
            child = mutate(child, MUTATION_RATE)
            new_population.append(child)
        
        new_population.extend(sorted(population, key=lambda x: evaluate_individual(x))[:EUGENY])
        population = new_population
        
        # Exibir o melhor indivíduo da geração
        if min(scores) < best_score:
            best_score = min(scores)
            best_individual = population[scores.index(best_score)]
            
            print(f"[G-{generation}] Nota: {best_score} | Melhor Indivíduo: {best_individual}")
            evolve_count = max(stuck_count, evolve_count)
            stuck_count = 0
            MUTATION_RATE = BASE_MUTATION_RATE
            
            global BEST_DUDE
            BEST_DUDE = best_individual
            
        else:
            stuck_count += 1

if __name__ == "__main__":  
    with Timer(visibility=True):
        try:  
            genetic_algorithm()
            
        except KeyboardInterrupt:
            print("\n\nExecução interrompida pelo usuário!\n\n")
            print_table(BEST_DUDE)
