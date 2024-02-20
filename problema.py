# Interfaz genérico para los estados del espacio de estados
from abc import abstractmethod, ABCMeta
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from busqueda import Busqueda
    from problema import Estado, Operador


class Estado(metaclass=ABCMeta):
    # Devuelve el Vector con la lista de Operadores aplicables sobre este Estado
    @abstractmethod
    def operadoresAplicables(self) -> list["Operador"]:
        pass

    # Indica si este es un estado final (solución)
    @abstractmethod
    def esFinal(self) -> bool:
        pass

    @abstractmethod
    # Genera un nuevo Estado resultante de aplicar el Operador indicado
    def aplicarOperador(self, operador: "Operador") -> "Estado":
        pass


# Interfaz para encapsular operadores
class Operador(metaclass=ABCMeta):
    @abstractmethod
    def getEtiqueta(self) -> Any:
        pass

    @abstractmethod
    def getCoste(self) -> int:
        pass


# Clase genérica (indepeniente de estados y algoritmos concretos) que representa un problema de búsqueda en espacio de estados.
# Está caracterizado por un Estado inicial y un método de Busqueda
class Problema:
    def __init__(self, inicial: "Estado", buscador: "Busqueda") -> None:
        self.inicial = inicial
        self.buscador = buscador

    # Aplica el método de Busqueda de este Problema concreto para resolverlo.
    # Devuelve la lista de Operadores que permiten alcanzar un Estado final desde el Estado inicial del Problema
    def obtenerSolucion(self) -> list["Operador"]:
        return self.buscador.buscarSolucion(self.inicial)
