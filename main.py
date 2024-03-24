import sys, csv
from cubo import Cubo
from busquedas import allSearchTypes
from problemaRubik import EstadoRubik
from problema import Problema
from typing import List, Tuple
import ast
from concurrent.futures import ProcessPoolExecutor


# Define a function to run the algorithm for a single algorithm
def run_algorithm(name, algorithm, movsMezcla, maxTime):
    newCube = Cubo()
    for movement in movsMezcla:
        newCube.mover(movement)
    problem = Problema(EstadoRubik(newCube), algorithm)
    return problem.obtenerSolucion(maxTime)


def multipleSearches(
    algorithms: dict, numMovs: int = 1, maxTime: int = 60, fileToCheck: str = None
) -> Tuple[dict, List[int]]:
    """
    Args:
        -algorithms: dict. A dictionary with the algorithms to use
        -numMovs: int. The number of movements to shuffle the cube
        -maxTime: int. The maximum amount of time to solve the problem
        -fileToCheck: str. The name of the file to check if the movements have been made before

    Returns:
        -dict. A dictionary with the results of the searches
        as the keys the names of the algorithms and as the values
        the results of the searches
        -List[int]. A list with the movements that were made to shuffle the cube
    """
    cubo = Cubo()
    movsMezcla = cubo.mezclar(numMovs)
    if fileToCheck:
        with open(fileToCheck, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            olderMoves = [
                ast.literal_eval(x["moves"]) for x in reader if x["moves"] != ""
            ]
        if movsMezcla in olderMoves:
            return {}, movsMezcla

    toret = {}

    with ProcessPoolExecutor() as executor:
        # Submit each algorithm to the executor
        futures = {
            executor.submit(run_algorithm, name, algorithm, movsMezcla, maxTime): name
            for name, algorithm in algorithms.items()
        }

        # Collect results as they become available
        for future in futures:
            name = futures[future]
            toret[name] = future.result()

    return toret, movsMezcla


if __name__ == "__main__":
    movs = 1
    if len(sys.argv) > 1:
        movs = int(sys.argv[1])

    opsSolucion, moves = multipleSearches(allSearchTypes(), movs, 10)

    maxLength = max([len(x) for x in opsSolucion.keys()])

    for name, solution in opsSolucion.items():
        if solution["solution"] != None:
            print(
                f"{name}{' '*(maxLength-len(name))} managed to solve it in {solution['lenSolution']} steps"
            )
        else:
            print(
                f"{name}{' '*(maxLength-len(name))} couldn't solve it in the given time"
            )

    print()
    for name, solution in opsSolucion.items():
        print(
            f"{name}{' '*(maxLength-len(name))} occupied max {solution['maxMemory']} bytes"
        )

    print()
    for name, solution in opsSolucion.items():
        print(
            f"{name}{' '*(maxLength-len(name))} lasted {solution['time']:.2f} seconds"
        )

    print()
    for name, solution in opsSolucion.items():
        print(
            f"{name}{' '*(maxLength-len(name))} length of closed was {solution['lenClosed']}"
        )

    print()
    for name, solution in opsSolucion.items():
        print(
            f"{name}{' '*(maxLength-len(name))} length of opened was {solution['lenOpened']}"
        )

    print()
    for name, solution in opsSolucion.items():
        if solution["solution"]:
            moves = [
                Cubo().visualizarMovimiento(o.getEtiqueta())
                for o in solution["solution"]
            ]
            moves = [word.ljust(2) for word in moves]
            print(f"{name}{' '*(maxLength-len(name))} moves were {' '.join(moves)}")
