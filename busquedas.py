from busquedaAnchura import BusquedaAnchura
from busquedaProfundidad import BusquedaProfundidad
from busquedaProfundidadIterativa import BusquedaProfundidadIterativa
from busquedaProfundidadLimitada import BusquedaProfundidadLimitada
from busquedaBidireccional import BusquedaBidireccional
from busquedaSimpleHillClimbing import BusquedaSimpleHillClimbing
from busquedaSteepestHillClimbing import BusquedaSteepestHillClimbing
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
            EstadoRubik.matchingFaceColor
        ),
        "AscensoColinaAscensoPronunciado1": BusquedaSteepestHillClimbing(
            EstadoRubik.matchingFaceColor
        ),
    }
    return toret
