import random

# Dicionário de aulas com seus respectivos caracteres
aula_dict = {
    'M': 'Matemática',
    'L': 'Língua Portuguesa',
    'E': 'Educação Financeira',
    'H': 'História',
    'G': 'Geografia',
    'C': 'Ciências',
    'R': 'Ensino Religioso',
    'U': 'Música',
    'I': 'Inglês',
    'F': 'Educação Física',
    'A': 'Arte'
}


def gerar_horarios(num_horarios=100):
    horarios = [''.join(random.choice(list(aula_dict.keys())) for _ in range(90)) for _ in range(num_horarios)]
    return horarios


def validar_horario(horario, restricoes):
    ponto = 0
    for dia, regras in restricoes.items():
        aulas_do_dia = horario[dia * 6:(dia + 1) * 6]  # Cada dia tem 6 aulas, dia vai de 0 (segunda) a 4 (sexta)
        for aula, condicoes in regras.items():
            # Verificar se há restrições de horário
            if 'manhã' in condicoes and aula in aulas_do_dia[3:]:
                ponto +=1
            if 'somente' in condicoes and aula not in aulas_do_dia:
                ponto +=1  # Aula deve estar presente no dia específico
    return ponto

# Definir restrições para as aulas
restricoes = {
    0: {  # Segunda-feira
        'G': ['manhã'],  # Geografia até 10h50
        'H': ['manhã'],  # História até 10h50
        'M': ['manhã'],  # Matemática até 10h50
    },
    1: {  # Terça-feira
        'G': ['manhã'],  # Geografia até 10h50
        'H': ['manhã'],  # História até 10h50
        'M': ['manhã'],  # Matemática até 10h50
    },
    2: {  # Quarta-feira
        'G': ['manhã'],  # Geografia até 10h50
        'H': ['manhã'],  # História até 10h50
        'M': ['manhã'],  # Matemática até 10h50
        'F': ['manhã']  # Educação Física somente pela manhã
    },
    3: {  # Quinta-feira
        'G': ['manhã'],  # Geografia até 10h50
        'H': ['manhã'],  # História até 10h50
        'M': ['manhã'],  # Matemática até 10h50
    },
    4: {  # Sexta-feira
        'G': ['manhã'],  # Geografia até 10h50
        'H': ['manhã'],  # História até 10h50
        'M': ['manhã'],  # Matemática até 10h50
        'C': ['somente']  # Ciências somente na sexta-feira
    }
}
def verificar_sobreposicao(horario):
    pontuacao = 0
    # Iterar sobre os horários de cada série (sub-horários de 30 caracteres)
    sub_horarios = [horario[i:i+30] for i in range(0, len(horario), 30)]
    
    # Iterar sobre cada período (6 aulas por dia, 5 dias por semana)
    for dia in range(5):
        for aula_index in range(6):
            aulas_no_horario = [sub_horario[dia * 6 + aula_index] for sub_horario in sub_horarios]
            # Contar quantas vezes cada aula aparece simultaneamente no mesmo período
            contador_aulas = {}
            for aula in aulas_no_horario:
                if aula in contador_aulas:
                    contador_aulas[aula] += 1
                else:
                    contador_aulas[aula] = 1
            # Penalizar se uma aula ocorrer em mais de uma sala ao mesmo tempo
            for aula, count in contador_aulas.items():
                if count > 1:
                    pontuacao += (count - 1)  # Penaliza pela sobreposição da mesma aula em mais de uma sala
    
    return pontuacao

