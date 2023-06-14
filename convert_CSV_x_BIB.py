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


def generatedRoute():
    # Generamos una variable de la fecha actual
    today = date.today().strftime("%d_%m_%Y")
    # Creamos una ruta con esa variable de fecha y la carpeta donde se guardarán los archivos
    ruta = 'bibtexArtsQuartil/{0}/'.format(today)
    # Preguntamos si ya hay una carpeta creada ese día
    if not os.path.isdir(ruta):
        # Creamos una carpeta para guardar los archivos con la fecha actual y una carpeta predeterminada dentro
        ruta = ruta + '1'
        os.makedirs(ruta)
        print(ruta)
        return ruta
    else:
        # Aquí asignamos un número dependiendo de cuantas carpetas se crearon ese día para crear la carpeta
        numDir = len(os.listdir(ruta)) + 1
        ruta = ruta + '{0}'.format(numDir)
        os.makedirs(ruta)
        return ruta


# Guardado del archivo CSV a BIB
def saveFileBIB(numFile):
    # Itero el objeto db.entries para ir añadiendo al archivo por cada iteración
    writer = BibTexWriter()
    writer.indent = '\n'

    with open("{0}/bibtexArtsQ{1}.bib".format(route, numFile), 'w', encoding='utf8') as bibFile:
        bibFile.write(writer.write(db))


# Genero la ruta de la carpeta donde se guardaran los archivos
route = generatedRoute()
# Aquí tomo los numero del 1 al 4
# para generar los BIB de los 4 quartiles al mismo tiempo
for n in range(1, 5):
    convertCSVxBIB(n)
