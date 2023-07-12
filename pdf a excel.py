import csv

with open("archivos/capital.csv") as csv_file:
    listFile = csv.reader(csv_file,delimiter=';')
    bigFile = []
    # Itero el objeto reader para añadirlo en una lista
    for row in listFile:
        if row[0] != 'CAPITAL':
            numero=row[0][0:-4].replace('$','').replace(',','.')
            bigFile.append(numero+',00')
    # print(bigFile)

#
with open("archivos/nuevoprueba.csv", "w") as new_csv_file:
    for i in bigFile:
        new_csv_file.write(i +'\n')


#     fieldnames = bigFile[0].keys()
#     writer = csv.DictWriter(new_csv_file, fieldnames=fieldnames, delimiter=';')
#
#     writer.writeheader()  # Escribir la fila de encabezados
#     writer.writerows(bigFile)  # Escribir los datos modificados
#
# print("El archivo CSV ha sido guardado con los cambios.")
