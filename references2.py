import re

import unidecode as unidecode

# nomarRefSql = "archivos\\referenciasContar"


# Genero el archivo y la cabecera para guardar toda la info

daniados = []
numLines = 0


def references(file):
    global tempauts
    bandera = 0
    nomarRef = "archivos\\referenciasContar"

    linea = ar.readline()  # cabecera
    linea = ar.readline()  # primera referencia
    conArc = 1
    authors = []
    conarchivo = 1

    with open(nomarRef + str(conarchivo) + ".csv", "w", encoding="utf8") as arRef:
        arRef.write("year,authorFirst, authorLast, authors,article,number,line\n")

    with open("referenciasDañadas.csv", "w", encoding="utf-8") as refDa:
        refDa.write('articulo\n')

    for linea in file:
        refArt = linea.split(";")
        for ref in refArt:
            if re.search(r',', ref) is None:  # Preguntamos si no es un valor bruto
                with open("referenciasDañadas.csv", "a", encoding="utf-8") as refDa:
                    refDa.write(ref + "\n")
            else:
                # Guardaremos los datos de autores, title y año
                data = {}
                reAnio = re.compile(r'\((\d{4})\)')
                reTitle = re.compile(r'(.+)\s\((\d{4})\)')

                unidecode.unidecode(ref)

                # Elimino las lineas que empiezan con una comilla o espacio o si están al final
                ref = re.sub(r'^\s|\s$|^"|"$', '', ref)

                tempRef = ref
                # Buscamos los autores de la línea con el siguiente regex
                authors = re.findall(r'([a-zA-ZÀ-ÿ .-]+,\s([A-Z].-[A-Z].|[A-Z].)+)+,\s', ref)
                yearArc = reAnio.search(ref)

                data['authors'] = []

                if len(authors) > 1:
                    for value in authors:
                        data['authors'].append(value[0])

                elif len(authors) == 1:
                    data['authors'].append(authors[0][0])

                else:
                    data['authors'].append('Vacio')
                    tempauts = 'Vacio'

                if yearArc is None:
                    data['year'] = 'Vacio'
                else:
                    data['year'] = yearArc.group(1)

                if data['authors'][0] != 'Vacio':
                    tempauts = ", ".join(data['authors'])
                    tempRef = tempRef.replace(tempauts + ", ", '')
                tempRef = re.sub(r'^\s|\s$', '', tempRef)

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

                lineSave = '"{anio}","{autorFirst}","{autorLast}","{autores}","{cont}","1","{linea}"\n'.format(
                    autorFirst=data['authors'][0],
                    autorLast=data['authors'][-1],
                    autores=tempauts,
                    cont=conArc,
                    anio=data['year'],
                    linea=ref)

                with open(nomarRef + str(conarchivo) + ".csv", "a", encoding="utf8") as arRef:
                    arRef.write(lineSave)

        conArc += 1

    print('Dañados: ', len(daniados))
    for i in daniados:
        print(i)


with open("scopusRef2.csv", encoding="utf8") as ar:  # Variable que toma el archivo
    references(ar)
