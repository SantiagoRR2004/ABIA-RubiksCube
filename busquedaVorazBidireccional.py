from nodos import NodoInformado
from busqueda import Busqueda
from cubo import Cubo
from problemaRubik import EstadoRubik
import time


class BusquedaVorazBidireccional(Busqueda):

    def __init__(self, heuristic):
        self.heuristic = heuristic

    def solveProblem(self):
        solutionFlag = False

        bestValue = self.heuristic(EstadoRubik(Cubo()))
        bestValueBack = self.heuristic(self.inicial, inv=True, objective=self.inicial)

        fowardOpened = []
        fowardOpened.append(
            NodoInformado(
                self.inicial,
                None,
                None,
                0,
                abs(self.heuristic(self.inicial) - bestValue),
            )
        )

        backwardOpened = []
        backwardOpened.append(
            NodoInformado(
                EstadoRubik(Cubo()),
                None,
                None,
                0,
                abs(
                    self.heuristic(
                        EstadoRubik(Cubo()), inv=True, objective=self.inicial
                    )
                    - bestValueBack
                ),
            )
        )

        closed = set()
        closed.add(self.inicial.cubo.visualizar())
        closed.add(Cubo().visualizar())

        fowardNode = fowardOpened[0]
        if fowardNode.estado.esFinal():
            solutionFlag = True
            solutionNodes = {"front": fowardNode, "back": backwardOpened[0]}

        while (
            not solutionFlag
            and len(fowardOpened) > 0
            and len(backwardOpened) > 0
            and time.time() - self.tiempoInicio < self.timeAmount
        ):
            fowardNode = min(fowardOpened, key=lambda x: x.getHeuristica())
            fowardOpened.remove(fowardNode)

            for operador in fowardNode.estado.operadoresAplicables():
                descendant = fowardNode.estado.aplicarOperador(operador)

                if descendant in [x.estado for x in backwardOpened]:
                    solutionNodes = {
                        "front": NodoInformado(
                            descendant,
                            fowardNode,
                            operador,
                            0,
                            abs(self.heuristic(descendant) - bestValue),
                        ),
                        "back": [
                            x
                            for x in backwardOpened
                            if x.estado.cubo.visualizar()
                            == descendant.cubo.visualizar()
                        ][0],
                    }
                    solutionFlag = True
                    break

                elif descendant.cubo.visualizar() not in closed:
                    fowardOpened.append(
                        NodoInformado(
                            descendant,
                            fowardNode,
                            operador,
                            0,
                            abs(self.heuristic(descendant) - bestValue),
                        )
                    )
                    closed.add(descendant.cubo.visualizar())

            # Now we check the backward nodes
            # We search around the objective node
            if not solutionFlag:
                backwardNode = min(backwardOpened, key=lambda x: x.getHeuristica())
                backwardOpened.remove(backwardNode)

                for operador in backwardNode.estado.operadoresAplicables():
                    descendant = backwardNode.estado.aplicarOperador(operador)

                    if descendant in [x.estado for x in fowardOpened]:
                        solutionNodes = {
                            "front": [
                                x for x in fowardOpened if x.estado == descendant
                            ][0],
                            "back": NodoInformado(
                                descendant,
                                backwardNode,
                                operador,
                                0,
                                abs(
                                    self.heuristic(
                                        descendant,
                                        inv=True,
                                        objective=self.inicial,
                                    )
                                    - bestValueBack
                                ),
                            ),
                        }
                        solutionFlag = True
                        break

                    elif descendant.cubo.visualizar() not in closed:
                        backwardOpened.append(
                            NodoInformado(
                                descendant,
                                backwardNode,
                                operador,
                                0,
                                abs(
                                    self.heuristic(
                                        descendant,
                                        inv=True,
                                        objective=self.inicial,
                                    )
                                    - bestValueBack
                                ),
                            )
                        )
                        closed.add(descendant.cubo.visualizar())

        toret = {
            "lenOpened": len(fowardOpened) + len(backwardOpened),
            "lenClosed": max(0, len(closed) - len(fowardOpened) - len(backwardOpened)),
        }

        if solutionFlag:
            toret["solution"] = []

            nodo = solutionNodes["front"]
            while nodo.padre != None:  # Asciende hasta la raíz
                toret["solution"].insert(0, nodo.operador)
                nodo = nodo.padre

            nodo = solutionNodes["back"]
            while nodo.padre != None:
                toret["solution"].append(nodo.operador.opposite())
                nodo = nodo.padre

            toret["lenSolution"] = len(toret["solution"])

        else:
            toret["solution"] = None
            toret["lenSolution"] = float("inf")

        return toret
