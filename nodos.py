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
