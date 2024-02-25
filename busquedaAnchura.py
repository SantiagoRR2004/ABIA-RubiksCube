from nodos import NodoAnchura
from busqueda import Busqueda
import time


# Implementa una búsqueda en Anchura genérica (independiente de Estados y Operadores) controlando repetición de estados.
# Usa lista ABIERTOS (lista) y lista CERRADOS (diccionario usando Estado como clave)
class BusquedaAnchura(Busqueda):
    # https://en.wikipedia.org/wiki/Breadth-first_search

    # Implementa la búsqueda en anchura.
    # Si encuentra solución recupera la lista de Operadores
    # empleados almacenada en los atributos de los objetos NodoAnchura
    def solveProblem(self):
        solutionFlag = False
        abiertos = []
        cerrados = set()  # We change it to a set of representations of the states,
        # this way we don't store the whole state
        abiertos.append(NodoAnchura(self.inicial, None, None))
        nodoActual = abiertos[0]
        if nodoActual.estado.esFinal():
            solutionFlag = True

        while (
            not solutionFlag
            and len(abiertos) > 0
            and time.time() - self.tiempoInicio < self.timeAmount
        ):
            nodoActual = abiertos.pop(0)
            for operador in nodoActual.estado.operadoresAplicables():
                hijo = nodoActual.estado.aplicarOperador(operador)

                if hijo.cubo.visualizar() not in cerrados:
                    if hijo.esFinal():
                        nodoActual = NodoAnchura(hijo, nodoActual, operador)
                        solutionFlag = True
                        break  # I don't like this but it is faster

                    else:
                        abiertos.append(NodoAnchura(hijo, nodoActual, operador))
                        cerrados.add(hijo.cubo.visualizar())
                        # utilizamos CERRADOS para mantener también traza de los nodos añadidos a ABIERTOS

        toret = {
            "lenOpened": len(abiertos),
            "lenClosed": max(0, len(cerrados) - len(abiertos)),
        }

        if solutionFlag:
            toret["solution"] = []
            nodo = nodoActual
            while nodo.padre != None:  # Asciende hasta la raíz
                toret["solution"].insert(0, nodo.operador)
                nodo = nodo.padre
            toret["lenSolution"] = len(toret["solution"])
        else:
            toret["solution"] = None
            toret["lenSolution"] = float("inf")

        return toret
