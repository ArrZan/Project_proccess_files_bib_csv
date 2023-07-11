import csv

with open("prueba.csv") as csv_file:
    listFile = csv.DictReader(csv_file, delimiter=';')
    bigFile = []
    # Itero el objeto reader para añadirlo en una lista

    lista = []
    for row in listFile:
        bigFile.append(row)

    for pos, nom in enumerate(bigFile):
        for clave in nom.keys():
            if clave == 'CAPITAL':
                lista.append(nom[clave])


    listanueva=[]
    lista2 = []
    for x in lista:
        numero_sin_ceros = str(x).rstrip('0')
        lista2.append(numero_sin_ceros)
        for i in bigFile:
            i['CAPITAL']=numero_sin_ceros
            listanueva.append(i)
    print(listanueva)



