import re

import bibtexparser
import unidecode as unidecode

# nomarRefSql = "archivos\\referenciasContar"


daniados = []
numLines = 0
nomarRef = "archivos\\referenciasContar"
conArc = 1
vacio = 'Vacio'


def addReference(refr):
    # Guardaremos los datos de autores, title y año
    data = {}
    # Transformo los caracteres con diéresis a su forma básica (ä -> a)
    unidecode.unidecode(refr)

    # Elimino las lineas que empiezan con una comilla o espacio o si están al final
    refr = re.sub(r'^\s|\s$|^"|"$', '', refr)

    tempRef = refr
    # Buscamos los autores de la línea con el siguiente regex
    authors = re.findall(r'([a-zA-ZÀ-ÿ .-]+,\s([A-Z].-[A-Z].|[A-Z].)+)+,\s', tempRef)
    yearArc = re.search(r'\((\d{4})\)', tempRef)

    data['authors'] = []

    # Sacamos el primer y último autor en caso que exista sino 'vacío'
    if len(authors) > 1:
        # Agregamos todos los autores
        for value in authors:
            data['authors'].append(value[0])

    elif len(authors) == 1:
        data['authors'].append(authors[0][0])

    else:
        data['authors'].append(vacio)

    # Añadimos el valor de año, en caso sea None el valor será 'vacio'
    data['year'] = vacio if yearArc is None else yearArc.group(1)

    # Unimos los autores en una sola variable siempre y cuando no venga 'vacío'
    tempauts = ", ".join(data['authors']) if data['authors'][0] != vacio else vacio
        

    return '"{anio}","{autorFirst}","{autorLast}","{autores}","{cont}","1","{references}"\n'.format(
        autorFirst=data['authors'][0],
        autorLast=data['authors'][-1],
        autores=tempauts,
        cont=conArc,
        anio=data['year'],
        references=ref)


with open("unidos.bib", encoding="utf8") as bibtex_file:  # Variable que toma el archivo
    bib_database = bibtexparser.load(bibtex_file)
    entries = bib_database.get_entry_list()
    # Genero el archivo y la cabecera para guardar toda la info
    with open(nomarRef + str(conarchivo) + ".csv", "w", encoding="utf8") as arRef:
        arRef.write("year,authorFirst, authorLast, authors,article,number,line\n")

    # Genero el archivo de errores
    with open("referenciasDañadas.csv", "w", encoding="utf-8") as refDa:
        refDa.write('articulo\n')

    for linea in art:

        refs = linea.split(";")

        for ref in refs:
            if re.search(r',', ref) is None:  # Preguntamos si no es un valor bruto
                with open("referenciasDañadas.csv", "a", encoding="utf-8") as refDan:
                    refDan.write(ref + "\n")
            else:

                lineSave = addReference(ref)
                with open(nomarRef + str(conarchivo) + ".csv", "a", encoding="utf8") as arRef:
                    arRef.write(lineSave)
        conArc += 1

    print('Dañados: ', len(daniados))
    for i in daniados:
        print(i)

print('Artículos: {0} entries in file'.format(len(entries1)))
