import random, inspect
from collections import Counter


REQUISITOS: dict = {'M': 5, 'T': 1, 'F': 1, 'L': 7, 'H': 2, 'G': 2, 'R': 1, 'A': 2, 'C': 2, 'I': 5, 'U': 1, 'E': 1}


def separar_turmas(horario: str, quantidade_turmas: int = 4) -> list[str]:
    """ Separa o horário em turmas
    
    Args:
        horario (str): Horário das aulas
        quantidade_turmas (int, optional): Quantidade de turmas. Defaults to 4.
    
    Returns:
        list[str]: Lista de horários separados por turma
    """
    tamanho_grupo = len(horario) // quantidade_turmas
    turmas = []
    for i in range(quantidade_turmas):
        inicio = i * tamanho_grupo
        fim = inicio + tamanho_grupo
        turmas.append(horario[inicio:fim])
        
    return turmas


def separar_dias(turma: str) -> list[list[str]]:
    """ Separa a turma em dias
    
    Args:
        turma (str): Horário de uma turma
    
    Returns:
        list[list[str]]: Lista de horários separados por dia
    """
    dias: list[list[str]] = [['' for _ in range(6)] for _ in range(5)]
    
    for i, aula in enumerate(turma):
        dias[i // 6][i % 6] = aula
    
    return [''.join(dia) for dia in dias]


def quantidade_aulas(horario: str, quantidade: int = 1, requisitos: dict = REQUISITOS) -> int:
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

    nota_quantidade: int =  sum( # Somatório
        abs( # Valor absoluto para obter a diferença entre a quantidade de aulas esperada e a quantidade de aulas no horário
            (requisitos[materia]*quantidade) - c.get(materia, 0) # Quantidade esperada daquela matéria - Quantidade de aulas daquela matéria no horário
        ) \
            for materia in requisitos # Aplica a operação para cada matéria, e soma o resultado
    )
    
    return nota_quantidade


def bonus_aula_dupla(hdia: str | list[str]) -> float:
    """ Verifica se há aulas duplas
    
    Args:
        hdia (str | list[str]): Horário de um dia
    
    Returns:
        float: Bônus por aula dupla
    """
    bonus: float = 0.00
    ultima: str = ''
    i: int = 0
    
    for aula in hdia:
        if aula == ultima:
            if i <= 1:
                bonus += 0.01
            else:
                bonus -= 1.01
                
            i+=1
            
        else:
            i = 0
            
        ultima = aula
        
    return round(bonus, 2)


def validar_restricoes(horario: str) -> int:
    """ Verifica se o horário atende as restrições"""
    # TODO:  Somar a distância entre o horário esperado x horário anotado pois incentiva mais a aproximação do horário esperado
    
    nota_restricoes: int = 0
    for turma in separar_turmas(horario):
        nota_restricoes+= quantidade_aulas(turma)
        for d, dia in enumerate(separar_dias(turma)):
            if any (dia.count(aula) > 3 for aula in dia):
                nota_restricoes += 1
            nota_restricoes -= bonus_aula_dupla(dia)
            
            # Verifica se o horário da aula de inglês é após as 10:50
            if 'I' in dia and dia.find('I', 4) >= 4:
                nota_restricoes += dia.find('I', 4)
            
            # Verifica se tem aula de inglês
            if 'I' not in dia:
                nota_restricoes += 1
            
            # Verifica se o horário de História é após as 10:50
            if 'H' in dia and dia.find('H', 4) >= 4:
                nota_restricoes += dia.find('H', 4)
                
            # Verifica se o horário de Geografia é após as 10:50
            if 'G' in dia and dia.find('G', 4) >= 4:
                nota_restricoes += dia.find('G', 4)
                
            # Verifica se o horário de Educação Física é antes das 9:10
            if 'E' in dia and dia.find('E', 0, 2) <= 1 and dia.find('E', 0, 2) != -1:
                nota_restricoes += 1
                
            # Verifica se o dia da educação física não é sexta-feira
            if 'E' in dia and d != 4:
                nota_restricoes += 1
                
            # Verifica se o dia de Artes é segunda-feira, terça-feira ou sexta-feira
            if 'A' in dia and d not in [0, 1, 4]:
                nota_restricoes += sum(1 for aula in dia if aula == 'A')
            
            # Verifica se o dia de Música é segunda-feira, terça-feira ou sexta-feira
            if 'U' in dia and d not in [0, 1, 4]:
                nota_restricoes += sum(1 for aula in dia if aula == 'U')

    return nota_restricoes


def validar_sobreposicoes(strings: list[str]) -> int:
    strings = [string.replace('T', 'M').replace('F', 'M')\
                .replace('G', 'H')\
                .replace('A', 'U') for string in strings]
    
    chars = set(list(''.join(strings)))
    positions = {char: {num: {} for num in range(5)} for char in chars}
    nota_sobreposicoes: int = 0
    
    for i, turma in enumerate(strings):
        for j, dia in enumerate(separar_dias(turma)):
            for k, aula in enumerate(dia):
                if positions[aula][j] and k not in positions[aula][j]:
                    positions[aula][j].add(k)
                elif positions[aula][j] and k in positions[aula][j]:
                    nota_sobreposicoes += 1
                else:
                    positions[aula][j] = {k}
    
    return nota_sobreposicoes


def fitting(horario: str, requisitos: dict = REQUISITOS) -> int:
    """ Função de fitness"""
    
    return round((quantidade_aulas(horario, 4, requisitos) + validar_restricoes(horario) + validar_sobreposicoes(separar_turmas(horario))), 2)
