from cubo import Cubo
from problemaRubik import EstadoRubik
from problema import Problema
import csv, os
from busquedas import allSearchTypes
from typing import List, Tuple
import ast
from concurrent.futures import ProcessPoolExecutor


def run_algorithm(name, algorithm, movsMezcla, maxTime):
    """This function runs a single algorithm"""
    newCube = Cubo()
    for movement in movsMezcla:
        newCube.mover(movement)
    problem = Problema(EstadoRubik(newCube), algorithm)
    return problem.obtenerSolucion(maxTime)


def multipleSearches(
    algorithms: dict, numMovs: int = 1, maxTime: int = 60, fileToCheck: str = None
) -> Tuple[dict, List[int]]:
    """
    Args:
        -algorithms: dict. A dictionary with the algorithms to use
        -numMovs: int. The number of movements to shuffle the cube
        -maxTime: int. The maximum amount of time to solve the problem
        -fileToCheck: str. The name of the file to check if the movements have been made before

    Returns:
        -dict. A dictionary with the results of the searches
        as the keys the names of the algorithms and as the values
        the results of the searches
        -List[int]. A list with the movements that were made to shuffle the cube
    """
    cubo = Cubo()
    movsMezcla = cubo.mezclar(numMovs)
    if fileToCheck:
        with open(fileToCheck, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            olderMoves = [
                ast.literal_eval(x["moves"]) for x in reader if x["moves"] != ""
            ]
        if movsMezcla in olderMoves:
            return {}, movsMezcla

    toret = {}

    with ProcessPoolExecutor() as executor:
        # Submit each algorithm to the executor
        futures = {
            executor.submit(run_algorithm, name, algorithm, movsMezcla, maxTime): name
            for name, algorithm in algorithms.items()
        }

        # Collect results as they become available
        for future in futures:
            name = futures[future]
            toret[name] = future.result()

    return toret, movsMezcla


def calculateTime(nMovs) -> int:
    """
    Args:
        -nMovs: int. The number of movements to shuffle the cube

    Returns:
        -int. The maximum amount of time to solve the problem
    """
    return 10 * nMovs


def createRow(nMovs) -> dict:
    """
    Args:
        -nMovs: int. The number of movements to shuffle the cube
        -time: int. The maximum amount of time to solve the problem
    Returns:
        -dict. A dictionary with the results of the searches
        as the keys the names of the algorithms and as the values
        the results of the searches
    """
    toret, moves = multipleSearches(
        allSearchTypes(), nMovs, calculateTime(nMovs), "data.csv"
    )
    if toret:  # If the movements have been made before
        newtoret = {"moves": moves, "maxTime": calculateTime(nMovs)}
        for name, value in toret.items():
            for name2, value2 in value.items():
                if name2 != "solution":
                    newtoret[name + name2] = value2
    else:
        newtoret = {}

    return newtoret


def getHeaders(filename) -> list:
    """
    It creates the file if it doesn't exist
    Args:
        -filename: str. The name of the file to get the headers from

    Returns:
        -list. A list with the headers of the CSV file
    """
    if not os.path.exists(filename):
        with open(filename, "w"):
            pass
        return []

    else:
        with open(filename, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames
        if fieldnames is None:
            return []
        return fieldnames
