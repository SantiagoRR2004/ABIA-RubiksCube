from nodos import NodoNoInformado
from busqueda import Busqueda
import time
from cubo import Cubo
from problemaRubik import EstadoRubik


class BusquedaSimpleHillClimbing(Busqueda):
    # https://en.wikipedia.org/wiki/Hill_climbing

    def __init__(self, heuristic):
        self.heuristic = heuristic

    def solveProblem(self):

        bestValue = self.heuristic(EstadoRubik(Cubo()))
        solutionFlag = False
        stuckFlag = False
        nodoActual = NodoNoInformado(self.inicial, None, None)
        heuristicValue = abs(self.heuristic(nodoActual.estado) - bestValue)
        lenOpened = 0
        lenClosed = 0

        while (
            not solutionFlag
            and not stuckFlag
            and time.time() - self.tiempoInicio < self.timeAmount
        ):
            if nodoActual.estado.esFinal():
                solutionFlag = True

            else:
                foundNext = False
                for operador in nodoActual.estado.operadoresAplicables():
                    estadoHijo = nodoActual.estado.aplicarOperador(operador)
                    lenOpened += 1

                    if abs(self.heuristic(estadoHijo) - bestValue) < heuristicValue:
                        nodoActual = NodoNoInformado(estadoHijo, nodoActual, operador)
                        heuristicValue = abs(self.heuristic(estadoHijo) - bestValue)
                        foundNext = True
                        break  # Es lo unico que cambia con respecto a la busquedaSteepestHillClimbing

                if not foundNext:
                    lenClosed += 1
                    lenOpened -= 1
                    stuckFlag = True

        toret = {
            "lenOpened": lenOpened,
            "lenClosed": lenClosed,
        }

        if solutionFlag:
            toret["solution"] = []
            nodo = nodoActual
            while nodo.padre != None:
                toret["solution"].insert(0, nodo.operador)
                nodo = nodo.padre
            toret["lenSolution"] = len(toret["solution"])
        else:
            toret["solution"] = None
            toret["lenSolution"] = float("inf")

        return toret
