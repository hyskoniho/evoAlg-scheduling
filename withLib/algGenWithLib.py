from deap import base, creator, tools, algorithms
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed, ThreadPoolExecutor
import random
import numpy as np

# Dicionário de aulas com seus respectivos caracteres
aula_dict = {
    'M': 'Matemática',
    'L': 'Língua Portuguesa',
    'H': 'História',
    'C': 'Ciências',
    'R': 'Ensino Religioso',
    'I': 'Inglês',
    'F': 'Educação Física',
    'A': 'Arte',
}

restricoes = {
    0: {  # Segunda-feira
        'I': ['manhã'],
        'H': ['manhã'],
        'F': []  
    },
    1: {  # Terça-feira
        'I': ['manhã'],
        'H': ['manhã'],
        'F': []
    },
    2: {  # Quarta-feira
        'I': ['manhã'],
        'H': ['manhã'],  
        'F': []
    },
    3: {  # Quinta-feira
        'I': ['manhã'],
        'H': ['manhã'],
        'F': []
    },
    4: {  # Sexta-feira
        'I': ['manhã'],
        'H': ['manhã'],
        'F': [2,3,4,5]  # Educação Física deve estar na terceira até sexta aula (índice 1)
    }
}

requisitos = {
    'M': 28, 
    'L': 28, 
    'H': 16, 
    'C': 8, 
    'R': 4, 
    'I': 20, 
    'F': 4
}


 #! FITTING
def validar_horario(horario, restricoes):
    pontos = 0
    for turma in range(4):
        offset = turma * 30
        for dia in range(5):
            aulas_do_dia = horario[offset + dia*6 : offset + (dia+1)*6]
            regras = restricoes[dia]
            for aula, condicoes in regras.items():
                if isinstance(condicoes, list):
                    for condicao in condicoes:
                        if isinstance(condicao, int):
                            if aulas_do_dia[condicao] != aula:
                                pontos += 1
                        elif isinstance(condicao, list):
                            if not any(aulas_do_dia[i] == aula for i in condicao):
                                pontos += 1
                        elif condicao == 'manhã' and aula in aulas_do_dia[4:]:
                            pontos += 1
                        elif condicao == 'somente' and aula not in aulas_do_dia:
                            pontos += 1
            count_ingles = aulas_do_dia.count('I')
            if count_ingles == 0:
                pontos += 1
            elif count_ingles > 1:
                pontos += (count_ingles - 1)
    return pontos

def verificar_sobreposicao(horario):
    pontuacao = 0
    sub_horarios = [horario[i:i+30] for i in range(0, len(horario), 30)]
    for dia in range(5):
        for aula_index in range(6):
            aulas_no_horario = [sub_horario[dia * 6 + aula_index] for sub_horario in sub_horarios]
            contador_aulas = {}
            for aula in aulas_no_horario:
                contador_aulas[aula] = contador_aulas.get(aula, 0) + 1
            for count in contador_aulas.values():
                if count > 1:
                    pontuacao += (count - 1)
    return pontuacao
def fitting(horario):
    horario = decode_individual(horario)
    contador = Counter(horario)
    pontuacao = sum(abs(requisitos[aula] - contador.get(aula, 0)) for aula in requisitos)
    pontuacao += validar_horario(horario, restricoes)
    pontuacao += verificar_sobreposicao(horario)  
    return pontuacao,

# Função de mapeamento para transformar índices de volta para as chaves
def decode_individual(individual):
    return [list(aula_dict.keys())[i] for i in individual]

# Criando os índices das chaves de aula_dict
indices_aula = list(range(len(aula_dict)))

def encode_individual(individual, indices_aula):
    return [list(aula_dict.keys()).index(i) for i in individual]

# SAMPLE_INDIVIDUAL: list[str] = ['L', 'I', 'L', 'M', 'F', 'L', 'H', 'I', 'H', 'L', 'L', 'R', 'M', 'I', 'L', 'L', 'A', 'M', 'H', 'A', 'L', 'M', 'M', 'I', 'L', 'M', 'I', 'H', 'L', 'F', 'M', 'L', 'C', 'I', 'M', 'M', 'L', 'A', 'L', 'I', 'R', 'L', 'L', 'L', 'H', 'I', 'M', 'L', 'M', 'M', 'I', 'C', 'L', 'M', 'H', 'I', 'M', 'F', 'A', 'F', 'H', 'R', 'M', 'I', 'L', 'A', 'H', 'C', 'M', 'I', 'A', 'A', 'H', 'H', 'I', 'H', 'C', 'M', 'I', 'H', 'H', 'L', 'A', 'L', 'M', 'L', 'I', 'A', 'L', 'C', 'A', 'M', 'I', 'C', 'R', 'C', 'M', 'H', 'I', 'M', 'M', 'M', 'M', 'L', 'M', 'C', 'L', 'I', 'L', 'L', 'A', 'I', 'M', 'A', 'I', 'H', 'H', 'L', 'M', 'M'] 
# FITNESS: (25,)

tam_pop = 512
prob_cruz = 0.8
prob_mut = 0.6
# num_geracoes = 131072
num_geracoes = 1310

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("aula", random.choice, indices_aula)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.aula, 120)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)
population = toolbox.population(n=tam_pop)

# toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=prob_mut)
toolbox.register("select", tools.selTournament, tournsize=6)
toolbox.register("evaluate", fitting)

alg = algorithms.eaSimple(
    population, toolbox, cxpb=prob_cruz, mutpb=prob_mut, ngen=num_geracoes, verbose=True
)

melhor_individuo = tools.selBest(population, 1)[0]
print(f"Melhor indivíduo: {decode_individual(melhor_individuo)}\nFitness: {fitting(melhor_individuo)}")