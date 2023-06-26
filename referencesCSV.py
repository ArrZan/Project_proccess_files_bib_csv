import re

import unidecode as unidecode

# nomarRefSql = "archivos\\referenciasContar"


daniados = []
numLines = 0
nomarRef = "archivos\\referenciasContar"
conarchivo = 1
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
    # Extraemos el año siempre que sea mayor a 1000 o menor 2999
    yearArc = re.search(r'\(([1-2]\d{3})\)', tempRef)

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
        tempauts = vacio

    # Añadimos el valor de año, en caso sea None el valor será 'Vacio'
    data['year'] = vacio if yearArc is None else yearArc.group(1)

    # Unimos los autores en una sola variable siempre y cuando no venga 'vacío'
    if data['authors'][0] != vacio:
        tempauts = ", ".join(data['authors'])
        # tempRef = tempRef.replace(tempauts + ", ", '')
    # tempRef = re.sub(r'^\s|\s$', '', tempRef)

    # reTitle = re.compile(r'(.+)\s\((\d{4})\)')

    # if re.match(r'^\((\d{4})\)', tempRef) is None:  # Preguntamos si el tempRef procesado no comienza con el año entre paréntesis
    #     if re.match(r'^https?:\/\/[\w\-]+(\.[\w\-]+)+[/#?]?.*$', tempRef) is None:  # Preguntamos si lo primero que lee no es una url
    #         if reTitle.match(tempRef) is not None:  # Preguntamos si comienza con un texto(titulo) y luego el año
    #             tempTitle = re.match(r'(.+)\s\((\d{4})\)', tempRef).group(1)  # Extraigo el grupo 1 de "titulo, año"
    #         else:
    #             tempTitle = re.match(r'(.+),\s', tempRef).group(1)
    #     else:
    #         dañados.append(ref)
    #         print('Dañado: ', ref)
    #         break
    # else:
    #     if re.match(r'^[(\d)]{6}[^,]', tempRef) is None:  # Preguntamos si tiene "," después del paréntesis del año
    #         tempTitle = re.match(r'^([^,]+)(,\s)',tempRef).group(1)
    #     else:
    #         tempTitle = re.match(r'\((\d{4})\)\s(.[^,]+)', tempRef).group(2)  # Extraigo el grupo 2 "año, titulo"

    # data['title'] = 'En proceso'

    # Guardamos los datos de autor, el contador de la iteración, el año y la linea(referencia)

    return '"{anio}","{autorFirst}","{autorLast}","{autores}","{cont}","1","{references}"\n'.format(
        autorFirst=data['authors'][0],
        autorLast=data['authors'][-1],
        autores=tempauts,
        cont=conArc,
        anio=data['year'],
        references=ref)


with open("scopusRef2.csv", encoding="utf8") as art:  # Variable que toma el archivo

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
