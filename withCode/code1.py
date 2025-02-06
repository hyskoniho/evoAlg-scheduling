import random, os, sys
from ptymer import Timer
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import freeze_support

# Medidas drásticas tomadas aqui. Não faça isso em casa!
try:
    from fitting import *
    from aux_tools import *
    
except ModuleNotFoundError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../fitting')))
    from fitting_function import *
    
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../aux_tools')))
    from hr_format import *
    from trace_function import *

# Parâmetros do algoritmo
POPULATION_SIZE = 250  # Tamanho da população
NUM_GENERATIONS = 10000000  # Número de gerações
MATE_RATE = 0.7  # Taxa de cruzamento
BASE_MUTATION_RATE = 0.01  # Taxa de mutação inicial
MUTATION_RATE = BASE_MUTATION_RATE  # Taxa de mutação variável
MUTATION_ADJUSTMENT = 0.0025  # Ajuste dinâmico da taxa de mutação
# EUGENY = int(POPULATION_SIZE*0.05)  # Número de indivíduos que passam para a próxima geração
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
def special_generate_population(size=POPULATION_SIZE, turmas: int = 4): 
    lis = []
    for _ in range(size):
        iv = list(''.join(f'{key}' * (value * turmas) for key, value in REQUISITOS.items()))
        random.shuffle(iv)
        lis.append(''.join(iv))
    return lis

# Função de avaliação de um indivíduo
def evaluate_individual(individual):
    return fitting(individual)

# Função para avaliar a população inteira
def evaluate_population(population):
    return [evaluate_individual(individual) for individual in population]

# Função para avaliar a população inteira de maneira assíncrona
def async_evaluate_population(population):
    with ThreadPoolExecutor(max_workers=32) as executor:
        futures = {executor.submit(evaluate_individual, individual): idx for idx, individual in enumerate(population)}
        resultados = [None] * len(population)
        for future in as_completed(futures):
            idx = futures[future]
            resultados[idx] = future.result()
    return resultados

# Função de seleção por torneio
def tournament_selection(population, scores, tournament_size=5):
    selected = random.sample(range(len(population)), tournament_size)
    best = min(selected, key=lambda idx: scores[idx])
    return population[best]

def roulette_selection(population, scores):
    total_score = sum(scores)
    probabilities = [(total_score - score) / total_score for score in scores]
    
    cumulative_probabilities = []
    cumulative_sum = 0
    for prob in probabilities:
        cumulative_sum += prob
        cumulative_probabilities.append(cumulative_sum)

    # Selecionar um número aleatório entre 0 e 1
    random_value = random.random()
    
    # Encontrar o indivíduo correspondente ao valor aleatório
    for i, cumulative_probability in enumerate(cumulative_probabilities):
        if random_value <= cumulative_probability:
            return population[i]

# Função de cruzamento (crossover)
def crossover(parent1, parent2, mate_rate=MATE_RATE):
    if random.random() > mate_rate:
        crossover_point = random.randint(1, len(parent1) - 1)
        return random.choice([parent1, parent2])
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

# Função de cruzamento (crossover) com N pontos
def special_crossover(parent1, parent2, N=3, mate_rate=MATE_RATE):
    if random.random() > mate_rate:
        return random.choice([parent1, parent2])
    
    # Garantir que N seja um número válido
    N = min(N, len(parent1) - 1)

    # Gerar N pontos de crossover aleatórios
    crossover_points = sorted(random.sample(range(1, len(parent1)), N))
    
    # Inicializar a lista para o filho
    child = []
    
    # Alternar entre os pais de acordo com os pontos de crossover
    start = 0
    for i in range(N):
        end = crossover_points[i]
        if i % 2 == 0:
            child += parent1[start:end]
        else:
            child += parent2[start:end]
        start = end

    # Adicionar a última parte do genoma (depois do último ponto de crossover)
    if N % 2 == 0:
        child += parent1[start:]
    else:
        child += parent2[start:]

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

