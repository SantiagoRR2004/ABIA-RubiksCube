import sys
from cubo import Cubo
from problemaRubik import EstadoRubik
from busquedaAnchura import BusquedaAnchura
from busquedaProfundidad import BusquedaProfundidad
from busquedaProfundidadIterativa import BusquedaProfundidadIterativa
from problema import Problema


cubo = Cubo()

# print("CUBO SIN MEZCLAR:\n" + cubo.visualizar())

# Mover frontal face
# cubo.mover(cubo.F)

# print("CUBO resultado del movimiento F:\n" + cubo.visualizar())

movs = 3
if len(sys.argv) > 1:
    movs = int(sys.argv[1])

movsMezcla = cubo.mezclar(movs)

print("MOVIMIENTOS ALEATORIOS:", movs)
for m in movsMezcla:
    print(cubo.visualizarMovimiento(m) + " ")
print()

# print("CUBO INICIAL (MEZCLADO):\n" + cubo.visualizar())

# Creación de un problema
problema = Problema(EstadoRubik(cubo), BusquedaProfundidadIterativa())

print("SOLUCION:")
opsSolucion = problema.obtenerSolucion()

if opsSolucion["solution"] != None:
    for o in opsSolucion["solution"]:
        print(cubo.visualizarMovimiento(o.getEtiqueta()) + " ")
        cubo.mover(o.movimiento)
    print()
    print("CUBO FINAL:\n" + cubo.visualizar())
else:
    print("no se ha encontrado solución")


print(f"Time taken: {opsSolucion['time']:.2f} seconds")
print(opsSolucion)
