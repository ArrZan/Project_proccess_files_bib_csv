import re

import unidecode as unidecode

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
        articulo = ref.strip("\"")
        articulo = re.sub(",", "", articulo)
        articulo = re.sub("/", "", articulo)
        # articulo = re.sub("\\", "", articulo)
        articulo = re.sub("'", "", articulo)

        unidecode.unidecode(articulo)

        # articulo = articulo.replace("Á", "A")
        # articulo = articulo.replace("É", "A")
        # articulo = articulo.replace("Í", "I")
        # articulo = articulo.replace("Ó", "O")
        # articulo = articulo.replace("Ú", "U")
        #
        # articulo = articulo.replace("á", "a")
        # articulo = articulo.replace("é", "e")
        # articulo = articulo.replace("í", "i")
        # articulo = articulo.replace("ó", "o")
        # articulo = articulo.replace("ú", "u")
        #
        # articulo = articulo.replace("ä", "a")
        # articulo = articulo.replace("Ä", "A")
        # articulo = articulo.replace("ë", "e")
        # articulo = articulo.replace("Ë", "E")
        # articulo = articulo.replace("ï", "i")
        # articulo = articulo.replace("Ï", "I")
        # articulo = articulo.replace("ö", "o")
        # articulo = articulo.replace("Ö", "o")
        # articulo = articulo.replace("ü", "u")
        # articulo = articulo.replace("Ü", "U")

        segRef = ref.split(",")
        conSeg = len(segRef)
        conelSeg = 0
        banderaT = 0
        while conelSeg < conSeg:
            if banderaT == 0:
                if segRef[conelSeg].__len__() <= 20 and conelSeg < conSeg - 1:
                    par1 = segRef[conelSeg]
                    par1 = re.sub("'", "", par1)
                    par1 = re.sub("\"", "", par1)
                    # par1 = re.sub("\\", "", par1)
                    par2 = segRef[conelSeg + 1]
                    par2 = re.sub("'", "", par2)
                    par2 = re.sub("\"", "", par2)

                    articulo = re.sub("\"", "", articulo)
                    articulo = re.sub("'", "", articulo)

                    author = par1.strip() + " " + par2.strip()
                    author = author[0:200]
                    authors.append([author, conArc])
                    author = "\"" + author + "\",\"" + str(conArc) + "\",1,\"" + articulo + "\"\n"
                    ##+ articulo.strip(",") + "\");\n"
                    sql = "INSERT INTO  \"public\".\"SRHM\" (authors,articulo) values(\'" + par1.strip().strip(
                        ",") + " " + par2.strip().strip(",") + "\',\'" + articulo.strip(",") + "\');\n"

                    if bandera == 0:
                        arRef = open(nomarRef + str(conarchivo) + ".csv", "w", encoding="utf8")
                        arRefsql = open(nomarRefSql + str(conarchivo) + ".sql", "w", encoding="utf8")
                        arRef.write("authors,articulo,numero,linea\n")
                        arRef.write(author)
                        arRefsql.write(sql)
                        bandera = 1
                        confila = 1
                    else:
                        arRef.write(author)
                        arRefsql.write(sql)
                        confila += 1
                        if confila > 200000:
                            bandera = 0
                            arRef.close()
                            arRefsql.close()
                            conarchivo += 1
                    conelSeg += 2
                else:
                    conelSeg += 1
                    banderaT = 1
            else:
                conelSeg += 1

        print(conArc, ref)
    conArc += 1

"""
authorsFinal=[]
arc1=open("authors.csv","w",encoding="utf8")
arc1.write("authos\n")
for authorx in authors:
    if authorx[0] not in authorsFinal:
        authorsFinal.append(authorx)
        arc1.write("\"" + authorx[0]+"\"\n")
arc1.close()
print("total: ",str(authorsFinal.__len__()))
AutCompleto=[]
for aut in authorsFinal:
    AutCompleto.append([aut[0],0])
print(AutCompleto.__len__())

for i in range(len(AutCompleto)):
    for autArt in authors:
        print(AutCompleto[i][0])
        print(autArt[0])
        if AutCompleto[i][0]==autArt[0]:
            AutCompleto[i][1]+=1
arf=open("authorsConteo.csv","w",encoding="utf8")
arf.write("authors,con\n")
for aut in AutCompleto:
    arf.write("\"" + aut[0] + "\"," + str(aut[1])+"\n")
arf.close()
arRef.close()
##arRef1.close()
ar.close()

"""