def special_mutate(individual, mutation_rate=MUTATION_RATE):
    individual = list(individual)  # Converte o indivíduo para uma lista para facilitar a troca
    
    # Aplica a mutação
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(individual) - 1)
            individual[i], individual[j] = individual[j], individual[i]
    
    return ''.join(individual)

# Loop de execução principal
def genetic_algorithm(special_insert: None | list[str] =None):
    population = special_generate_population()
    
    if special_insert:
        random_pos = random.choices(range(len(population)), k=len(special_insert))
        for pos, individual in zip(random_pos, special_insert):
            population[pos] = individual

    stuck_count = 0
    evolve_count = 1
    best_score = float('inf')
    best_individual = None
    cataclisms = 0
    
    for generation in range(NUM_GENERATIONS):
        # Ajuste dinâmico da taxa de mutação
        global MUTATION_RATE
        if stuck_count != 0 and stuck_count % evolve_count == 0:
            if MUTATION_RATE >= 1:
                print(f"[G-{generation}] Taxa de mutação atingiu o limite máximo! Realizando a recriação da população...")
                population = special_generate_population(POPULATION_SIZE-1)
                
                population.append(best_individual)
                MUTATION_RATE = BASE_MUTATION_RATE
                stuck_count = 0
                evolve_count = (evolve_count//2) if evolve_count > 1 else 1
                
                if cataclisms <= 2:
                    cataclisms += 1
                else:
                    print(f"[G-{generation}] Cataclismas consecutivos! Realizando a recriação da população com aumento significativo...")
                    track_execution(fitting, best_individual)
                    population.extend(special_generate_population((len(population)*2)-POPULATION_SIZE))
                    cataclisms = 0
                
            else:
                MUTATION_RATE = round(MUTATION_RATE + MUTATION_ADJUSTMENT, 4)
                print(f"[G-{generation}] Taxa de mutação ajustada para {MUTATION_RATE}!")
                
        scores = async_evaluate_population(population)
        
        # Exibir o melhor indivíduo da geração
        if min(scores) < best_score:
            best_score = min(scores)
            best_individual = population[scores.index(best_score)]
            
            print(f"[G-{generation}] Nota: {best_score} | Melhor Indivíduo: {best_individual}")
            evolve_count = max(stuck_count, (evolve_count//2) if evolve_count > 1 else 1)
            stuck_count = 0
            cataclisms = 0
            MUTATION_RATE = BASE_MUTATION_RATE
            
            global BEST_DUDE
            BEST_DUDE = best_individual
            if best_score == 0:
                raise AttributeError(f"Melhor indivíduo encontrado!{'\n'.join([f'{k}: {v}' for k, v in locals().items()])}")
            
        else:
            stuck_count += 1

        new_population = []
        # for _ in range(POPULATION_SIZE - EUGENY):
        for _ in range(len(population)):
            parent1 = tournament_selection(population, scores, 100)
            parent2 = tournament_selection(population, scores, 100)
            child = special_crossover(parent1, parent2, N=7)
            child = special_mutate(child, MUTATION_RATE)
            new_population.append(child)
        
        # new_population.extend(sorted(population, key=lambda x: evaluate_individual(x))[:EUGENY])
        population = new_population

if __name__ == "__main__":  
    freeze_support()
    with Timer(visibility=True):
        try:
            best_path = os.path.join(os.path.dirname(__file__), 'best_individuals.txt')
            sp = []
            
            if os.path.exists(best_path):
                with open(best_path, 'r') as f:
                    for line in f:
                        sp.append(line.strip())
            
            genetic_algorithm(
                # special_insert=sp
            )
            
        except KeyboardInterrupt:
            print("\n\nExecução interrompida pelo usuário!\n\n")
            print_table(BEST_DUDE)
            print(f"\n\nIndivíduo: {BEST_DUDE}\nNota: {fitting(BEST_DUDE)}")
            track_execution(fitting, BEST_DUDE)
        
        except AttributeError as e:
            print(e)
            print_table(BEST_DUDE)
            exit(BEST_DUDE)
            
        
        with open(best_path, 'a' if os.path.exists(best_path) else 'w') as f:
            f.write(f"{BEST_DUDE}\n")
