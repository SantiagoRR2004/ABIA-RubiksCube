from nodos import NodoAnchura
from busqueda import Busqueda


# Implementa una búsqueda en Anchura genérica (independiente de Estados y Operadores) controlando repetición de estados.
# Usa lista ABIERTOS (lista) y lista CERRADOS (diccionario usando Estado como clave)
class BusquedaAnchura(Busqueda):

    # Implementa la búsqueda en anchura. Si encuentra solución recupera la lista de Operadores empleados almacenada en los atributos de los objetos NodoAnchura
    def buscarSolucion(self, inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()
        abiertos.append(NodoAnchura(inicial, None, None))
        while not solucion and len(abiertos) > 0:
            nodoActual = abiertos.pop(0)
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
        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre != None:  # Asciende hasta la raíz
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None
