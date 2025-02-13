import openpyxl

def intrvl(s: str, e: str) -> list[str]:    
    return [chr(i) for i in range(ord(s), ord(e) + 1)]

def fill_excel(com_string: str) -> None:
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
    
    com_list: list = list(com_string)
    for i, aula in enumerate(com_list): com_list[i] = aula_dict.get(aula, '')
    turmas: list[list] = [com_list[i:i+30] for i in range(0, len(com_list), 30)]
    ranges: list = [
        # Start_Column, End_Column, Start_Row, Skip_Row, End_Row
        ('B', 'F', 3, 6, 9), # 6
        ('I', 'M', 3, 6, 9), # 7
        ('B', 'F', 13, 16, 19), # 8
        ('I', 'M', 13, 16, 19), # 9
    ]
    
    path: str = r'.\data\best_solution.xlsx'    
    try:
        wb = openpyxl.load_workbook(filename=path)
        sheet = wb['Cola aqui os valores']
        
        for turma, data in zip(turmas, ranges):
            dias = [turma[i:i+6] for i in range(0, len(turma), 6)]
            for column, d in zip(intrvl(data[0], data[1]), dias):
                for row, aula in zip(range(data[2], data[4]), d):
                    if row != data[3]: sheet[f"{column}{row}"] = aula
                
        wb.save(filename=path)
        
    except Exception as e:
        print(e)

if __name__ == "__main__":
    fill_excel("UHHIAATILLLMGFLICCMILLLRGIMEMMLLITCCLLIHAAIHMLRMLFIMMMILGGUEFIAAMMHHUIMLLLIMMRILGGCCLTEILLIMMLLLIMMMCCFIHHLLGGTIRLAAILEU")
