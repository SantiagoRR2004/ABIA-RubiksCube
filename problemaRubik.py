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

    def matchingFaceColor(self) -> int:
        """
        Función para la heurística
        Compara el color que tiene que tener cada cara con el color que tiene cada casilla en esa cara.
        Si coincide, está en su posición final y suma 1.
        Finalmente, devuelve el numero de casillas que estan en su lugar.
        """
        n = 0
        for cara in self.cubo.caras:
            for casilla in cara.casillas:
                if casilla.color == cara.color:
                    n += 1
        return n

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, EstadoRubik):
            return self.equals(other)
        return False

    def manhattanDistance(self) -> int:
        """
        Función para la heurística
        Calcula la distancia de manhattan de cada casilla a su posición final.
        """

        colors = {"W": 0, "Y": 1, "O": 2, "R": 3, "G": 4, "B": 5}
        rcolors = {v: k for k, v in colors.items()}

        # Each corner has the face and then the number on the face

        corners = [
            [(0, 0), (1, 0), (4, 2)],
            [(0, 2), (3, 2), (4, 0)],
            [(0, 6), (1, 2), (2, 0)],
            [(0, 8), (2, 2), (3, 0)],
            [(5, 0), (1, 8), (2, 6)],
            [(5, 2), (2, 8), (3, 6)],
            [(5, 6), (1, 6), (4, 8)],
            [(5, 8), (3, 8), (4, 6)],
        ]

        for corner in corners:
            a = rcolors[self.cubo.caras[corner[0][0]].casillas[corner[0][1]].color]
            b = rcolors[self.cubo.caras[corner[1][0]].casillas[corner[1][1]].color]
            c = rcolors[self.cubo.caras[corner[2][0]].casillas[corner[2][1]].color]
            print(f"corner: {a}{b}{c}")

        # Así encontramos las esquinas W
        # for cara in self.cubo.caras:
        #     for casilla in cara.casillas:
        #         # print(casilla.posicionCorrecta, casilla.color)
        #         if casilla.color == colors["W"] and casilla.posicionCorrecta in [0,2,6,8]:
        #             print("found a W corner")


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


if __name__ == "__main__":
    from cubo import Cubo

    c = Cubo()
    e = EstadoRubik(c)
    print(c.visualizar())
    print(e.manhattanDistance())
