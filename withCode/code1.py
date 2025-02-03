import random
from collections import Counter

# Parâmetros do algoritmo
POPULATION_SIZE = 250  # Tamanho da população
NUM_GENERATIONS = 10000  # Número de gerações
MATE_RATE = 0.8  # Taxa de cruzamento
MUTATION_RATE = 0.01  # Taxa de mutação inicial
MUTATION_ADJUSTMENT = 0.001  # Ajuste dinâmico da taxa de mutação















def separar_turmas(horario: str, quantidade_turmas: int = 4) -> list[str]:
    """ Separa o horário em turmas
    
    Args:
        horario (str): Horário das aulas
        quantidade_turmas (int, optional): Quantidade de turmas. Defaults to 4.
    
    Returns:
        list[str]: Lista de horários separados por turma
    """
    
    # Cria uma lista de strings vazias
    turmas: list[str] = ['' for _ in range(quantidade_turmas)]
    
    # Itera sobre o horário
    for i, aula in enumerate(horario):
        # Adiciona a aula na turma correspondente
        turmas[i % quantidade_turmas] += aula
    
    return turmas

def separar_dias(turma: str) -> list[list[str]]:
    """ Separa a turma em dias
    
    Args:
        turma (str): Horário de uma turma
    
    Returns:
        list[list[str]]: Lista de horários separados por dia
    """
    
    # Cria uma lista de strings vazias
    dias: list[list[str]] = [['' for _ in range(6)] for _ in range(5)]
    
    # Itera sobre o horário
    for i, aula in enumerate(turma):
        # Adiciona a aula no dia correspondente
        dias[i // 6][i % 6] = aula
    
    return dias

REQUISITOS: dict = {
    'M': 5*4, 
    'T': 1, 
    'F': 1, 
    'L': 7*4, 
    'H': 2*4, 
    'G': 2*4, 
    'R': 1, 
    'A': 2*4, 
    'C': 2*4, 
    'I': 5*4, 
    'U': 1, 
    'E': 1, 
}

def quantidade_aulas(horario: str, requisitos: dict) -> int:
    """ Verifica se o horário tem a quantidade de aulas necessárias 
    
    Args:
        horario (str): Horário das aulas
        requisitos (dict): Requisitos de aulas por matéria
    
    Returns:
        int: Quantidade de aulas faltantes ou excedentes
    """
    
    # Conta a quantidade de aulas de cada matéria no horário especificado
    c: Counter = Counter(horario)
    # e.g. {'M': 28, 'L': 28, 'H': 16, 'C': 8, 'R': 4, 'I': 20, 'F': 4}
    
    n: int =  sum( # Somatório
        abs( # Valor absoluto para obter a diferença entre a quantidade de aulas esperada e a quantidade de aulas no horário
            requisitos[materia] - c.get(materia, 0) # Quantidade esperada daquela matéria - Quantidade de aulas daquela matéria no horário
        ) \
            for materia in requisitos # Aplica a operação para cada matéria, e soma o resultado
    )
    
    return n

def validar_restricoes(horario: str) -> int:
    """ Verifica se o horário atende as restrições"""
    # TODO:  Somar a distância entre o horário esperado x horário anotado pois incentiva mais a aproximação do horário esperado
    
    n: int = 0
    for turma in separar_turmas(horario):
        for d, dia in enumerate(separar_dias(turma)):
            
            # Verifica se o horário da aula de inglês é após as 10:50
            if 'I' in dia and dia.index('I') >= 4:
                n += 1
            
            # Verifica se tem aula de inglês
            if 'I' not in dia:
                n += 1
            
            # Verifica se o horário de História é após as 10:50
            if 'H' in dia and dia.index('H') >= 4:
                n += 1
                
            # Verifica se o horário de Geografia é após as 10:50
            if 'G' in dia and dia.index('G') >= 4:
                n += 1
                
            # Verifica se o horário de Educação Física é antes das 9:10
            if 'E' in dia and dia.index('E') < 2:
                n += 1
                
            # Verifica se o dia da educação física não é sexta-feira
            if 'E' in dia and d < 4:
                n += 1
                
            # Verifica se o dia de Artes é segunda-feira, terça-feira ou sexta-feira
            if 'A' in dia and d not in [0, 1, 4]:
                n += 1
            
            # Verifica se o dia de Música é segunda-feira, terça-feira ou sexta-feira
            if 'U' in dia and d not in [0, 1, 4]:
                n += 1

    return n

def validar_sobreposicoes(strings: list[str]) -> int:
    
    # Inicializa um dicionário para contar os caracteres em cada índice
    contagem = {}
    
    # Itera sobre cada string e cada índice
    for string in strings:
        for i, char in enumerate(string):
            if i not in contagem:
                contagem[i] = set()  # Usamos um conjunto para evitar duplicatas
            contagem[i].add(char)
    
    # Conta quantos índices têm mais de um caractere
    sobreposicoes = sum(1 for chars in contagem.values() if len(chars) > 1)
    
    return sobreposicoes

def fitting(horario: str, requisitos: dict = REQUISITOS) -> int:
    """ Função de fitness"""
    
    return quantidade_aulas(horario, requisitos) + validar_restricoes(horario) + validar_sobreposicoes(separar_turmas(horario))























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
    stuck_count = -1
    evolve_count = 0
    best_score = float('inf')
    best_individual = None
    
    for generation in range(NUM_GENERATIONS):
        scores = evaluate_population(population)
        
        # Ajuste dinâmico da taxa de mutação
        global MUTATION_RATE
        if best_score > min(scores) and stuck_count == evolve_count:
            MUTATION_RATE += MUTATION_ADJUSTMENT
        else:
            MUTATION_RATE = max(0.01, MUTATION_RATE - MUTATION_ADJUSTMENT)

        new_population = []
        
        for _ in range(POPULATION_SIZE):
            parent1 = tournament_selection(population, scores)
            parent2 = tournament_selection(population, scores)
            child = crossover(parent1, parent2)
            child = mutate(child, MUTATION_RATE)
            new_population.append(child)
        
        population = new_population
        
        # Exibir o melhor indivíduo da geração
        if min(scores) < best_score:
            best_score = min(scores)
            best_individual = population[scores.index(best_score)]
            
            print(f"Geração {generation + 1}: Melhor Indivíduo: {best_individual}, Score: {best_score}")
            evolve_count = max([stuck_count, evolve_count])
            stuck_count = 0
            
        else:
            stuck_count += 1

if __name__ == "__main__":    
    genetic_algorithm()
