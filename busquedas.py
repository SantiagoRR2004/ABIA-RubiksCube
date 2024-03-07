from busquedaAnchura import BusquedaAnchura
from busquedaProfundidad import BusquedaProfundidad
from busquedaProfundidadIterativa import BusquedaProfundidadIterativa
from busquedaProfundidadLimitada import BusquedaProfundidadLimitada
from busquedaBidireccional import BusquedaBidireccional
from busquedaSimpleHillClimbing import BusquedaSimpleHillClimbing
from busquedaSteepestHillClimbing import BusquedaSteepestHillClimbing
from busquedaVoraz import BusquedaVoraz
from busquedaAStar import BusquedaAStar
from problemaRubik import EstadoRubik


def allSearchTypes() -> dict:
    """
    Returns:
        -dict. A dictionary with the algorithms to use
        as the keys the names of the algorithms and as the values
        the algorithms
    """

    toret = {
        "Anchura": BusquedaAnchura(),
        "Profundidad": BusquedaProfundidad(),
        "ProfundidadIterativa": BusquedaProfundidadIterativa(),
        "ProfundidadIterativa2": BusquedaProfundidadIterativa(2),
        "ProfundidadLimitada": BusquedaProfundidadLimitada(),
        "Bidireccional": BusquedaBidireccional(),
        "AscensoColinaSimple1": BusquedaSimpleHillClimbing(
            EstadoRubik.matchingCorrectPosition
        ),
        "AscensoColinaAscensoPronunciado1": BusquedaSteepestHillClimbing(
            EstadoRubik.matchingCorrectPosition
        ),
        "Voraz1": BusquedaVoraz(EstadoRubik.matchingCorrectPosition),
        "AStar1": BusquedaAStar(EstadoRubik.matchingCorrectPosition),
    }
    return toret
