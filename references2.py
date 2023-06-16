import re

ar = open("scopusRef.csv", encoding="utf8")  # Varible que toma
# tsodo el archivo
nomarRef = "archivos\\referenciasContar"
nomarRefSql = "archivos\\referenciasContar"

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
        data = {}
        tempRef = ref
        autores1 = re.findall(r'([a-zA-ZÀ-ÿ .-]+,\s([A-Z].-[A-Z].|[A-Z].)+)+,\s', ref) #  83
        añoArc = re.search(r'([(\d)]{6}){1}', ref) #  85

        # tempRef = tempRef.replace(autores1.group(1),'')
        # tempRef = tempRef.replace(añoArc.group(1),'')
        data['autores'] = []
        if len(autores1) > 1:
            for value in autores1:
                data['autores'].append(value[0])
        else:
            data['autores'].append(autores1[0][0])

        data['año'] = añoArc.group(1)

        if tempRef[0] == "(":
            pass
        ar.close()