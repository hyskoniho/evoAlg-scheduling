from Heuristic import *
from Tools import print_table, fill_excel
from ptymer import Timer
from multiprocessing import freeze_support, cpu_count
from concurrent.futures import ProcessPoolExecutor, as_completed

# Genetic Algorithm
POPULATION_SIZE = 2000
NUM_GENERATIONS = 10000000
MATE_RATE = 0.7
BASE_MUTATION_RATE = 0.01
MUTATION_RATE = BASE_MUTATION_RATE
MUTATION_ADJUSTMENT = 0.0025

# Simulated Annealing
INITIAL_TEMP = 1000
COOLING_RATE = 0.95
MAX_ITERATIONS = 300000


def parallel_annealing(quantity: int,
                       initial_solution: str | list[str],
                       initial_temp: int,
                       cooling_rate: float,
                       max_iterations: int) -> tuple[str | list[str],
                                                     int | float]:
    with ProcessPoolExecutor() as executor:
        futures: list = [
            executor.submit(
                simulated_annealing,
                initial_solution,
                initial_temp,
                cooling_rate,
                max_iterations) for _ in range(quantity)]
        results: list = [future.result() for future in as_completed(futures)]
    return sorted(results, key=lambda x: x[1])[0]


@Timer(visibility=True)
def main() -> None:
    try:
        fit: float | int = float('inf')
        dude: str | list[str] = ''

        dude, fit = genetic_algorithm(
            pop_size=POPULATION_SIZE,
            num_generations=NUM_GENERATIONS,
            base_mutation_rate=BASE_MUTATION_RATE,
            mutation_adjustment=MUTATION_ADJUSTMENT,
            mutation_rate=MUTATION_RATE,
            mating_rate=MATE_RATE
        )

        cristal_i: int = 0
        while fit >= -0.35:
            print(f"[S-{cristal_i}] Starting Simulated Annealing!")
            dude, fit = parallel_annealing(
                quantity=cpu_count(),
                initial_solution=dude,
                initial_temp=INITIAL_TEMP,
                cooling_rate=COOLING_RATE,
                max_iterations=MAX_ITERATIONS
            )
            print(f"[S-{cristal_i}] Fit: {fit} | Individual: {dude}")
            cristal_i += 1

    except KeyboardInterrupt:
        if dude:
            pass
        else:
            raise KeyboardInterrupt("No solution found yet!")

    except Exception as e:
        raise e

    print("Best solution:", dude)
    print("Fit:", fit)
    print_table(dude)

    with open(r'./data/best_solution.txt', 'w') as f:
        f.write(dude)
    fill_excel(dude)


if __name__ == '__main__':
    freeze_support()
    main()