def fitting(horario):
    # Quantidade desejada de cada aula
    requisitos = {
        'L': 21,
        'E': 3,
        'H': 6,
        'G': 6,
        'C': 6,
        'R': 3,
        'U': 3,
        'I': 15,
        'F': 3,
        'A': 6
    }
    
    # Contar a quantidade de cada letra no horário
    contador = {letra: horario.count(letra) for letra in aula_dict.keys()}
    
    # Calcular a pontuação com base na diferença entre o esperado e o real
    pontuacao = 0

    # Pontos para quantidade total de aulas 
    for aula, qtd_desejada in requisitos.items():
        pontuacao += max(0, abs(qtd_desejada - contador.get(aula, 0)))
    
    # Pontos para quantidade semanal de aulas
    for i in range(0, len(horario), 30):
        sub_horario = horario[i:i+30]
        # Contar a quantidade de cada letra no sub-horário
        contador = {letra: sub_horario.count(letra) for letra in aula_dict.keys()}
        
        # Calcular a pontuação com base na diferença entre o esperado e o real
        for aula, qtd_desejada in requisitos.items():
            qtd_desejada_por_sub = qtd_desejada // 3
            pontuacao += max(0, abs(qtd_desejada_por_sub - contador.get(aula, 0)))
    
        pontuacao += validar_horario(sub_horario, restricoes)     
    pontuacao += verificar_sobreposicao(horario)     
    
    return pontuacao


# Gerar uma lista com 100 strings de 90 caracteres
horarios = gerar_horarios()
lista_fitting = []
# Exibir os 100 horários gerados com suas pontuações
for horario in horarios:
    lista_fitting.append((fitting(horario),horario))

# Ordenar a lista com base na pontuação (melhores pontuações primeiro)
lista_fitting.sort(key=lambda x: x[0])

def crossover(horario1, horario2):
    # Escolher um ponto de corte aleatório
    ponto_corte = random.randint(1, len(horario1) - 1)
    # Fazer o crossover de 1 ponto
    filho1 = horario1[:ponto_corte] + horario2[ponto_corte:]
    filho2 = horario2[:ponto_corte] + horario1[ponto_corte:]
    return filho1, filho2

def mutacao(horario, taxa_mutacao=0.01):
    # Converter o horário em uma lista de caracteres para facilitar a mutação
    horario_list = list(horario)
    for i in range(len(horario_list)):
        if random.random() < taxa_mutacao:
            # Escolher uma nova aula aleatória diferente da atual
            novas_opcoes = [aula for aula in aula_dict.keys() if aula != horario_list[i]]
            horario_list[i] = random.choice(novas_opcoes)
    # Converter a lista de volta para string
    return ''.join(horario_list)

for i in range(100000):  # Loop com 100000 iterações (pode ajustar conforme desejar)
    # Calcular a pontuação de cada horário e armazenar em uma lista
    lista_fitting = []
    for horario in horarios:
        lista_fitting.append((fitting(horario), horario))

    # Ordenar a lista com base na pontuação (melhores pontuações primeiro)
    lista_fitting.sort(key=lambda x: x[0])
    if i == 0:
        pontuacao_menor = lista_fitting[0][0]
    pontuacao_menor_atual = lista_fitting[0][0]
    
    if lista_fitting[0][0] == 0:
        print(f'Geracao {i}, {lista_fitting[0]}')
        break
    elif pontuacao_menor_atual <pontuacao_menor:
        pontuacao_menor = pontuacao_menor_atual
        print(f'Geracao {i}, {lista_fitting[0]}')
    # Pegar os 50 primeiros horários com as melhores pontuações
    melhores_horarios = lista_fitting[:50]
    filhos = []
    
    for i in range(0, len(melhores_horarios), 2):
        if i + 1 < len(melhores_horarios):
            pai1 = melhores_horarios[i][1]
            pai2 = melhores_horarios[i + 1][1]
            filho1, filho2 = crossover(pai1, pai2)
            filhos.extend([filho1, filho2])
    filhos_mutados = [mutacao(filho) for filho in filhos]

    # Gerar outros 50 horários novos
    novos_horarios = gerar_horarios(50)
    # horarios = novos_horarios + filhos_mutados
    melhores_horarios = lista_fitting[:25]
    # horarios = [horario for _, horario in melhores_horarios] + filhos_mutados
    horarios =  filhos_mutados + novos_horarios
