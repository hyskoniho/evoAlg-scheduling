import random, os, sys, math
from ptymer import Timer

try:
    from fitting import *
    from aux_tools import *
    
except ModuleNotFoundError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../fitting')))
    from fitting_function import *
    
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../aux_tools')))
    from hr_format import *
    from trace_function import *

# Definindo os requisitos multiplicados por 4
requirements = {
    'M': 20,  
    'T': 4,  
    'F': 4,  
    'L': 28,  
    'H': 8,  
    'G': 8,  
    'R': 4,  
    'A': 8,  
    'C': 8,  
    'I': 20,  
    'U': 4,  
    'E': 4,  
}

# # Função que calcula a nota da solução
# def fitting(schedule):
#     count = {key: 0 for key in requirements.keys()}
    
#     for char in schedule:
#         if char in count:
#             count[char] += 1
            
#     # Calculando a nota
#     score = 0
#     for key in requirements:
#         score += abs(count[key] - requirements[key])
    
#     return score

# Função para gerar uma solução inicial aleatória
def generate_initial_solution():
    characters = list(requirements.keys())
    return ''.join(random.choices(characters, k=120))

# Função para gerar uma solução vizinha
def get_neighbor(solution):
    # Escolhe dois índices aleatórios para trocar
    idx1, idx2 = random.sample(range(len(solution)), 2)
    neighbor = list(solution)
    neighbor[idx1], neighbor[idx2] = neighbor[idx2], neighbor[idx1]
    return ''.join(neighbor)

# Função de Simulated Annealing
@Timer(visibility=True)
def simulated_annealing(initial_solution, initial_temp, cooling_rate, max_iterations):
    current_solution = initial_solution
    current_score = fitting(current_solution)
    best_solution = current_solution
    best_score = current_score
    
    temperature = initial_temp
    
    for iteration in range(max_iterations):
        # Gera uma solução vizinha
        neighbor_solution = get_neighbor(current_solution)
        neighbor_score = fitting(neighbor_solution)
        
        # Se a nova solução é melhor, aceita
        if neighbor_score < current_score:
            current_solution = neighbor_solution
            current_score = neighbor_score
            
            # Atualiza a melhor solução encontrada
            if neighbor_score < best_score:
                best_solution = neighbor_solution
                best_score = neighbor_score
        else:
            # Aceita a nova solução com uma probabilidade
            acceptance_probability = math.exp((current_score - neighbor_score) / temperature)
            if random.random() < acceptance_probability:
                current_solution = neighbor_solution
                current_score = neighbor_score
        
        # Resfriamento
        temperature *= cooling_rate
        
        # Se a nota for 0, encontramos a solução perfeita
        if best_score == -0.56:
            break
    
    return best_solution, best_score

# Parâmetros do algoritmo
initial_temp = 1000
cooling_rate = 0.95
max_iterations = 500000

# Executando o algoritmo
# initial_solution = generate_initial_solution()
# initial_solution = 'GICLLAFTLIAMGLHIRLMLHICMMILMUEILFMCMIHULLLMMIMLRHILGTCGLAIEAUGIGMCLLIHRALIMLMCLFITLLIHEAMMMMLIULHIMMTCIGLHCFIGMLRLAAIELL'
# initial_solution = 'IMLLLAULIHMCHIGFLCMLMIRLGAIMETAGIMCLMAHILUMMLICLLMIGFRIHLLTELLUIATGIMFCLLGILMRIHHMLCMEMILAGIMAMCIFLLATILMGRMHILLCMLIEHUL'
# initial_solution = 'LILTCMIALLAUHCGIMRIMFHMLLIMGELMAILLCUGIAMCLMIGREFIHLLMHLLITMIMHHULGLGICLMIMTLLRLLICMMFIEAAGLAIMUMIMMLTILLLCFHGIMRCIHALLE'
# initial_solution = 'MIHHAAGGLIUMLLIFCCILTLRLMMILMEULLILLAIMMCCGGHIRFMMLILTHIMEALIMAACCLLIGTUMIMGLLHHIMMRLLLIEFHHIMMMIMULLLITLLMRLIGGCCIAEFLA'
initial_solution = 'TLIUAAFIGGCCMMMIRMHHILLLIMLLLELIGGMMIMMMFTLILHLRLLHICCLUEIAAIMMLLLHHIAALGLILCCFILGTRUIMEMMAALICCLLLILUIGGMMLIMMMRFHHITEL'
best_solution, best_score = simulated_annealing(initial_solution, initial_temp, cooling_rate, max_iterations)

print("Melhor solução encontrada:", best_solution)
print("Nota da melhor solução:", best_score)