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

    def matchingFaceColor(
        self, inv: bool = False, objective: "EstadoRubik" = None
    ) -> int:
        """
        Función para la heurística
        Compara el color que tiene que tener cada cara con el color que tiene cada casilla en esa cara.
        Si coincide, está en su posición final y suma 1.
        Finalmente, devuelve el numero de casillas que estan en su cara correcta.

        Args:
            -inv: bool. If we are going to compare with the objective
            if false, with the solved cube
            -objective: EstadoRubik. The objective to compare with
        """
        n = 0
        if not inv:
            for cara in self.cubo.caras:
                for casilla in cara.casillas:
                    if casilla.color == cara.color:
                        n += 1

        else:  # We are going to compare the colors with the objective
            for index, cara in enumerate(self.cubo.caras):
                """
                We count the colors of each face of
                the objective. Then we check the number of squares
                that match for each face of the cube"""
                objColors = {x: 0 for x in range(6)}
                for casilla in objective.cubo.caras[index].casillas:
                    objColors[casilla.color] += 1

                for casilla in cara.casillas:
                    if objColors[casilla.color] > 0:
                        n += 1
                        objColors[casilla.color] -= 1

        return n

    def matchingCorrectPosition(
        self, inv: bool = False, objective: "EstadoRubik" = None
    ) -> int:
        """
        Función para la heurística
        Compara si una casilla está en la cara correcta y en su posición adecuada.
        Si es el caso, suma 1
        Finalmente, obtenemos el número de casillas bien colocadas

        Args:
            -inv: bool. If we are going to compare with the objective
            if false, with the solved cube
            -objective: EstadoRubik. The objective to compare with
        """
        n = 0
        if not inv:
            for cara in self.cubo.caras:
                for i in range(0, 9):
                    casilla = cara.casillas[i]
                    if casilla.color == cara.color and casilla.posicionCorrecta == i:
                        n += 1

        else:
            for indexCara, cara in enumerate(self.cubo.caras):
                for indexCas, casilla in enumerate(cara.casillas):
                    if (
                        casilla.color
                        == objective.cubo.caras[indexCara].casillas[indexCas].color
                    ) and (
                        casilla.posicionCorrecta
                        == objective.cubo.caras[indexCara]
                        .casillas[indexCas]
                        .posicionCorrecta
                    ):
                        n += 1

        return n

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, EstadoRubik):
            return self.equals(other)
        return False

    def getMovesEdges(self) -> int:
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
        oppositeColors = {0: 5, 1: 3, 2: 4, 3: 1, 4: 2, 5: 0}
        movesEdges = 0

        edgesPositions = [
            [(0, 1), (4, 1)],
            [(0, 7), (1, 1)],
            [(0, 3), (3, 1)],
            [(0, 5), (2, 1)],
            [(1, 3), (2, 7)],
            [(2, 3), (3, 7)],
            [(3, 3), (4, 7)],
            [(4, 3), (1, 7)],
            [(5, 1), (2, 5)],
            [(5, 7), (1, 5)],
            [(5, 3), (3, 5)],
            [(5, 5), (4, 5)],
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

        return movesEdges

    def getMovesEdgesInv(self, objective: "EstadoRubik") -> int:
        """
        Lo que hacemos es crear un diccionario que traduce
        los colores de las caras a los que deberían ser

        Entonces decimos que la arista formada por los colores de las
        caras de self tiene que moverse a la arista formada por
        los colores de las caras del objetivo.

        La T es de temporal.

        El cubo dentro del estado no puede cambiar porque
        si no el traductor sería incorrecto.
        """
        oppositeColors = {0: 5, 1: 3, 2: 4, 3: 1, 4: 2, 5: 0}
        movesEdges = 0

        edgesPositions = [
            [(0, 1), (4, 1)],
            [(0, 7), (1, 1)],
            [(0, 3), (3, 1)],
            [(0, 5), (2, 1)],
            [(1, 3), (2, 7)],
            [(2, 3), (3, 7)],
            [(3, 3), (4, 7)],
            [(4, 3), (1, 7)],
            [(5, 1), (2, 5)],
            [(5, 7), (1, 5)],
            [(5, 3), (3, 5)],
            [(5, 5), (4, 5)],
        ]

        if not hasattr(objective, "edgeTranslator"):
            translator = {}
            for edge in edgesPositions:
                a = objective.cubo.caras[edge[0][0]].casillas[edge[0][1]].color
                b = objective.cubo.caras[edge[1][0]].casillas[edge[1][1]].color
                A = objective.cubo.caras[edge[0][0]].color
                B = objective.cubo.caras[edge[1][0]].color
                colors = sorted(zip([a, b], [A, B]))
                lower, capi = zip(*colors)
                translator["".join(map(str, lower))] = capi
            objective.edgeTranslator = translator

        for edge in edgesPositions:

            aT = self.cubo.caras[edge[0][0]].casillas[edge[0][1]].color
            bT = self.cubo.caras[edge[1][0]].casillas[edge[1][1]].color
            AT = self.cubo.caras[edge[0][0]].color
            BT = self.cubo.caras[edge[1][0]].color
            lowerT, capiT = zip(*sorted(zip([aT, bT], [AT, BT])))
            A, B = objective.edgeTranslator["".join(map(str, lowerT))]
            a, b = capiT

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

        return movesEdges

    def getMovesCorners(self) -> int:
        """
        I am going to explain how to calculate the minimum number of movements
        to place a corner in its correct position. Then we add up all the
        movements of all the corners.

        Any corner can be in 8 positions and 3 orientations giving
        a total of 24 different positions+orientations. The 3 colors
        of the corner are a, b and c. Their correspondant faces are A, B and C.
        And the opposite faces are A', B' and C'. Here we have
        the 24 different positions+orientations:

        a∈A     b∈B     c∈C         0 movements
        a∈A     b∈C     c∈B'        1 movement
        a∈A     b∈B'    c∈C'        2 movements
        a∈A     b∈C'    c∈B         1 movement

        a∈A'    b∈B     c∈C'        2 movements
        a∈A'    b∈C     c∈B         3 movements
        a∈A'    b∈B'    c∈C         2 movements
        a∈A'    b∈C'    c∈B'        3 movements

        a∈B     b∈C'    c∈A'        2 movements
        a∈B     b∈A     c∈C'        3 movements
        a∈B     b∈C     c∈A         2 movements
        a∈B     b∈A'    c∈C         1 movement

        a∈B'    b∈A     c∈C         1 movement
        a∈B'    b∈C'    c∈A         2 movements
        a∈B'    b∈A'    c∈C'        3 movements
        a∈B'    b∈C     c∈A'        2 movements

        a∈C     b∈B     c∈A'        1 movement
        a∈C     b∈A     c∈B         2 movements
        a∈C     b∈B'    c∈A         3 movements
        a∈C     b∈A'    c∈B'        2 movements

        a∈C'    b∈B     c∈A         1 movement
        a∈C'    b∈A     c∈B'        2 movements
        a∈C'    b∈B'    c∈A'        3 movements
        a∈C'    b∈A'    c∈B         2 movements


        So we can combine this into 3 groups
        if we eliminate the possibility of entering
        the next group. The groups are the following:

        The first one has 10 positions+orientations
        and at least one is in its face color.

        When a∈A:
            -If b∈B:        0 movements
            -If b∈B':       2 movements
            -Else:          1 movement


        The second one has 6 positions+orientations
        and at least one is in its opposite color.

        When a∈A':      3 movements


        The last one has 8 positions+orientations
        and is the rest. All have 2 movements.
        """

        oppositeColors = {0: 5, 1: 3, 2: 4, 3: 1, 4: 2, 5: 0}

        movesCorners = 0

        # Each corner has the face and then the number on the face
        corners = [
            [(0, 0), (1, 0), (4, 2)],
            [(0, 2), (3, 2), (4, 0)],
            [(0, 6), (1, 2), (2, 0)],
            [(0, 4), (2, 2), (3, 0)],
            [(5, 0), (1, 4), (2, 6)],
            [(5, 2), (2, 4), (3, 6)],
            [(5, 6), (1, 6), (4, 4)],
            [(5, 4), (3, 4), (4, 6)],
        ]

        for corner in corners:
            a = self.cubo.caras[corner[0][0]].casillas[corner[0][1]].color
            b = self.cubo.caras[corner[1][0]].casillas[corner[1][1]].color
            c = self.cubo.caras[corner[2][0]].casillas[corner[2][1]].color
            A = self.cubo.caras[corner[0][0]].color
            B = self.cubo.caras[corner[1][0]].color
            C = self.cubo.caras[corner[2][0]].color

            if a == A or b == B or c == C:
                if a == A and b == B and c == C:
                    movesCorners += 0
                elif (
                    a == oppositeColors[A]
                    or b == oppositeColors[B]
                    or c == oppositeColors[C]
                ):
                    movesCorners += 2
                else:
                    movesCorners += 1
            elif (
                a == oppositeColors[A]
                or b == oppositeColors[B]
                or c == oppositeColors[C]
            ):
                movesCorners += 3
            else:
                movesCorners += 2

        return movesCorners

    def getMovesCornersInv(self, objective: "EstadoRubik") -> int:
        """
        Traducimos la cara de cada esquina a la cara que debería ser
        para ser igual al objetivo.

        Entonces decimos que la esquina formada por los colores de las
        caras de self tiene que moverse a la esquina formada por
        los colores de las caras del objetivo.

        La T es de temporal.

        El cubo dentro del estado no puede cambiar porque
        si no el traductor sería incorrecto.
        """
        oppositeColors = {0: 5, 1: 3, 2: 4, 3: 1, 4: 2, 5: 0}

        movesCorners = 0

        # Each corner has the face and then the number on the face
        corners = [
            [(0, 0), (1, 0), (4, 2)],
            [(0, 2), (3, 2), (4, 0)],
            [(0, 6), (1, 2), (2, 0)],
            [(0, 4), (2, 2), (3, 0)],
            [(5, 0), (1, 4), (2, 6)],
            [(5, 2), (2, 4), (3, 6)],
            [(5, 6), (1, 6), (4, 4)],
            [(5, 4), (3, 4), (4, 6)],
        ]

        if not hasattr(objective, "cornerTranslator"):
            translator = {}
            for corner in corners:
                a = objective.cubo.caras[corner[0][0]].casillas[corner[0][1]].color
                b = objective.cubo.caras[corner[1][0]].casillas[corner[1][1]].color
                c = objective.cubo.caras[corner[2][0]].casillas[corner[2][1]].color
                A = objective.cubo.caras[corner[0][0]].color
                B = objective.cubo.caras[corner[1][0]].color
                C = objective.cubo.caras[corner[2][0]].color
                colors = sorted(zip([a, b, c], [A, B, C]))
                lower, capi = zip(*colors)
                translator["".join(map(str, lower))] = capi
            objective.cornerTranslator = translator

        for corner in corners:
            aT = self.cubo.caras[corner[0][0]].casillas[corner[0][1]].color
            bT = self.cubo.caras[corner[1][0]].casillas[corner[1][1]].color
            cT = self.cubo.caras[corner[2][0]].casillas[corner[2][1]].color
            AT = self.cubo.caras[corner[0][0]].color
            BT = self.cubo.caras[corner[1][0]].color
            CT = self.cubo.caras[corner[2][0]].color
            lowerT, capiT = zip(*sorted(zip([aT, bT, cT], [AT, BT, CT])))
            A, B, C = objective.cornerTranslator["".join(map(str, lowerT))]
            a, b, c = capiT

            if a == A or b == B or c == C:
                if a == A and b == B and c == C:
                    movesCorners += 0
                elif (
                    a == oppositeColors[A]
                    or b == oppositeColors[B]
                    or c == oppositeColors[C]
                ):
                    movesCorners += 2
                else:
                    movesCorners += 1
            elif (
                a == oppositeColors[A]
                or b == oppositeColors[B]
                or c == oppositeColors[C]
            ):
                movesCorners += 3
            else:
                movesCorners += 2

        return movesCorners

    def manhattanDistance(
        self, inv: bool = False, objective: "EstadoRubik" = None
    ) -> int:
        """
        Función para la heurística
        Calcula la distancia de manhattan de cada casilla a su posición final.

        # https://www.cs.princeton.edu/courses/archive/fall06/cos402/papers/korfrubik.pdf
        En la página 2 abajo a la derecha se explica esta heurística.

        Cogemos el máximo de del numero de movimientos de las aristas/4 y las esquinas/4
        porque es lo que pone en el paper.
        """
        if not inv:
            return max(self.getMovesCorners() / 4, self.getMovesEdges() / 4)

        else:
            return max(
                self.getMovesCornersInv(objective) / 4,
                self.getMovesEdgesInv(objective) / 4,
            )


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
    import random

    # Comprobamos que Manhattan sea bidireccional

    c1 = Cubo()
    c2 = Cubo()

    while True:

        c1.mezclar(random.randint(0, 11))
        c2.mezclar(random.randint(0, 11))

        n1 = EstadoRubik(c1).manhattanDistance(True, EstadoRubik(c2))
        n2 = EstadoRubik(c2).manhattanDistance(True, EstadoRubik(c1))

        if n1 != n2:
            print(
                "ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR"
            )
            print(c1.visualizar())
            print(c2.visualizar())
