import csv
import random
from utils import createRow, getHeaders


if __name__ == "__main__":
    nameFile = "data.csv"
    minimum = 2
    maximum = 3
    numberOfRows = 3

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

        print(f"Added {nMovs} movements")
