import csv

newFile = []  # Aquí se guarda los datos con la nueva estructura (año, author, q, palabras, contador)
filterFile = []  # Archivo con los campos filtrados de las referencias


# Función para extraer Autores, Quartiles y keywords de un archivo con referencias
def Extract_A_Q_K_from_Refr(file):
    # Itero el objeto reader para añadirlo en una lista
    for row in file:
        data = {}  # Aquí se guarda los datos con la nueva estructura

        # Inclusión del autor, si hay más de dos, solo entra el primer y último author
        if len(row["Authors"].split(",")) > 1:
            data["Authors"] = row["Authors"].split(",")[0] + "," + row["Authors"].split(",")[-1]
        else:
            data["Authors"] = row["Authors"].split(",")[0]

        # Solo incluyo a los cuartiles 1,2,3 y 4 si no, será "vacio"
        if row["quartil"] == "Q1" or row["quartil"] == "Q2" or row["quartil"] == "Q3" or row["quartil"] == "Q4":
            data["Quartil"] = row["quartil"]
        else:
            data["Quartil"] = "vacio"

        if row["Keywords"]:
            data["Keywords"] = row["Keywords"].replace(";", ",")
        else:
            data["Keywords"] = "vacio"

        data["Year"] = row["Publication year"]
        data["Count"] = 1

        # Añadimos a la lista el diccionario creado
        filterFile.append(data)

    # Mandamos a guardar el archivo
    SaveFile(filterFile)


def SaveFile(file):
    # Guardamos los datos del filterFile
    listKeyYear = open("keywordForYear.csv", "w")
    # Creamos la cabecera de las columnas del csv
    listKeyYear.write("year;Authors; AuthorOne;AuthorLast;Quartil;Keywords;Keyword;Count;" + chr(13))

    for row in file:
        # Aquí escogemos un valor predeterminado(vacio) cuando solo es un autor para el "AuthorLast"
        aut2 = "vacio"
        if len(row["Authors"].split(",")) > 1:
            aut2 = row["Authors"].split(",")[1]

        # Añadiremos tantas veces se repita los keywords para irlos colocando separados en el campo "Keyword", no en el campo "Keywords"
        if row["Keywords"] != "vacio":
            keywordCatch = row["Keywords"].split(",")
            for posKey in range(len(row["Keywords"].split(","))):
                listKeyYear.write(
                    str(row["Year"]) + ";" + row["Authors"] + ";" + row["Authors"].split(",")[0] + ";" + aut2 + ";" +
                    row[
                        "Quartil"] + ";" + row["Keywords"] + ";" + keywordCatch[posKey] + ";" + str(
                        row["Count"]) + ";" + chr(13))
        else:
            listKeyYear.write(
                str(row["Year"]) + ";" + row["Authors"] + ";" + row["Authors"].split(",")[0] + ";" + aut2 + ";" + row[
                    "Quartil"] + ";" + row["Keywords"] + ";" + row["Keywords"] + ";" + str(
                    row["Count"]) + ";" + chr(13))
        # Intento corregir el encode de ciertos caracteres que salen undefined
        # print(str(str(row["Year"]) + ";" + str(row["Authors"].encode('utf-8')) + ";" + row["Quartil"] + ";" + row["Keywords"] + ";" + str(row["Count"]) + ";" + chr(13)))
        # listKeyYear.write(str(row["Year"]) + ";" + str(row["Authors"].encode('utf-8')) + ";" + row["Quartil"] + ";" + row["Keywords"] + ";" + str(row["Count"]) + ";" + chr(13))

    listKeyYear.close()


with open('articuloRefer.csv', encoding="utf-8") as csv_file:
    # Crea un objeto reader similar a un diccionario delimitado por la barra |
    listFile = csv.DictReader(csv_file, delimiter='|')
    Extract_A_Q_K_from_Refr(listFile)
