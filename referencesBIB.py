import re

import bibtexparser

from referencesCSV import addReference
import unidecode as unidecode

# nomarRefSql = "archivos\\referenciasContar"


daniados = []  # Guardamos los archivos que no se pueden procesar por que no cumplen con los parametros
# numLines = 0
nomarRef = "archivos\\referenciasContar"  # Dirección y nombre del archivo csv
conArc = 1  # Contador para el Artículo
vacio = 'Vacio'
ArtSinRef = 0  # Contador para los artículos sin referencia


def addReferenceWoS(refr):
    # Transformo los caracteres con diéresis a su forma básica (ä -> a)
    unidecode.unidecode(refr)

    # Separamos los campos de la referencia
    tempRef = refr.split(',')

    # Variable para indicar si existe y toma el valor del año
    yearExiste = re.search(r'(\d{4})', tempRef[1])

    # Si es None, pondrá vacio, si no tomará el año
    year = vacio if yearExiste is None else yearExiste.group(1)

    return '"{anio}","{autorFirst}","{autorLast}","{autores}","{cont}","1","{references}"\n'.format(
        anio=year,
        autorFirst=tempRef[0],
        autorLast=tempRef[0],
        autores=tempRef[0],
        cont=conArc,
        references=refr)


with open("prueba.bib", encoding="utf-8") as bibtex_file:  # Variable que toma el archivo
    bib_database = bibtexparser.load(bibtex_file)
    listArticulos = bib_database.get_entry_list()

    # Genero el archivo y la cabecera para guardar toda la info
    with open(nomarRef + "1.csv", "w", encoding="utf-8") as arRef:
        arRef.write("year, authorFirst, authorLast, authors, article, number, line\n")

    # Genero el archivo de errores
    with open("referenciasDañadas.csv", "w", encoding="utf-8") as refDa:
        refDa.write('articulo\n')

    for articulo in listArticulos:
        refersExiste = True

        if 'references' in articulo:
            formatReferencia = 'references'
        elif 'cited-references' in articulo:
            formatReferencia = 'cited-references'
        else:
            refersExiste = False

        if refersExiste:
            listRefers = articulo[formatReferencia]

            listRefers = listRefers.split(';') if formatReferencia == 'references' else re.findall(r'\S.+\.',
                                                                                                   listRefers)
            for refer in listRefers:
                if formatReferencia == 'cited-references':
                    # Separamos los datos de la referencia por los campos que tenemos
                    lineSave = addReferenceWoS(refer)
                else:
                    if re.search(r',', refer) is None:  # Preguntamos si no es un valor bruto
                        # Si está dañado se lo guarda en este archivo
                        with open("referenciasDañadas.csv", "a", encoding="utf-8") as refDan:
                            refDan.write(refer + "\n")
                    else:
                        # Separamos los datos de la referencia por los campos que tenemos
                        lineSave = addReference(refer)

                # Añadimos la referencia al archivo
                with open(nomarRef + "1.csv", "a", encoding="utf-8") as arRef:
                    arRef.write(lineSave)

        else:
            print('dañado', articulo)
            # with open("referenciasDañadas.csv", "a", encoding="utf-8") as refDan:
            #     refDan.write(articulo + "\n")
            # ArtSinRef += 1

        conArc += 1

    print('Dañados: ', len(daniados))
    for i in daniados:
        print(i)

