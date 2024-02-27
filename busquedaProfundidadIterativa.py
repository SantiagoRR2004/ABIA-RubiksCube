from nodos import NodoAnchura
from busqueda import Busqueda
import time


class BusquedaProfundidadIterativa(Busqueda):
    # https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search

    def __init__(self, step: int = 1) -> None:
        """
        The step is the amount of movements to increase the depth of the search
        if you don't specify it, it will be 1

        Args:
            -step: int. The amount of movements to increase the depth of the search"""
        self.step = step

    def ldfs(
        self, node: NodoAnchura, visited: set[NodoAnchura], number: int
    ) -> NodoAnchura:
        """
        This is the same as the ./busquedaProfundidadLimitada.py file
        """
        visited.add(node.estado.cubo.visualizar())
        self.lenClosed[0] += 1

        if node.estado.esFinal():
            return node

        elif time.time() - self.tiempoInicio > self.timeAmount or number == 0:
            visited.remove(node.estado.cubo.visualizar())
            return None

        for operator in node.estado.operadoresAplicables():
            hijo = node.estado.aplicarOperador(operator)
            if hijo.cubo.visualizar() not in visited:
                result = self.ldfs(
                    NodoAnchura(hijo, node, operator), visited, number - 1
                )
                if result or (time.time() - self.tiempoInicio > self.timeAmount):
                    return result

        visited.remove(node.estado.cubo.visualizar())
        return None

    def solveProblem(self):
        solution = None

        maxDepth = 0
        self.lenClosed = [0]
        while time.time() - self.tiempoInicio < self.timeAmount and not solution:
            cerrados = set()
            solution = self.ldfs(
                NodoAnchura(self.inicial, None, None), cerrados, maxDepth
            )
            maxDepth += self.step

        toret = {
            "lenOpened": 0,
            "lenClosed": self.lenClosed[0],
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
