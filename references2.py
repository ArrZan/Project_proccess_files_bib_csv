import re

import unidecode as unidecode

ar = open("scopusRef.csv", encoding="utf8")  # Varible que toma
# tsodo el archivo
nomarRef = "archivos\\referenciasContar"
# nomarRefSql = "archivos\\referenciasContar"

bandera = 0

linea = ar.readline()  # cabecera
linea = ar.readline()  # primera referencia
conArc = 1
authors = []
conarchivo = 1
confila = 1
for linea in ar:
    # print(conArc, linea)
    refArt = linea.split(";")
    for ref in refArt:
        if re.search(r',', ref) is None:  # Preguntamos si no es un valor bruto
            print('Dañado')
        else:
            # Guardaremos los datos de autores, title y año
            data = {}
            unidecode.unidecode(ref)

            # Elimino el comienzo de una comilla o el final de una
            ref = re.sub(r'^"|"$', '', ref)

            tempRef = ref.strip("\"")
            tempRef = re.sub(",", "", tempRef)
            tempRef = re.sub("/", "", tempRef)
            tempRef = re.sub("'", "", tempRef)

            tempRef = ref
            # Buscamos los autores de la línea con el siguiente regex
            authors = re.findall(r'([a-zA-ZÀ-ÿ .-]+,\s([A-Z].-[A-Z].|[A-Z].)+)+,\s', ref)
            yearArc = re.search(r'([(\d)]{6})', ref)

            data['authors'] = []

            if len(authors) > 1:
                for value in authors:
                    data['authors'].append(value[0])
            elif len(authors) == 1:
                data['authors'].append(authors[0][0])
            else:
                data['authors'].append('Vacio')

            data['year'] = yearArc.group(1)

            tempauts = ", ".join(data['authors']) + ", "
            tempRef = tempRef.replace(tempauts, '')
            tempRef = re.sub(r'^\s|\s$', '', tempRef)

            # if re.match(r'^[(\d)]{6}', tempRef) is None:  # Preguntamos si el tempRef procesado comienza con el año
            if re.match(r'^[(\d)]{6}', tempRef) is None:  # Preguntamos si el tempRef procesado comienza con el año
                tempTitle = re.search(r'(.+)\s([(\d)]{6})', tempRef).group(1)  # Extraigo el grupo 1 de "titulo, año"
            else:
                tempTitle = re.search(r'([(\d)]{6})\s(.[^,]+)', tempRef).group(2)  # Extraigo el grupo 2 "año, titulo"

            data['title'] = tempTitle

            lineSave = '"{anio}","{autorFirst}",""{autorLast}","{autores}","{cont}","1","{titulo}","{linea}"'.format(
                autorFirst=data['authors'][0],
                autorLast=data['authors'][-1],
                autores=data['authors'],
                cont=conArc,
                anio=data['year'],
                titulo=data['title'],
                linea=ref)

            if bandera == 0:
                arRef = open(nomarRef + str(conarchivo) + ".csv", "w", encoding="utf8")
                arRef.write("year,authorFirst, authorLast, authors,article,number,title,line\n")
                arRef.write(lineSave)
                bandera = 1
                confila = 1
                arRef.close()
            else:
                arRef = open(nomarRef + str(conarchivo) + ".csv", "w", encoding="utf8")
                arRef.write(lineSave)
                arRef.close()

    conArc += 1

ar.close()
