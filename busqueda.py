from abc import abstractmethod
from abc import ABCMeta
from typing import TYPE_CHECKING, Dict
import time
import tracemalloc

if TYPE_CHECKING:
    from problema import Estado


# Interfaz genérico para algoritmos de búsqueda
class Busqueda(metaclass=ABCMeta):

    def buscarSolucion(self, inicial: "Estado", timeAmount: int = 60) -> Dict:
        """
        Args:
            -inicial: Estado. The initial state of the problem
            -timeAmount: int. (In seconds) The amount of time in seconds that the algorithm has to solve the problem
                This needs to be implemented in the concrete classes

        Returns:
            -Dict. The dictionary that returns solveProblem(),
                the time it took to solve the problem
                and the maximum amount of memory used
        """
        self.inicial = inicial
        self.timeAmount = timeAmount
        self.tiempoInicio = time.time()

        tracemalloc.reset_peak()

        tracemalloc.start()  # Start tracing memory allocations

        toret = self.solveProblem()

        toret["time"] = time.time() - self.tiempoInicio

        # Get the peak memory usage
        toret["maxMemory"] = tracemalloc.get_traced_memory()[1]

        tracemalloc.reset_peak()

        return toret

    @abstractmethod
    def solveProblem(self) -> Dict:
        """
        This function should be implemented in the concrete classes
        it also needs to make sure that the timeAmount is respected

        returns:
            -Dict. A dictionary with the following keys:

                -'solution': A list with the solution to the problem
                -'lenOpened': An integer with the length of the open list
                -'lenClosed': An integer with the length of the closed list
                -'lenSolution': An integer with the length of the solution

        """
        pass
