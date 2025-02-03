from rich.console import Console
from rich.table import Table

def print_table(aulas: str | list[str], mode: str = "full") -> None:
    """ 
    Cria tabelas de aulas a partir de uma string de aulas

    >>> Args:
        aulas (str | list[str]): String de aulas
        mode (str): Modo de exibição das aulas ("full", "compact")
    """
    
    if isinstance(aulas, list): aulas = ''.join(aulas)
    assert mode in ['full', 'compact'], "Modo de exibição inválido"
    
    if mode == 'full':
        aula_dict = {
            'M': 'Matemática',
            'T': 'Mind Makers',
            'F': 'Ed. Financeira',
            'L': 'Língua Portuguesa',
            'H': 'História',
            'G': 'Geografia',
            'R': 'Ensino Religioso',
            'A': 'Artes',
            'C': 'Ciências',
            'I': 'Inglês',
            'U': 'Música',
            'E': 'Educação Física',
        }
        
    elif mode == 'compact':
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
        
    console = Console()
    
    # Definindo os dias da semana e o número de aulas por dia
    dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
    num_aulas_por_dia = 6
    num_turmas = 4

    # Criando tabelas para cada turma
    for turma in range(1, num_turmas + 1):
        table = Table(title=f"Aulas - Turma {turma}")
        # Adicionando colunas para os dias da semana
        for dia in dias:
            table.add_column(dia)

        # Criando as linhas para os dias da semana
        for i in range(num_aulas_por_dia):
            # aulas_dia = [char for char in ]
            
            # inicio = (i * num_aulas_por_dia) + (turma - 1) * (num_aulas_por_dia * len(dias))
            aulas_dia = [aula_dict[char] for char in aulas[i:num_aulas_por_dia*len(dias):num_aulas_por_dia]]
            table.add_row(*aulas_dia)
        
        aulas = aulas[num_aulas_por_dia*len(dias):]

        # Exibindo a tabela da turma
        console.print(table)
        print('\n'*3)

if __name__ == '__main__':
    # Exemplo de string de aulas
    print_table(input("DIGITE O HORARIO: "), "full")