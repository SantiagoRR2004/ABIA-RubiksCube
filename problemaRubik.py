from problema import Operador, Estado
from typing import TYPE_CHECKING


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


# Implementa el interfaz Operador encapsulando un movimiento (giro) Rubik
class OperadorRubik(Operador):
    def __init__(self, mov: int) -> None:
        self.movimiento = mov

    def getEtiqueta(self) -> int:
        return self.movimiento

    # El coste de los giros es siempre 1 (para la búsqueda todos son idénticos)
    def getCoste(self) -> int:
        return 1
