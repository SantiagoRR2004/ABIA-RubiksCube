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

    plots = []

    plt.figure(title)
    for key in fieldnames:
        if key[-lenKey:].lower() == keyword.lower():
            plots.append(
                plt.plot(
                    list(data.keys()),
                    [x[key] for x in data.values()],
                    label=key[:-lenKey],
                ),
            )

    # plt.gca().clabel(plots, inline=True, fontsize=10)

    handles, labels = plt.gca().get_legend_handles_labels()

    # Sort the handles and labels alphabetically by labels
    handles_labels_sorted = sorted(zip(handles, labels), key=lambda x: x[1])
    handles_sorted, labels_sorted = zip(*handles_labels_sorted)

    # Create the legend with sorted handles and labels
    plt.legend(handles_sorted, labels_sorted)

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
                    if len(ast.literal_eval(x["moves"])) == num and x[key] != ""
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
                            and x[key] != ""
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

    # Now we add the minimum number of moves to the data
    attribute = "lenSolution"
    for row in data:
        lenSolutions = [
            value
            for key, value in row.items()
            if key[-len(attribute) :] == attribute and value != ""
        ]
        lenSolutions = [float(x) for x in lenSolutions] + [
            len(ast.literal_eval(row["moves"]))
        ]
        row["lenMinSolution"] = int(min(lenSolutions))

    # We create the numbers
    nMinMovs = set([row["lenMinSolution"] for row in data])

    # We create the average by the minimum number of moves to solve
    avgMinData = {x: {} for x in nMinMovs}
    for num in avgMinData.keys():
        for key in fieldnames:
            number = np.mean(
                [
                    float(x[key])
                    for x in data
                    if x["lenMinSolution"] == num and x[key] != ""
                ]
            )
            avgMinData[num][key] = number

    # We create the average by the minimum number of moves to solve with the solved ones
    avgMinDataFinish = {x: {} for x in nMinMovs}
    for num in avgMinDataFinish.keys():
        for algo in allSearchTypes().keys():
            for key in fieldnames:
                if key[: len(algo)] == algo:
                    number = np.mean(
                        [
                            float(x[key])
                            for x in data
                            if x["lenMinSolution"] == num
                            and x[algo + "lenSolution"] != "inf"
                            and x[key] != ""
                        ]
                    )
                    avgMinDataFinish[num][key] = number

                if key == "maxTime":
                    number = np.mean(
                        [
                            float(x[key])
                            for x in data
                            if x["lenMinSolution"] == num and x[key] != ""
                        ]
                    )
                    avgMinDataFinish[num][key] = number

    typesOfGraphs = {
        "": avgData,
        " (Solved)": avgDataFinish,
        " (Real)": avgMinData,
        " (Real and Solved)": avgMinDataFinish,
    }

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
        {
            "name": "maxMemory",
            "title": "Memory vs Number of moves",
            "ylabel": "Memory (bytes)",
        },
        {
            "name": "EBF",
            "title": "Ramification Factor vs Number of moves",
            "ylabel": "EBF",
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
