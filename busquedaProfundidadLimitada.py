from nodos import NodoNoInformado
from busqueda import Busqueda
import time


class BusquedaProfundidadLimitada(Busqueda):
    # https://es.wikipedia.org/wiki/B%C3%BAsqueda_en_profundidad_limitada
    # https://cube20.org/qtm/

    def ldfs(
        self, node: NodoNoInformado, visited: set[NodoNoInformado], number: int
    ) -> NodoNoInformado:
        """
        This is a recursive implementation of the limited depth first search

        Args:
            -node: NodoAnchura. The node to start the search from
            -visited: set[NodoAnchura]. The set of visited nodes
            -number: int. The number of movements to search

        Returns:
            -NodoAnchura. The node that is the solution
                or None if the solution is not found in the time limit
        """
        visited.add(node.estado.cubo.visualizar())

        if node.estado.esFinal():
            return node

        elif time.time() - self.tiempoInicio > self.timeAmount or number == 0:
            visited.remove(node.estado.cubo.visualizar())
            return None

        for operator in node.estado.operadoresAplicables():
            hijo = node.estado.aplicarOperador(operator)
            if hijo.cubo.visualizar() not in visited:
                self.lenOpened += 1
                result = self.ldfs(
                    NodoNoInformado(hijo, node, operator), visited, number - 1
                )
                if result or (time.time() - self.tiempoInicio > self.timeAmount):
                    return result

        visited.remove(node.estado.cubo.visualizar())
        self.lenOpened -= 1
        self.lenClosed += 1
        return None

    def solveProblem(self):
        cerrados = set()
        number = 26  # 26 is the maximum number of movements to solve the cube
        # Second link in this file
        self.lenClosed = 0
        self.lenOpened = 0

        solution = self.ldfs(
            NodoNoInformado(self.inicial, None, None), cerrados, number
        )

        toret = {
            "lenOpened": self.lenOpened,
            "lenClosed": self.lenClosed,
        }

        if solution:
            toret["solution"] = []
            nodo = solution
            while nodo.padre != None:  # Asciende hasta la raíz
                toret["solution"].insert(0, nodo.operador)
                nodo = nodo.padre
            toret["lenSolution"] = len(toret["solution"])
        else:
            toret["solution"] = None
            toret["lenSolution"] = float("inf")

        return toret
