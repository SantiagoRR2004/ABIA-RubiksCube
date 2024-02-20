from problema import Estado, Operador
from typing import TypeVar

N = TypeVar("N", bound="Nodo")

# Nodos a almacenar como parte de los algoritmos de búsqueda


class Nodo:
    def __init__(self, estado: Estado, padre: N) -> None:
        self.estado = estado
        self.padre = padre


# Nodos usados por la BusquedaAnchura.
# Añade el Operador usado para generar el estado almacenado en este Nodo.
# Usado para simplificar la reconstrucción del camino solución.


class NodoAnchura(Nodo):
    def __init__(self, estado: Estado, padre: N, operador: Operador) -> None:
        super().__init__(estado, padre)
        self.operador = operador
