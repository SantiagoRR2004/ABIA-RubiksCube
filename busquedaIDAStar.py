from collections import deque
from nodos import NodoInformado
from busqueda import Busqueda
import time
from cubo import Cubo
from problemaRubik import EstadoRubik


class BusquedaIDAStar(Busqueda):
    # https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search

    def __init__(self, heuristic) -> None:
        self.heuristic = heuristic

    def ldfs(
        self, node: NodoInformado, cota: int, bestValue: int
    ) -> NodoInformado:
        f = node.getTotal()
        if f > cota:
            return f

        if node.estado.esFinal():
            return node

        elif time.time() - self.tiempoInicio > self.timeAmount:
            return None
        
        min = 99999

        for operator in node.estado.operadoresAplicables():
            hijo = node.estado.aplicarOperador(operator)
            newNode = NodoInformado(
                hijo,
                node,
                operator,
                1,
                abs(self.heuristic(hijo) - bestValue),
            )
            newNode_cota = newNode.getTotal()
            result = self.ldfs(
                newNode, cota, bestValue,
            )
            if type(result) != int or (time.time() - self.tiempoInicio > self.timeAmount):
                return result
            elif result < min:
                min = result

        return min

    def solveProblem(self):
        bestValue = self.heuristic(EstadoRubik(Cubo()))

        solution = None
        #path = deque()
        #path.append()

        cota = abs(self.heuristic(self.inicial) - bestValue)
        self.lenClosed = [0]
        while time.time() - self.tiempoInicio < self.timeAmount:
            solution = self.ldfs(
                NodoInformado(self.inicial, None, None, 1,
                abs(self.heuristic(self.inicial) - bestValue),), 
                cota, bestValue,
            )
            if type(solution) == int:
                if solution == 99999:
                    solution = None
                    break
                cota = solution
            elif solution.estado.esFinal():
                break

        toret = {
            "lenOpened": 0,
            "lenClosed": 0,
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
