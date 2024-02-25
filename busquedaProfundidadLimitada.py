from nodos import NodoAnchura
from busqueda import Busqueda
import time


class BusquedaProfundidadLimitada(Busqueda):
    # https://es.wikipedia.org/wiki/B%C3%BAsqueda_en_profundidad_limitada
    # https://cube20.org/qtm/

    def ldfs(
        self, node: NodoAnchura, visited: set[NodoAnchura], number: int
    ) -> NodoAnchura:
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
            return None

        for operator in node.estado.operadoresAplicables():
            hijo = node.estado.aplicarOperador(operator)
            if hijo.cubo.visualizar() not in visited:
                result = self.ldfs(
                    NodoAnchura(hijo, node, operator), visited, number - 1
                )
                if result or (time.time() - self.tiempoInicio > self.timeAmount):
                    return result
        return None

    def solveProblem(self):
        cerrados = set()
        cerrados.add(NodoAnchura(self.inicial, None, None))
        number = 26  # 26 is the maximum number of movements to solve the cube
        # Second link in this file

        solution = self.ldfs(NodoAnchura(self.inicial, None, None), cerrados, number)

        toret = {
            "lenOpened": 0,
            "lenClosed": len(cerrados),
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
