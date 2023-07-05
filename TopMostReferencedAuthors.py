import csv

nomarRef = "archivos\\referenciasContar"  # Dirección y nombre del archivo csv


def countAuthors(listaAutores):
    """
    Recibe una lista, y devuelve un diccionario con todas las repeticiones de
    cada valor
    """
    return {i: listaAutores.count(i) for i in listaAutores}


with open(nomarRef + "1.csv", "r", encoding="utf-8") as csvfile:
    # Crea un objeto reader similar a un diccionario delimitador por la barra |
    listFile = csv.DictReader(csvfile, delimiter=',')
    bigFile = []

    # # Itero el objeto reader para añadirlo en una lista
    # for row in listFile:
    #     bigFile.append(row)

    print(bigFile)

    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        print(row)
