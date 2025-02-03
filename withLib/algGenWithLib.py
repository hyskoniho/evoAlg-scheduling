from deap import base, creator, tools, algorithms
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed, ThreadPoolExecutor
import random, sys, os
import numpy as np

# Medidas drásticas tomadas aqui. Não faça isso em casa!
try:
    from fitting import *
    from aux_tools import *
    
except ModuleNotFoundError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../fitting')))
    from fitting_function import *
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../aux_tools')))
    from hr_format import *

AULAS: list[str] = ['M', 'T', 'F', 'L', 'H', 'G', 'R', 'A', 'C', 'I', 'U', 'E']

# Função de mapeamento para transformar índices de volta para as chaves
def decode_individual(individual):
    return [AULAS[i] for i in individual]

# Criando os índices das chaves de aula_dict
indices_aula = list(range(len(AULAS)))

def encode_individual(individual, indices_aula):
    return [AULAS.index(i) for i in individual]

def fit_individual(individual):
    return fitting(decode_individual(individual)),

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
toolbox.register("evaluate", fit_individual)

alg = algorithms.eaSimple(
    population, toolbox, cxpb=prob_cruz, mutpb=prob_mut, ngen=num_geracoes, verbose=True
)

melhor_individuo = tools.selBest(population, 1)[0]
print(f"Melhor indivíduo: {decode_individual(melhor_individuo)}\nFitness: {fitting(melhor_individuo)}")