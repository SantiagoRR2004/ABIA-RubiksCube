import csv, ast
from utils import createRow, getHeaders


if __name__ == "__main__":
    nameFile = "data.csv"
    numberOfRows = 2

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

    # Here is where the code changes
    for i in range(numberOfRows):
        moves = "Not need to refill"
        with open(nameFile, "r", newline="") as file:  # This code is repeated
            reader = csv.DictReader(file)
            oldData = list(reader)

        for index, row in enumerate(oldData):
            if len([x for x in row.values() if x == ""]) > 0:
                maxTime = int(row["maxTime"])
                moves = ast.literal_eval(row["moves"])
                oldData[index] = createRow(0, maxTime, moves)
                break

        with open(nameFile, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(oldData)

        print(f"Refilled the moves {moves}")
