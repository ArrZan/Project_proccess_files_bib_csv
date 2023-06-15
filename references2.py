import re

ar = open("scopusRef.csv", encoding="utf8")
nomarRef = "archivos\\referenciasContar"
nomarRefSql = "archivos\\referenciasContar"

bandera = 0
# arRef=open("referenciasContar.csv","w", encoding="utf8")
# arRef.write("author,archivo\n")
# arRef1=open("referenciasContar.sql","w", encoding="utf8")
linea = ar.readline()  # cabecera
linea = ar.readline()  # primera referencia
conArc = 1
authors = []
conarchivo = 1
confila = 1
for linea in ar:
    print(conArc, linea)
    refArt = linea.split(";")
    for ref in refArt:
        pass