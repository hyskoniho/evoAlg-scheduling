import random, sys, string, os, inspect
from collections import Counter


REQUISITOS: dict = {'M': 20, 'T': 4, 'F': 4, 'L': 28, 'H': 8, 'G': 8, 'R': 4, 'A': 8, 'C': 8, 'I': 20, 'U': 4, 'E': 4}


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


def quantidade_aulas(horario: str, requisitos: dict = REQUISITOS) -> int:
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
                n += dia.index('I')
            
            # Verifica se tem aula de inglês
            if 'I' not in dia:
                n += 1
            
            # Verifica se o horário de História é após as 10:50
            if 'H' in dia and dia.index('H') >= 4:
                n += dia.index('H')
                
            # Verifica se o horário de Geografia é após as 10:50
            if 'G' in dia and dia.index('G') >= 4:
                n += dia.index('G')
                
            # Verifica se o horário de Educação Física é antes das 9:10
            if 'E' in dia and dia.index('E') < 2:
                n += 1
                
            # Verifica se o dia da educação física não é sexta-feira
            if 'E' in dia and d != 4:
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
    sobreposicoes = sum(10 for chars in contagem.values() if len(chars) > 1)
    
    return sobreposicoes


def fitting(horario: str, requisitos: dict = REQUISITOS) -> int:
    """ Função de fitness"""
    
    return (quantidade_aulas(horario, requisitos) + validar_restricoes(horario) + validar_sobreposicoes(separar_turmas(horario)))
