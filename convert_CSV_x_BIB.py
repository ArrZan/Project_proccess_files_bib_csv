import csv, os, errno
from datetime import date
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

db = BibDatabase()


# Conversión del archivo CSV a BIB
def convertCSVxBIB(numFile):
    with open("filesCSV/arts{0}.csv".format(numFile), encoding="utf8") as csv_file:
        # Crea un objeto reader similar a un diccionario delimitador por la barra |
        listFile = csv.DictReader(csv_file, delimiter='|')
        bigFile = []

        # Itero el objeto reader para añadirlo en una lista
        for row in listFile:
            bigFile.append(row)
        db.entries = bigFile
        saveFileBIB(numFile)


# Guardado del archivo CSV a BIB
def saveFileBIB(numFile):
    # Itero el objeto db.entries para ir añadiendo al archivo por cada iteración
    writer = BibTexWriter()
    writer.indent = '\n'
    for row in db.entries:
        # Generamos una variable de la fecha actual
        today = date.today().strftime("%d_%m_%Y")
        # Creamos una ruta con esa variable de fecha y la carpeta donde se guardarán los archivos
        ruta = 'bibtexArtsQuartil/{0}/1'.format(today)
        # Preguntamos si ya hay una carpeta creada ese día
        if not os.path.isdir(ruta):
            # Creamos una carpeta para guardar los archivos con la fecha actual
            os.makedirs(ruta)

        with open("{0}/bibtexArtsQ{1}.bib".format(ruta, numFile), 'w', encoding='utf8') as bibFile:
            bibFile.write(writer.write(db))


# Aquí tomo los el numero del 1 al 4
# para generar los BIB de los 4 quartiles al mismo tiempo
for n in range(1, 5):
    convertCSVxBIB(n)
