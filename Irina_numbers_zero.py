import csv

with open("archivos/capital.csv") as csv_file, open("archivos/nuevoprueba.csv", "w") as new_csv_file:
    listFile = csv.reader(csv_file, delimiter=' ')

    next(listFile, None)  # quito el header del file csv

    # Itero el objeto reader para añadirlo en una lista
    for row in listFile:
        numero = ''.join(row)
        numero = numero[1:-5]
        new_csv_file.write(f"{numero}.00\n")
