import csv

with open("Acccervecerianac.csv") as csv_file:
    listFile = csv.DictReader(csv_file, delimiter=';')
    bigFile = []
    # Itero el objeto reader para añadirlo en una lista
    lista2 = []
    lista = []
    for row in listFile:
        bigFile.append(row)
    for pos, nom in enumerate(bigFile):
        for clave in nom.keys():
            if clave == 'CAPITAL':
                lista.append(nom[clave])
    for x in lista:
        numero_sin_ceros = x[:-2]
        lista2.append(numero_sin_ceros)
    CONT = 0
    listanueva = []
    for cap in bigFile:
        for x in cap:
            if x == 'CAPITAL':
                dicc = {x: lista2[CONT]}
                cap.update(dicc)
                CONT += 1
    print(bigFile)

with open("nuevoprueba.csv", "w", newline='') as new_csv_file:
    fieldnames = bigFile[0].keys()
    writer = csv.DictWriter(new_csv_file, fieldnames=fieldnames, delimiter=';')

    writer.writeheader()  # Escribir la fila de encabezados
    writer.writerows(bigFile)  # Escribir los datos modificados

print("El archivo CSV ha sido guardado con los cambios.")
