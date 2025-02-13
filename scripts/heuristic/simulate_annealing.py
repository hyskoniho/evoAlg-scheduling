from fitting_function import *
import random
import os
import sys
import math
from ptymer import Timer

sys.path.append(os.path.abspath(os.path.join('./scripts', 'fitting')))

# Get close neighbor


def get_neighbor(solution):
    idx1, idx2 = random.sample(range(len(solution)), 2)
    neighbor = list(solution)
    neighbor[idx1], neighbor[idx2] = neighbor[idx2], neighbor[idx1]
    return ''.join(neighbor)

# Simulated Annealing Function


def simulated_annealing(initial_solution: str,
                        initial_temp: int,
                        cooling_rate: float,
                        max_iterations: int) -> tuple[str | list[str],
                                                      int | float]:
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
            acceptance_probability = math.exp(
                (current_score - neighbor_score) / temperature)

            if random.random() < acceptance_probability:
                current_solution = neighbor_solution
                current_score = neighbor_score

        # Resfriamento
        temperature *= cooling_rate

        # Se a nota for 0, encontramos a solução perfeita
        if best_score == -0.56:
            break

    return best_solution, best_score


if __name__ == "__main__":

    # Parâmetros do algoritmo
    initial_temp = 1000
    cooling_rate = 0.95
    max_iterations = 500000

    initial_solution = 'TLIUAAFIGGCCMMMIRMHHILLLIMLLLELIGGMMIMMMFTLILHLRLLHICCLUEIAAIMMLLLHHIAALGLILCCFILGTRUIMEMMAALICCLLLILUIGGMMLIMMMRFHHITEL'
    best_solution, best_score = simulated_annealing(
        initial_solution, initial_temp, cooling_rate, max_iterations)

    print("Melhor solução encontrada:", best_solution)
    print("Nota da melhor solução:", best_score)
