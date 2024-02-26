from nodos import NodoAnchura
from busqueda import Busqueda
import time


class BusquedaProfundidadIterativa(Busqueda):
    def busquedaProfundaRecursiva(self, nodoActual, cota, cerrados):
        actual = nodoActual.estado
        if actual.esFinal():
            return nodoActual
        if cota == 0:
            return None
        cerrados[actual.cubo.visualizar()] = (
            actual  # utilizamos CERRADOS para mantener también traza de los nodos añadidos a ABIERTOS
        )
        for operador in actual.operadoresAplicables():
            hijo = actual.aplicarOperador(operador)
            if hijo.cubo.visualizar() not in cerrados.keys():
                nodoHijo = NodoAnchura(hijo, nodoActual, operador)
                nodoResultado = self.busquedaProfundaRecursiva(
                    nodoHijo, cota - 1, cerrados.copy()
                )

                if nodoResultado:
                    return nodoResultado
        return None

    def profundidad(self, cota=10000):
        cerrados = dict()
        raiz = NodoAnchura(self.inicial, None, None)
        nodoResultado = self.busquedaProfundaRecursiva(raiz, cota, cerrados)

        # esta parte se podría refactorizar a la función solveProblem
        # Para que no cree el toret pese a que no se haya alcanzado ni la solución ni la cota maxima.
        toret = {
            "lenOpened": 0,
            "lenClosed": len(cerrados),
        }

        if nodoResultado:
            toret["solution"] = []
            nodo = nodoResultado
            while nodo.padre != None:  # Asciende hasta la raíz
                toret["solution"].insert(0, nodo.operador)
                nodo = nodo.padre
            toret["lenSolution"] = len(toret["solution"])
        else:
            toret["solution"] = None
            toret["lenSolution"] = float("inf")

        return toret

    def solveProblem(self, cota=2):
        # cota 7 ya se va a un tiempo de: 900 segundos
        if cota is None:
            return self.profundidad()
        for i in range(1, cota + 1):
            print("cota:", i)
            toret = self.profundidad(i)
            if toret["solution"]:
                return toret
        return toret
