from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nodos import Nodo
    from problema import Estado, Operador

# Nodos a almacenar como parte de los algoritmos de búsqueda


class Nodo:
    def __init__(self, estado: "Estado", padre: "Nodo") -> None:
        self.estado = estado
        self.padre = padre


# Nodos usados por la BusquedaAnchura.
# Añade el Operador usado para generar el estado almacenado en este Nodo.
# Usado para simplificar la reconstrucción del camino solución.


class NodoNoInformado(Nodo):
    def __init__(self, estado: "Estado", padre: "Nodo", operador: "Operador") -> None:
        super().__init__(estado, padre)
        self.operador = operador


class NodoInformado(NodoNoInformado):

    def __init__(
        self,
        estado: "Estado",
        padre: "Nodo",
        operador: "Operador",
        coste: float = 0,
        heuristica: float = 0,
    ) -> None:
        """
        Args:
            -estado: Estado. The state of the problem
            -padre: Nodo. The parent of the node
            -operador: Operador. The operator used to generate the state
            -coste: float. The cost of the node
            -heuristica: float. The heuristic of the node

        Returns:
            -None
        """
        super().__init__(estado, padre, operador)
        self.coste = coste
        self.heuristica = heuristica

    def getHeuristica(self) -> float:
        """
        Returns:
            -float. The heuristic of the node
        """
        return self.heuristica

    def getCoste(self) -> float:
        """
        This method returns the cost of the node up
        to the root node. It doesn't return the cost
        of tha last action.

        Returns:
            -float. The cost of the node
        """
        if self.padre == None:
            return self.coste
        return self.coste + self.padre.getCoste()

    def getTotal(self) -> float:
        """
        Returns:
            -float. The total cost of the node
        """
        return self.getCoste() + self.getHeuristica()

    def changeFather(self, newFather: "NodoInformado", newOperator: "Operador") -> None:
        """
        Args:
            -newFather: NodoInformado. The new father of the node
            -newOperator: Operador. The operator used to generate the state
            from the new father to the node

        Returns:
            -None
        """
        self.padre = newFather
        self.operador = newOperator
