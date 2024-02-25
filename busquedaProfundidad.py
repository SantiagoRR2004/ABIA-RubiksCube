from nodos import NodoAnchura
from busqueda import Busqueda
import time


class BusquedaProfundidad(Busqueda):

    # Implementa la búsqueda en profundidad. Si encuentra solución recupera la lista de Operadores empleados almacenada en los atributos de los objetos NodoProfundidad
    def solveProblem(self):
        solucion = False
        nodoActual = None
        actual, hijo = None, None
        solutionFlag = False
        abiertos = []
        cerrados = dict()
        abiertos.append(NodoAnchura(self.inicial, None, None))

        while (
            not solucion
            and len(abiertos) > 0
            and time.time() - self.tiempoInicio < self.timeAmount
        ):
            if len(set(abiertos)) != len(abiertos):
                print("Es necesario")
            nodoActual = abiertos.pop(-1)
            actual = nodoActual.estado
            if actual.esFinal():
                solucion = True
            else:
                # cerrados[actual.cubo.visualizar()] = nodoActual
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    if hijo.cubo.visualizar() not in cerrados.keys():
                        abiertos.append(NodoAnchura(hijo, nodoActual, operador))
                        cerrados[hijo.cubo.visualizar()] = (
                            hijo  # utilizamos CERRADOS para mantener también traza de los nodos añadidos a ABIERTOS
                        )

        toret = {
            "lenOpen": len(abiertos),
            "lenClose": len(cerrados),
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
