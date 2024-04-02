import sys
from cubo import Cubo
from busquedas import allSearchTypes
from utils import multipleSearches

if __name__ == "__main__":
    movs = 4
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
        print(f"{name}{' '*(maxLength-len(name))} branching factor {solution['EBF']}")

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
