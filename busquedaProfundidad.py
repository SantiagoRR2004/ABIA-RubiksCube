from nodos import NodoAnchura
from busqueda import Busqueda
import time


class BusquedaProfundidad(Busqueda):
    # https://en.wikipedia.org/wiki/Depth-first_search

    def solveProblem(self):
        """
        In the end we couldn't use recursion
        because if we change the recursion limit
        with sys.setrecursionlimit(2**31 - 1)
        sometimes the program ends without any output
        and giving no error.

        If we use recursion, we would need to choose an arbitrary
        limit and we already have a limited depth search.

        The correct way of doing it recursively is similar
        to the limited depth search. We just need to ignore
        the number of moves allowed and not remove closed
        nodes from the set of closed nodes.
        """

        cerrados = set()
        solutionFlag = False
        abiertos = []
        abiertos.append(NodoAnchura(self.inicial, None, None))

        while (
            not solutionFlag
            and len(abiertos) > 0
            and time.time() - self.tiempoInicio < self.timeAmount
        ):
            nodoActual = abiertos.pop()

            if nodoActual.estado.esFinal():
                solutionFlag = True

            else:
                for operador in nodoActual.estado.operadoresAplicables():
                    hijo = nodoActual.estado.aplicarOperador(operador)

                    if hijo.cubo.visualizar() not in cerrados:

                        abiertos.append(NodoAnchura(hijo, nodoActual, operador))
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
