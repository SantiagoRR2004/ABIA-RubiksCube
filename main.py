import sys
from cubo import Cubo
from problemaRubik import EstadoRubik
from busquedaAnchura import BusquedaAnchura
from busquedaProfundidad import BusquedaProfundidad
from busquedaProfundidadIterativa import BusquedaProfundidadIterativa
from problema import Problema


def multipleSearches(algorithms: dict, numMovs: int = 1, maxTime: int = 60) -> dict:
    """
    Args:
        -algorithms: dict. A dictionary with the algorithms to use
        -numMovs: int. The number of movements to shuffle the cube
        -maxTime: int. The maximum amount of time to solve the problem

    Returns:
        -dict. A dictionary with the results of the searches
        as the keys the names of the algorithms and as the values
        the results of the searches
    """
    cubo = Cubo()
    movsMezcla = cubo.mezclar(numMovs)
    toret = {}

    for name, algorithm in algorithms.items():
        newCube = Cubo()
        for movement in movsMezcla:
            newCube.mover(movement)
        problem = Problema(EstadoRubik(newCube), algorithm)
        solution = problem.obtenerSolucion(maxTime)
        toret[name] = solution
    return toret


if __name__ == "__main__":
    movs = 2
    if len(sys.argv) > 1:
        movs = int(sys.argv[1])

    opsSolucion = multipleSearches(
        {
            "Anchura": BusquedaAnchura(),
            "Profundidad": BusquedaProfundidad(),
            "ProfundidadIterativa": BusquedaProfundidadIterativa(),
        },
        movs,
    )

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
