import random
import sys
import csv
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import freeze_support

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

# Gerar horários aleatórios
def gerar_horarios(num_horarios=200):
    return [''.join(random.choice(list(aula_dict.keys())) for _ in range(120)) for _ in range(num_horarios)]

# Validação do horário
def validar_horario(horario, restricoes):
    pontos = 0
    for dia, regras in restricoes.items():
        aulas_do_dia = horario[dia * 6:(dia + 1) * 6]  # Cada dia tem 6 aulas
        for aula, condicoes in regras.items():
            if isinstance(condicoes, list):
                for condicao in condicoes:
                    if isinstance(condicao, int):  # Se for um horário específico
                        if aulas_do_dia[condicao] != aula:  # Aula não está na posição correta
                            pontos += 1
                    elif isinstance(condicao, list):  # Lista de horários permitidos
                        if not any(aulas_do_dia[i] == aula for i in condicao):
                            pontos += 1  # Penaliza se a aula não estiver em nenhum dos horários permitidos
                    elif condicao == 'manhã' and aula in aulas_do_dia[3:]:  # Deve estar até a 3ª aula
                        pontos += 1
                    elif condicao == 'somente' and aula not in aulas_do_dia:  # Deve estar presente no dia
                        pontos += 1
        count_ingles = aulas_do_dia.count('I')
        if count_ingles == 0:
            pontos += 1  # Penaliza se não houver Inglês no dia
        elif count_ingles > 1:
            pontos += (count_ingles - 1)  # Penaliza por cada aula extra de Inglês no dia
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

# Função de Fitness
def fitting(horario):
    contador = Counter(horario)
    pontuacao = sum(abs(requisitos[aula] - contador.get(aula, 0)) for aula in requisitos)
    pontuacao += validar_horario(horario, restricoes)
    pontuacao += verificar_sobreposicao(horario)   
    return pontuacao

# Crossover Inteligente
def crossover(pai1, pai2):
    filho1, filho2 = list(pai1), list(pai2)
    for i in range(0, len(pai1), 6):
        bloco_pai1 = pai1[i:i+6]
        bloco_pai2 = pai2[i:i+6]
        fitness_pai1 = fitting(''.join(filho1[:i]) + bloco_pai1 + ''.join(filho1[i+6:]))
        fitness_pai2 = fitting(''.join(filho2[:i]) + bloco_pai2 + ''.join(filho2[i+6:]))
        if fitness_pai1 < fitness_pai2:
            filho1[i:i+6] = list(bloco_pai1)
            filho2[i:i+6] = list(bloco_pai1)
        else:
            filho1[i:i+6] = list(bloco_pai2)
            filho2[i:i+6] = list(bloco_pai2)
    filho1 = mutacao_direcionada(filho1)
    filho2 = mutacao_direcionada(filho2)
    if fitting(''.join(filho1)) > min(fitting(pai1), fitting(pai2)):
        filho1 = list(pai1)
    if fitting(''.join(filho2)) > min(fitting(pai1), fitting(pai2)):
        filho2 = list(pai2)
    return ''.join(filho1), ''.join(filho2)

def mutacao_direcionada(horario_list):
    for dia in range(0, len(horario_list), 6):
        aulas_dia = horario_list[dia:dia+6]
        for aula in set(aulas_dia):
            if aulas_dia.count(aula) > 2:
                idxs = [i for i, x in enumerate(aulas_dia) if x == aula]
                if len(idxs) > 2:
                    for idx in idxs[2:]:
                        aulas_dia[idx] = random.choice(list(aula_dict.keys()))
        horario_list[dia:dia+6] = aulas_dia
    return horario_list

def mutacao_inteligente(horario):
    """ 
    Aplica mutação adaptativa: 
    - Quanto pior o horário (maior a pontuação), maior a chance de mutação. 
    - Troca aleatoriamente um gene com base na pontuação.
    """
    pontuacao = fitting(horario)  # Avalia o quão longe está do ideal (0)
    
    # Define a taxa de mutação de forma adaptativa (quanto pior, maior a taxa)
    taxa_mutacao = min(0.1 + (pontuacao / 1000), 0.5)  # Máx de 50% de mutação

    if random.random() < taxa_mutacao:
        horario = list(horario)  # Converte para lista mutável
        idx = random.randint(0, len(horario) - 1)  # Escolhe um índice aleatório
        horario[idx] = random.choice(list(aula_dict.keys()))  # Substitui por uma aula aleatória
        return ''.join(horario)
    
    return horario  # Retorna o mesmo se não houver mutação

# Função para calcular fitness em paralelo
def calcular_fitness(horarios):
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(fitting, horario): horario for horario in horarios}
        resultados = {}
        for future in as_completed(futures):
            resultados[futures[future]] = future.result()
    return resultados

def algGen(pop_size, eugeny, max_gen=100000):
    melhor_pontuacao = float('inf')
    sem_melhora = 0
    
    populacao = gerar_horarios(pop_size)
    for geracao in range(max_gen):
        pontuacoes = calcular_fitness(populacao)
        populacao = sorted(pontuacoes.keys(), key=lambda x: pontuacoes[x])
        
        if pontuacoes[populacao[0]] == 0:
            print(f'Geração {geracao}: Melhor solução encontrada! {populacao[0]}')
            break
        
        if pontuacoes[populacao[0]] < melhor_pontuacao:
            melhor_pontuacao = pontuacoes[populacao[0]]
            sys.stdout.write(f'Geração {geracao}, Melhor pontuação: {melhor_pontuacao}, Gene: {populacao[0]}\n')
            sem_melhora = 0
        else:
            sem_melhora += 1
        
        if sem_melhora > 250:
            nova_populacao = populacao[:pop_size//2]
            nova_populacao.extend(gerar_horarios(pop_size//2))
            sem_melhora = 0
        
        else:   
            nova_populacao = populacao[:eugeny]
            while len(nova_populacao) < pop_size:
                pai1, pai2 = random.sample(populacao[:pop_size//2], 2)
                filho1, filho2 = crossover(pai1, pai2)
                nova_populacao.extend([mutacao_inteligente(filho1), mutacao_inteligente(filho2)])
        
        populacao = nova_populacao
        
    return populacao[0]


if __name__ == '__main__':
    freeze_support()
    
    melhor_horario = algGen(
        pop_size=300,  # Tamanho da população
        eugeny=10,  # Quantidade de indivíduos selecionados por eugenia
        max_gen=100000  # Número máximo de gerações
    )

