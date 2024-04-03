import csv, ast
from utils import createRow, getHeaders


if __name__ == "__main__":
    nameFile = "data.csv"
    numberOfRows = 1
    timeToAdd = 10

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
            # If the list is empty it means at least one
            # of the algorithms has solved the problem
            if not [
                key
                for key, value in row.items()
                if key[-11:].lower() == "lensolution" and value != "inf" and value != ""
            ]:
                maxTime = int(row["maxTime"])
                moves = ast.literal_eval(row["moves"])
                print(f"Adding {timeToAdd}s to {moves}")
                oldData[index] = createRow(0, maxTime + timeToAdd, moves)
                break

        with open(nameFile, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(oldData)

        print(f"Added {timeToAdd}s to {moves}")
