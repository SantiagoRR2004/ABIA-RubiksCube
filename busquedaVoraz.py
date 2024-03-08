from nodos import NodoInformado
from busqueda import Busqueda
import time
from cubo import Cubo
from problemaRubik import EstadoRubik


class BusquedaVoraz(Busqueda):
    # https://en.wikipedia.org/wiki/Best-first_search

    def __init__(self, heuristic):
        self.heuristic = heuristic

    def solveProblem(self):
        bestValue = self.heuristic(EstadoRubik(Cubo()))
        solutionFlag = False
        abiertos = []
        cerrados = set()
        abiertos.append(
            NodoInformado(
                self.inicial,
                None,
                None,
                0,
                abs(self.heuristic(self.inicial) - bestValue),
            )
        )
        cerrados.add(self.inicial.cubo.visualizar())

        while (
            not solutionFlag
            and len(abiertos) > 0
            and time.time() - self.tiempoInicio < self.timeAmount
        ):
            nodoActual = min(abiertos, key=lambda x: x.getHeuristica())
            abiertos.remove(nodoActual)

            if nodoActual.estado.esFinal():
                solutionFlag = True
            else:

                for operador in nodoActual.estado.operadoresAplicables():
                    hijo = nodoActual.estado.aplicarOperador(operador)

                    if hijo.cubo.visualizar() not in cerrados:

                        abiertos.append(
                            NodoInformado(
                                hijo,
                                nodoActual,
                                operador,
                                0,
                                abs(self.heuristic(hijo) - bestValue),
                            )
                        )
                        cerrados.add(hijo.cubo.visualizar())

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
