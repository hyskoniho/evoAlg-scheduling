from rich.console import Console
from rich.table import Table
from rich.text import Text

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
        aula_dict: dict = {
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
        
        color_dict: dict = {
            'M': '#FF5733',  # Matemática - cor vibrante (laranja)
            'T': '#9B59B6',  # Mind Makers - roxo criativo
            'F': '#2ECC71',  # Ed. Financeira - verde confiável
            'L': '#3498DB',  # Língua Portuguesa - azul tranquilo
            'H': '#E67E22',  # História - laranja clássico
            'G': '#1ABC9C',  # Geografia - verde água
            'R': '#F39C12',  # Ensino Religioso - amarelo dourado
            'A': '#F1C40F',  # Artes - amarelo brilhante
            'C': '#16A085',  # Ciências - verde esmeralda
            'I': '#2980B9',  # Inglês - azul profundo
            'U': '#8E44AD',  # Música - roxo escuro
            'E': '#E74C3C',  # Educação Física - vermelho forte
        }
        
    elif mode == 'compact':
        aula_dict: dict = {
            'M': 'Matemática',
            'L': 'Língua Portuguesa',
            'H': 'História',
            'C': 'Ciências',
            'R': 'Ensino Religioso',
            'I': 'Inglês',
            'F': 'Educação Física',
            'A': 'Arte',
        }
        
        color_dict: dict = {
            'M': '#FF5733',  # Matemática - cor vibrante (laranja)
            'L': '#3498DB',  # Língua Portuguesa - azul tranquilo
            'H': '#E67E22',  # História - laranja clássico
            'C': '#16A085',  # Ciências - verde esmeralda
            'R': '#F39C12',  # Ensino Religioso - amarelo dourado
            'I': '#2980B9',  # Inglês - azul profundo
            'F': '#E74C3C',  # Educação Física - vermelho forte
            'A': '#8E44AD',  # Artes - amarelo brilhante
        }
        
    console = Console()
    print('\n')
    
    # Definindo os dias da semana e o número de aulas por dia
    dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
    num_aulas_por_dia = 6
    num_turmas = 4

    # Criando tabelas para cada turma
    for turma in range(1, num_turmas + 1):
        table = Table(title=f"Aulas - Turma {turma}", style="bold")
        # Adicionando colunas para os dias da semana
        for dia in dias:
            table.add_column(dia)

        # Criando as linhas para os dias da semana
        for i in range(num_aulas_por_dia):
            aulas_dia = []
            for char in aulas[i:num_aulas_por_dia*len(dias):num_aulas_por_dia]:
                materia = aula_dict[char]
                cor = color_dict[char]
                # Criando um texto colorido para a matéria
                colored_text = Text(materia, style=cor)
                aulas_dia.append(colored_text)
            table.add_row(*aulas_dia)
        
        aulas = aulas[num_aulas_por_dia*len(dias):]

        # Exibindo a tabela da turma
        console.print(table)
        print('\n'*3)

if __name__ == '__main__':
    # Exemplo de string de aulas
    print_table(input("DIGITE O HORARIO: "), "full")