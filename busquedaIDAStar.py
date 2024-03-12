from nodos import NodoInformado
from busqueda import Busqueda
import time
from cubo import Cubo
from problemaRubik import EstadoRubik


class BusquedaIDAStar(Busqueda):

    def __init__(self, heuristic) -> None:
        self.heuristic = heuristic
        self.newCota = 99999

    def ldfs(
        self, node: NodoInformado, cota: float, bestValue: int
    ) -> NodoInformado:
        f = node.getTotal()

        if f > cota:
            if f < self.newCota:
                self.newCota = f
            return None

        if node.estado.esFinal():
            return node

        elif time.time() - self.tiempoInicio > self.timeAmount:
            return None

        for operator in node.estado.operadoresAplicables():
            hijo = node.estado.aplicarOperador(operator)
            newNode = NodoInformado(
                hijo,
                node,
                operator,
                1,
                abs(self.heuristic(hijo) - bestValue),
            )
            result = self.ldfs(
                newNode, cota, bestValue,
            )
            if result or (time.time() - self.tiempoInicio > self.timeAmount):
                return result

        return None

    def solveProblem(self):
        bestValue = self.heuristic(EstadoRubik(Cubo()))
        node_initial = NodoInformado(self.inicial, None, None, 1,
                                     abs(self.heuristic(self.inicial) - bestValue),
                                    )
        solution = None

        self.newCota = node_initial.getTotal()

        while time.time() - self.tiempoInicio < self.timeAmount and not solution:
            cota = self.newCota
            self.newCota = 99999
            solution = self.ldfs(
                node_initial, cota, bestValue,
            )

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
