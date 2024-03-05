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

        # https://www.cs.princeton.edu/courses/archive/fall06/cos402/papers/korfrubik.pdf
        En la página 2 abajo a la derecha se explica esta heurística.

        Cogemos el máximo de del numero de movimientos de las aristas/4 y las esquinas/4
        porque es lo que pone en el paper.
        """

        oppositeColors = {0: 5, 1: 3, 2: 4, 3: 1, 4: 2, 5: 0}

        movesCorners = 0

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
            a = self.cubo.caras[corner[0][0]].casillas[corner[0][1]].color
            b = self.cubo.caras[corner[1][0]].casillas[corner[1][1]].color
            c = self.cubo.caras[corner[2][0]].casillas[corner[2][1]].color

        """
        I am going to explain how to calculate the minimum number of movements
        to place an edge in its correct position

        Any edge can be in 24 different positions+orientations but we
        can divide this number into 4 groups. Once the edge fits 
        in one of these groups it isn't added to the next 
        groups even if it fits in them too.

        The first group is the one where at least one of the colors
        of the edge lays with its face color. This group has 7.

        The second group is the one where at least one of the colors
        of the edge lays with the color of the face of the other color
        of the edge. This group has 7.

        The third group is the one where at least one of the colors
        of the edge lays with its inversed face color. This group has 5.

        The final group is the one where at least one of the colors
        of the edge lays with the inverse color of the face of the other color
        of the edge. This group has 5.

        All add up to 24.

        So let us call a to the a color of the edge and b to the other.
        We will call A to the color of the face of a and B to the color
        of the face of b. And A' and B' to the inverse colors of A and B.

        The following has been tested by using a real cube.

        When a∈A:
            -If b∈B:        0 movements
            -If b∈B':       2 movements
            -Else:          1 movement

        When a∈B:
            -If b∈A:        3 movements
            -If b∈A':       3 movements
            -Else:          2 movements

        When a∈A':
            -If b∈B:        2 movements     # Equivalent to a∈A and b∈B'
            -If b∈B':       4 movements
            -Else:          3 movements


        When a∈B': # This is going to be an else
            -If b∈A:        3 movements     # Equivalent to a∈B and b∈A'
            -If b∈A':       3 movements
            -Else:          2 movements

        """
        movesEdges = 0

        edgesPositions = [
            [(0, 1), (4, 7)],
            [(0, 3), (1, 2)],
            [(0, 5), (3, 2)],
            [(0, 7), (2, 2)],
            [(1, 5), (2, 3)],
            [(2, 5), (3, 3)],
            [(3, 5), (4, 3)],
            [(4, 5), (1, 3)],
            [(5, 1), (2, 7)],
            [(5, 3), (1, 7)],
            [(5, 5), (3, 7)],
            [(5, 7), (4, 7)],
        ]

        for edge in edgesPositions:
            a = self.cubo.caras[edge[0][0]].casillas[edge[0][1]].color
            b = self.cubo.caras[edge[1][0]].casillas[edge[1][1]].color
            A = self.cubo.caras[edge[0][0]].color
            B = self.cubo.caras[edge[1][0]].color

            if a == A or b == B:
                if a == A and b == B:
                    movesEdges += 0
                elif a == oppositeColors[A] or b == oppositeColors[B]:
                    movesEdges += 2
                else:
                    movesEdges += 1

            elif a == B or b == A:
                if a == B and b == A:
                    movesEdges += 3
                elif a == oppositeColors[B] or b == oppositeColors[A]:
                    movesEdges += 3
                else:
                    movesEdges += 2

            elif a == oppositeColors[A] or b == oppositeColors[B]:
                if a == oppositeColors[A] and b == oppositeColors[B]:
                    movesEdges += 4
                else:
                    movesEdges += 3

            else:
                if a == oppositeColors[B] and b == oppositeColors[A]:
                    movesEdges += 3
                else:
                    movesEdges += 2

        return max(movesCorners / 4, movesEdges / 4)


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
    c.mezclar(1)
    print(c.visualizar())
    print(e.manhattanDistance())
