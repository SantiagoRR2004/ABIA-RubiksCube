import csv
import ast
import matplotlib.pyplot as plt
import numpy as np
from busquedas import allSearchTypes


def createGraph(data, fieldnames, keyword: str, title: str = None, ylabel: str = None):
    if ylabel is None:
        ylabel = keyword

    if title is None:
        title = ylabel + " vs Number of moves"

    lenKey = len(keyword)

    plt.figure(title)
    for key in fieldnames:
        if key[-lenKey:].lower() == keyword.lower():
            plt.plot(
                list(data.keys()),
                [x[key] for x in data.values()],
                label=key[:-lenKey],
            )

    plt.legend()
    plt.xlabel("Number of moves")
    plt.xticks(list(data.keys()))
    plt.ylabel(ylabel)
    plt.title(title)


if __name__ == "__main__":
    nameFile = "data.csv"

    data = []

    with open(nameFile, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        fieldnames = csv_reader.fieldnames

        for row in csv_reader:
            data.append(row)

    fieldnames.remove("moves")
    nMovs = set([len(ast.literal_eval(row["moves"])) for row in data])

    avgData = {x: {} for x in nMovs}
    for num in avgData.keys():
        for key in fieldnames:
            number = np.mean(
                [
                    float(x[key])
                    for x in data
                    if len(ast.literal_eval(x["moves"])) == num
                ]
            )
            avgData[num][key] = number

    avgDataFinish = {x: {} for x in nMovs}
    for num in avgDataFinish.keys():
        for algo in allSearchTypes().keys():
            for key in fieldnames:
                if key[: len(algo)] == algo:
                    number = np.mean(
                        [
                            float(x[key])
                            for x in data
                            if len(ast.literal_eval(x["moves"])) == num
                            and x[algo + "lenSolution"] != "inf"
                        ]
                    )
                    avgDataFinish[num][key] = number

                if key == "maxTime":
                    number = np.mean(
                        [
                            float(x[key])
                            for x in data
                            if len(ast.literal_eval(x["moves"])) == num
                        ]
                    )
                    avgDataFinish[num][key] = number

    typesOfGraphs = {"": avgData, " (Solved)": avgDataFinish}

    variables = [
        {"name": "time", "title": "Time vs Number of moves", "ylabel": "Time (s)"},
        {
            "name": "lenClosed",
            "title": "Closed vs Number of moves",
            "ylabel": "Number closed",
        },
        {
            "name": "lenOpened",
            "title": "Opened vs Number of moves",
            "ylabel": "Number opened",
        },
        {
            "name": "lenSolution",
            "title": "Solution length vs Number of moves",
            "ylabel": "Number of moves",
        },
    ]

    for key, graph in typesOfGraphs.items():
        for variable in variables:
            createGraph(
                graph,
                fieldnames,
                variable["name"],
                variable["title"] + key,
                variable["ylabel"],
            )

    plt.show()
