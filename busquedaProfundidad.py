from nodos import NodoAnchura
from busqueda import Busqueda
import time
import traceback


class BusquedaProfundidad(Busqueda):
    # https://en.wikipedia.org/wiki/Depth-first_search

    def dfs(self, node: NodoAnchura, visited: set[NodoAnchura]) -> NodoAnchura:
        """
        This is a recursive implementation of the depth first search

        Args:
            -node: NodoAnchura. The node to start the search from
            -visited: set[NodoAnchura]. The set of visited nodes

        Returns:
            -NodoAnchura. The node that is the solution
                or None if the solution is not found in the time limit
        """
        visited.add(node.estado.cubo.visualizar())

        if node.estado.esFinal():
            return node

        elif time.time() - self.tiempoInicio > self.timeAmount:
            return None

        if len(traceback.extract_stack()) > 100:
            """
            This is not supposed to be in a dfs
            but we use it to avoid:
            RecursionError: maximum recursion depth exceeded in comparison
            This should be used properly
            in the limited depth search
            """
            return None

        for operator in node.estado.operadoresAplicables():
            hijo = node.estado.aplicarOperador(operator)
            if hijo.cubo.visualizar() not in visited:
                result = self.dfs(NodoAnchura(hijo, node, operator), visited)
                if result or (time.time() - self.tiempoInicio > self.timeAmount):
                    return result
        return None

    # Implementa la búsqueda en profundidad.
    # Si encuentra solución recupera la lista de Operadores empleados
    # almacenada en los atributos de los objetos NodoProfundidad
    def solveProblem(self):
        cerrados = set()
        cerrados.add(NodoAnchura(self.inicial, None, None))

        solution = self.dfs(NodoAnchura(self.inicial, None, None), cerrados)

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
