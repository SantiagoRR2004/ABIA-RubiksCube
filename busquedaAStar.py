from nodos import NodoInformado
from busqueda import Busqueda
import time
from cubo import Cubo
from problemaRubik import EstadoRubik


class BusquedaAStar(Busqueda):
    # https://en.wikipedia.org/wiki/A*_search_algorithm

    def __init__(self, heuristic):
        self.heuristic = heuristic

    def solveProblem(self):
        bestValue = self.heuristic(EstadoRubik(Cubo()))
        solutionFlag = False
        abiertos = []
        cerrados = []
        initial = NodoInformado(
            self.inicial,
            None,
            None,
            1,
            abs(self.heuristic(self.inicial) - bestValue),
        )

        abiertos.append(initial)
        cerrados.append(initial)

        while (
            not solutionFlag
            and len(abiertos) > 0
            and time.time() - self.tiempoInicio < self.timeAmount
        ):
            nodoActual = min(abiertos, key=lambda x: x.getTotal())
            abiertos.remove(nodoActual)

            if nodoActual.estado.esFinal():
                solutionFlag = True

            else:
                for operador in nodoActual.estado.operadoresAplicables():
                    descendant = nodoActual.estado.aplicarOperador(operador)

                    if descendant not in [x.estado for x in cerrados]:
                        newNode = NodoInformado(
                            descendant,
                            nodoActual,
                            operador,
                            1,
                            abs(self.heuristic(descendant) - bestValue),
                        )

                        abiertos.append(newNode)
                        cerrados.append(newNode)

                    else:
                        previous = [x for x in cerrados if x.estado == descendant][0]
                        if previous.getCoste() > nodoActual.getCoste() + 1:
                            # We change the the older father for one with less cost
                            previous.changeFather(nodoActual, operador)

        toret = {
            "lenOpened": len(abiertos),
            "lenClosed": max(0, len(cerrados) - len(abiertos)),
        }

        if solutionFlag:
            toret["solution"] = []
            nodo = nodoActual
            while nodo.padre != None:  # Asciende hasta la raíz
                toret["solution"].insert(0, nodo.operador)
                nodo = nodo.padre
            toret["lenSolution"] = len(toret["solution"])
        else:
            toret["solution"] = None
            toret["lenSolution"] = float("inf")

        return toret
