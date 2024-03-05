from nodos import NodoNoInformado
from busqueda import Busqueda
from cubo import Cubo
from problemaRubik import EstadoRubik
import time


class BusquedaBidireccional(Busqueda):
    # https://en.wikipedia.org/wiki/Bidirectional_search

    def solveProblem(self):
        solutionFlag = False

        fowardOpened = []
        fowardOpened.append(NodoNoInformado(self.inicial, None, None))

        backwardOpened = []
        backwardOpened.append(NodoNoInformado(EstadoRubik(Cubo()), None, None))

        closed = set()
        closed.add(self.inicial.cubo.visualizar())
        closed.add(Cubo().visualizar())

        fowardNode = fowardOpened[0]
        if fowardNode.estado.esFinal():
            solutionFlag = True
            solutionNodes = {"front": fowardNode, "back": backwardOpened[0]}

        while (
            not solutionFlag
            and len(backwardOpened) > 0
            and len(backwardOpened) > 0
            and time.time() - self.tiempoInicio < self.timeAmount
        ):
            fowardNode = fowardOpened.pop(0)
            for operador in fowardNode.estado.operadoresAplicables():
                descendant = fowardNode.estado.aplicarOperador(operador)

                if descendant in [x.estado for x in backwardOpened]:
                    solutionNodes = {
                        "front": NodoNoInformado(descendant, fowardNode, operador),
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
                        NodoNoInformado(descendant, fowardNode, operador)
                    )
                    closed.add(descendant.cubo.visualizar())

            if not solutionFlag:
                backwardNode = backwardOpened.pop(0)
                for operador in backwardNode.estado.operadoresAplicables():
                    descendant = backwardNode.estado.aplicarOperador(operador)

                    if descendant in [x.estado for x in fowardOpened]:
                        solutionNodes = {
                            "front": [
                                x for x in fowardOpened if x.estado == descendant
                            ][0],
                            "back": NodoNoInformado(descendant, backwardNode, operador),
                        }
                        solutionFlag = True
                        break

                    elif descendant.cubo.visualizar() not in closed:
                        backwardOpened.append(
                            NodoNoInformado(descendant, backwardNode, operador)
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
