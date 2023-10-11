import csv, os, errno
from datetime import date
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

db = BibDatabase()


""" Convertidor de archivo bib a csv """

# Conversión de un archivo CSV a BIB
def convertCSVxBIB(numFile):
    with open(f"filesCSV/arts{numFile}.csv", encoding="utf8") as csv_file:
        # Crea un objeto reader similar a un diccionario delimitado por la barra |
        listFile = csv.DictReader(csv_file, delimiter='|')
        bigFile = []

        # Itero el objeto reader para añadirlo en una lista
        for row in listFile:
            bigFile.append(row)
        db.entries = bigFile
        saveFileBIB(numFile)


# Función para generar ruta
def generateRoute(nameFolder):
    # Generamos una variable de la fecha actual
    today = date.today().strftime("%d_%m_%Y")  # día mes y año

    # Creamos una ruta con esa variable de fecha y la carpeta donde se guardarán los archivos
    ruta = f"{nameFolder}/Projects_{today}/"

    # Preguntamos si ya hay una carpeta creada ese día
    if not os.path.isdir(ruta):
        # Creamos una carpeta para guardar los archivos con la fecha actual y una carpeta predeterminada dentro
        ruta = f"{ruta}/Project_1"
        os.makedirs(ruta)
        return ruta

    else:
        # Aquí asignamos un codigo dependiendo del número máximo
        # que haya entre los nombres de las carpetas
        folders = os.listdir(ruta)
        numFolders = [int(folder.split("_")[1]) for folder in folders]
        codeFolder = sorted(numFolders, reverse=True)[0]
        ruta = f"{ruta}/Project_{codeFolder + 1}"
        os.makedirs(ruta)
        return ruta


# Guardado del archivo CSV a BIB
def saveFileBIB(numFile):
    writer = BibTexWriter()
    writer.indent = '\n'

    with open(f"{route}/bibtexArtsQ{numFile}.csv", 'w', encoding='utf8') as bibFile:
        bibFile.write(writer.write(db))


# Genero la ruta de la carpeta donde se guardaran los archivos
route = generateRoute("History Projects")

# Aquí tomo los numero del 1 al 4
# para generar los BIB de los 4 quartiles al mismo tiempo
# Itero el objeto db.entries para ir añadiendo al archivo por cada iteración
# for n in range(1, 5):
#     convertCSVxBIB(n)
