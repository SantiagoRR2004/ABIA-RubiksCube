from problema import Operador, Estado
from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from problemaRubik import EstadoRubik, OperadorRubik
    from cubo import Cubo

# Objeto que implementa la interfaz Estado para un cubo Rubik concreto.
# La mayor parte de los métodos definidos en el interfaz Estado se delegan en el objeto Cubo.

class EstadoRubik(Estado):

    def __init__(self, cubo: "Cubo") -> None:

        self.listaOperadoresAplicables = []
        for m in cubo.movimientosPosibles:
            self.listaOperadoresAplicables.append(OperadorRubik(m))

        self.cubo = cubo

    def operadoresAplicables(self) -> list["OperadorRubik"]:
        return self.listaOperadoresAplicables

    def esFinal(self) -> bool:
        return self.cubo.esConfiguracionFinal()

    def aplicarOperador(self, o: "OperadorRubik") -> "EstadoRubik":
        nuevo = self.cubo.clonar()
        nuevo.mover(o.movimiento)
        return EstadoRubik(nuevo)

    def equals(self, e: "EstadoRubik") -> bool:
        return self.cubo.equals(e.cubo)
    
    def getNumEnFinal(self) -> int:
        """
        Función para la heurística
        Compara el color que tiene que tener cada cara con el color que tiene cada casilla en esa cara.
        Si coincide, está en su posición final y suma 1.
        Finalmente, devuelve el numero de casillas que estan en su lugar.
        """
        n = 0
        for c in self.caras:
            for n in c.casillas:
                if n.color == c.color:
                    n += 1
        return n

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, EstadoRubik):
            return self.equals(other)
        return False


# Implementa el interfaz Operador encapsulando un movimiento (giro) Rubik
class OperadorRubik(Operador):
    def __init__(self, mov: int) -> None:
        self.movimiento = mov

    def getEtiqueta(self) -> int:
        return self.movimiento

    # El coste de los giros es siempre 1 (para la búsqueda todos son idénticos)
    def getCoste(self) -> int:
        return 1

    def opposite(self) -> "OperadorRubik":
        """
        This method returns the opposite operator of the current one
        Because the oparator is stored as an integer and the opposites in
        the cube are like this:

        0 -> 6
        1 -> 7
        2 -> 8
        3 -> 9
        4 -> 10
        5 -> 11

        we only need to add or substract 6
        to the current operator to get the opposite

        Returns:
            -OperadorRubik. The opposite of the current operator
        """
        if self.movimiento < 6:
            return self.__class__(abs(self.movimiento + 6))
        else:
            return self.__class__(abs(self.movimiento - 6))
