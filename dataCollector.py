from main import multipleSearches
from busquedas import allSearchTypes
import csv
import os
import random


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


if __name__ == "__main__":
    nameFile = "data.csv"
    minimum = 1
    maximum = 10
    numberOfRows = 10

    oldHeaders = getHeaders(nameFile)

    with open(nameFile, "r", newline="") as file:
        reader = csv.DictReader(file)
        oldData = list(reader)

    data = createRow(0)

    newHeaders = list(data.keys())

    diff = set(newHeaders) - set(oldHeaders)

    oldHeaders.extend(diff)
    fieldnames = oldHeaders

    with open(nameFile, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for row in oldData:
            writer.writerow(row)

    for i in range(numberOfRows):
        nMovs = random.randint(minimum, maximum)
        data = createRow(nMovs)
        with open(nameFile, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if data:
                writer.writerow(data)
