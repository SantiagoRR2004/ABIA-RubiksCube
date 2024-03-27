from nodos import NodoInformado
from busqueda import Busqueda
import time
from cubo import Cubo
from problemaRubik import EstadoRubik


class BusquedaAStarBidireccional(Busqueda):

    def __init__(self, heuristic) -> None:
        self.heuristic = heuristic

    @staticmethod
    def addNode(node: NodoInformado, opened: list, closed: list) -> None:
        """
        This function adds a node to the opened and closed list if it is not in the closed list
        If it is in the closed list, it checks if the new node has a better cost and changes the father if it is the case

        Args:
            node (NodoInformado): The node to be added
            opened (list): The list of opened nodes
            closed (list): The list of closed nodes
        """
        if node not in [x.estado for x in closed]:
            opened.append(node)
            closed.append(node)
        else:
            previous = [x for x in closed if x.estado == node.estado][0]
            if previous.getCoste() > node.getCoste():
                previous.changeFather(node.padre, node.operador)

    def solveProblem(self):
        solutionFlag = False

        bestValue = self.heuristic(EstadoRubik(Cubo()))
        bestValueBack = self.heuristic(self.inicial, inv=True, objective=self.inicial)

        initial = NodoInformado(
            self.inicial,
            None,
            None,
            1,
            abs(self.heuristic(self.inicial) - bestValue),
        )

        end = NodoInformado(
            EstadoRubik(Cubo()),
            None,
            None,
            1,
            abs(
                self.heuristic(EstadoRubik(Cubo()), inv=True, objective=self.inicial)
                - bestValueBack
            ),
        )

        fowardOpened = []
        fowardOpened.append(initial)

        backwardOpened = []
        backwardOpened.append(end)

        fowardClosed = []
        fowardClosed.append(initial)

        backwardClosed = []
        backwardClosed.append(end)

        fowardNode = fowardOpened[0]
        if fowardNode.estado.esFinal():
            solutionFlag = True

        ####################################################################

        while (
            not solutionFlag
            and len(fowardOpened) > 0
            and time.time() - self.tiempoInicio < self.timeAmount
        ):
            fowardNode = min(fowardOpened, key=lambda x: x.getTotal())
            fowardOpened.remove(fowardNode)

            if fowardNode.estado.esFinal():
                solutionFlag = True

            # First we do the foward search
            else:
                for operador in fowardNode.estado.operadoresAplicables():
                    descendant = fowardNode.estado.aplicarOperador(operador)
                    """
                    We have 3 things to check now:
                    - If the descendant needs to be added to the fowardOpened list
                    - If the descendant changes a node in the closedOpened list
                    - If the descendant makes a path with backwardOpened list
                    """

                    # We add the node as normal
                    if descendant not in [x.estado for x in fowardClosed]:
                        if descendant in [x.estado for x in backwardOpened]:
                            # If we find a path to the solution we add all those nodes to fowardOpened
                            otherNode = [
                                x
                                for x in backwardOpened
                                if x.estado.cubo.visualizar()
                                == descendant.cubo.visualizar()
                            ][0]

                            newNode = NodoInformado(
                                descendant,
                                fowardNode,
                                operador,
                                1,
                                abs(self.heuristic(descendant) - bestValue),
                            )

                            self.addNode(newNode, fowardOpened, fowardClosed)

                            nextNode = otherNode.padre

                            while nextNode != None:

                                newNode = NodoInformado(
                                    estado=nextNode.estado,
                                    padre=newNode,
                                    operador=otherNode.operador.opposite(),
                                    coste=1,
                                    heuristica=abs(
                                        self.heuristic(nextNode.estado) - bestValue
                                    ),
                                )

                                self.addNode(newNode, fowardOpened, fowardClosed)

                                otherNode = nextNode
                                nextNode = nextNode.padre

                        else:
                            newNode = NodoInformado(
                                descendant,
                                fowardNode,
                                operador,
                                1,
                                abs(self.heuristic(descendant) - bestValue),
                            )
                            fowardOpened.append(newNode)
                            fowardClosed.append(newNode)

                    else:
                        previous = [x for x in fowardClosed if x.estado == descendant][
                            0
                        ]
                        if previous.getCoste() > fowardNode.getCoste() + 1:
                            # We change the the older father for one with less cost
                            previous.changeFather(fowardNode, operador)

                # Then we do the backwards search
                backwardNode = min(backwardOpened, key=lambda x: x.getTotal())
                backwardOpened.remove(backwardNode)

                for operador in backwardNode.estado.operadoresAplicables():
                    descendant = backwardNode.estado.aplicarOperador(operador)

                    # We still add the node as normal
                    if descendant not in [x.estado for x in backwardClosed]:
                        newNode = NodoInformado(
                            descendant,
                            backwardNode,
                            operador,
                            1,
                            abs(
                                self.heuristic(
                                    descendant,
                                    inv=True,
                                    objective=self.inicial,
                                )
                                - bestValueBack
                            ),
                        )
                        backwardOpened.append(newNode)
                        backwardClosed.append(newNode)

                    """
                    This time if it makes a conecting path
                    we still add the nodes to the fowardOpened list
                    So we go backwards on the backwardNode
                    """
                    if descendant in [x.estado for x in fowardOpened]:
                        otherNode = [
                            x
                            for x in fowardOpened
                            if x.estado.cubo.visualizar()
                            == descendant.cubo.visualizar()
                        ][0]

                        copy = backwardNode

                        newNode = NodoInformado(
                            estado=copy.estado,
                            padre=otherNode,
                            operador=operador.opposite(),
                            coste=1,
                            heuristica=abs(self.heuristic(copy.estado) - bestValue),
                        )

                        self.addNode(newNode, fowardOpened, fowardClosed)

                        nextNode = copy.padre

                        while nextNode != None:

                            newNode = NodoInformado(
                                estado=nextNode.estado,
                                padre=newNode,
                                operador=copy.operador.opposite(),
                                coste=1,
                                heuristica=abs(
                                    self.heuristic(nextNode.estado) - bestValue
                                ),
                            )

                            self.addNode(newNode, fowardOpened, fowardClosed)

                            copy = nextNode
                            nextNode = nextNode.padre

                    else:
                        previous = [
                            x for x in backwardClosed if x.estado == descendant
                        ][0]
                        if previous.getCoste() > backwardNode.getCoste() + 1:
                            # We change the the older father for one with less cost
                            previous.changeFather(backwardNode, operador)

        toret = {
            "lenOpened": len(fowardOpened) + len(backwardOpened),
            "lenClosed": max(
                0,
                len(fowardClosed)
                + len(backwardClosed)
                - len(fowardOpened)
                - len(backwardOpened),
            ),
        }

        if solutionFlag:
            toret["solution"] = []
            nodo = fowardNode
            while nodo.padre != None:  # Asciende hasta la raíz
                toret["solution"].insert(0, nodo.operador)
                nodo = nodo.padre
            toret["lenSolution"] = len(toret["solution"])
        else:
            toret["solution"] = None
            toret["lenSolution"] = float("inf")

        return toret
