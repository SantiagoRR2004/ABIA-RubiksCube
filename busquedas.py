from busquedaAnchura import BusquedaAnchura
from busquedaProfundidad import BusquedaProfundidad
from busquedaProfundidadIterativa import BusquedaProfundidadIterativa
from busquedaProfundidadLimitada import BusquedaProfundidadLimitada
from busquedaBidireccional import BusquedaBidireccional
from busquedaSimpleHillClimbing import BusquedaSimpleHillClimbing
from busquedaSteepestHillClimbing import BusquedaSteepestHillClimbing
from busquedaVoraz import BusquedaVoraz
from busquedaVorazBidireccional import BusquedaVorazBidireccional
from busquedaAStar import BusquedaAStar
from busquedaIDAStar import BusquedaIDAStar
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
        "AscensoColinaSimple2": BusquedaSimpleHillClimbing(
            EstadoRubik.manhattanDistance
        ),
        "AscensoColinaSimple3": BusquedaSimpleHillClimbing(
            EstadoRubik.matchingCorrectPosition
        ),
        "AscensoColinaMaximaPendiente1": BusquedaSteepestHillClimbing(
            EstadoRubik.matchingFaceColor
        ),
        "AscensoColinaMaximaPendiente2": BusquedaSteepestHillClimbing(
            EstadoRubik.manhattanDistance
        ),
        "AscensoColinaMaximaPendiente3": BusquedaSteepestHillClimbing(
            EstadoRubik.matchingCorrectPosition
        ),
        "Voraz1": BusquedaVoraz(EstadoRubik.matchingFaceColor),
        "Voraz2": BusquedaVoraz(EstadoRubik.manhattanDistance),
        "Voraz3": BusquedaVoraz(EstadoRubik.matchingCorrectPosition),
        "VorazBidireccional1": BusquedaVorazBidireccional(
            EstadoRubik.manhattanDistance
        ),
        "VorazBidireccional2": BusquedaVorazBidireccional(
            EstadoRubik.manhattanDistance
        ),
        "VorazBidireccional3": BusquedaVorazBidireccional(
            EstadoRubik.manhattanDistance
        ),
        "AStar1": BusquedaAStar(EstadoRubik.matchingFaceColor),
        "AStar2": BusquedaAStar(EstadoRubik.manhattanDistance),
        "AStar3": BusquedaAStar(EstadoRubik.matchingCorrectPosition),
        "IDAStar1": BusquedaIDAStar(EstadoRubik.matchingFaceColor),
        "IDAStar2": BusquedaIDAStar(EstadoRubik.manhattanDistance),
        "IDAStar3": BusquedaIDAStar(EstadoRubik.matchingCorrectPosition),
    }
    return toret
