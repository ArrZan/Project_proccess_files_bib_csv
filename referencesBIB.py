import re
import bibtexparser
import unidecode as ud

# nomarRefSql = "archivos\\referenciasContar"


daniados = []  # Guardamos los archivos que no se pueden procesar por que no cumplen con los parametros
nomarRef = "archivos\\referenciasContar"  # Dirección y nombre del archivo csv
conArc = 1  # Contador para el Artículo
numRefArts = 0  # Número de referencias de todos los artículos
vacio = 'Vacio'
ArtSinRef = 0  # Contador para los artículos sin referencia

TopAuthors = {}  # Diccionario de los autores y de la cantidad de veces que fueron referenciados

# Lista de diccionarios, con lista de diccionarios y así hasta 9 veces en total con todos:
# [{indice: [{autor: [{year: [{autores: [title1, ... title n]}]}]}]}]
index = {}
complete = 0  # Porcentaje de completado
pruebas = []


def addReference(refr, autorArt, anioArt):
    # Guardaremos los datos extraídos de la referencia (year,authorFirst, authorLast, authors,article,number,line)
    data = {}
    # Transformo los caracteres con diéresis a su forma básica (ä -> a)
    ud.unidecode(refr)

    # Elimino las lineas que empiezan con una comilla o espacio o si están al final
    refr = re.sub(r'^\s|\s$|^"|"$', '', refr)

    tempRef = refr
    # Buscamos los autores de la línea con el siguiente regex
    authors = re.findall(r"(([-\w'? ]+),\s(([A-Z-]\.?\s?)+)),", tempRef)

    # Extraemos el año siempre que sea mayor a 1000 o menor 2999
    yearExiste = re.search(r'\(([1-2]\d{3})\)', tempRef)

    # Si es None, pondrá vacio, si no tomará el año
    yearRef = vacio if yearExiste is None else yearExiste.group(1)

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

    primerAutor = data['authors'][0]
    # Unimos los autores en una sola variable siempre y cuando no venga 'vacío'
    if primerAutor != vacio:
        # Unimos todos los autores con una coma
        tempauts = ", ".join(data['authors'])

        # Añadir los autores
        TopAuthors[primerAutor] = TopAuthors[primerAutor] + 1 if primerAutor in TopAuthors else 1

    posLastAut = 0

    for author in authors:
        posLastAut = posLastAut + len(author[0]) + 2

    title = refr

    if yearRef != vacio:
        posYear = yearExiste.regs[0][1]
        # Si el año está al comienzo... year, author, title
        if yearExiste.regs[0][0] == 0:
            posComa = refr.find(",")
            title = refr[posYear + 1:posComa]  # Sumamos 1 por la coma o espacio
        # Si el año está en la mitad... author, year, title
        elif "," in refr[posYear - 9:posYear]:
            if re.search(r',\s\d+\s\(\d+\)', refr) is not None:
                posVolNum = re.search(r',\s\d+\s\(\d+\)', refr).group()
                posEnd = refr[posYear:].find(posVolNum)
            elif ", pp" in refr:
                posEnd = refr[posYear:].find(", pp")
            elif ", ," in refr:
                posEnd = refr[posYear:].find(", ,")
            else:
                posEnd = refr[posYear:].find(",")

            title = refr[posYear:posEnd + posYear]
        else:
            title = refr[posLastAut:posYear - 6]  # Restamos por el len de year
    else:
        pruebas.append(refr)

    data['firstAuthor'] = primerAutor
    data['year'] = yearRef
    data['refr'] = refr
    data['line'] = (f'"{anioArt}"|"{autorArt}"|"{yearRef}"|"{data["authors"][0]}"|"{data["authors"][-1]}"|'
                    f'"{tempauts}"|"{conArc}"|"1"|"{refr}"|"{title}"\n')

    return data


def quest_name_refer(articulo):
    if 'references' in articulo:
        return 'references'
    elif 'cited-references' in articulo:
        return 'cited-references'
    else:
        # No existe
        return False


def addReferenceWoS(refr, autorArt, anioArt):
    # Transformo los caracteres con diéresis a su forma básica (ä -> a)
    ud.unidecode(refr)
    data = {}

    # Separamos los campos de la referencia
    tempRef = refr.split(',')

    # Variable para indicar si existe y toma el valor del año
    if len(tempRef) > 1:
        yearExiste = re.search(r'(\d{4})', tempRef[1])
        yearRef = vacio if yearExiste is None else yearExiste.group(1)
    else:
        yearRef = vacio

    autorRef = tempRef[0]

    if tempRef[0] is not vacio:
        if "Anonymous" not in tempRef[0]:
            # Añadir los autores
            TopAuthors[autorRef] = TopAuthors[autorRef] + 1 if autorRef in TopAuthors else 1
        else:
            autorRef = vacio

    DOIexiste = re.search(r'(DOI)\s(.+)', tempRef[-1])
    DOI = tempRef[-1] if DOIexiste is None else DOIexiste.group(2)

    data["firstAuthor"] = autorRef
    data["authors"] = autorRef
    data["year"] = yearRef
    data["title"] = DOI
    data["line"] = (f'"{anioArt}"|"{autorArt}"|"{yearRef}"|"{autorRef}"|"{autorRef}"|"{autorRef}"|"{conArc}"|"1"'
                    f'|"{refr}"|"{DOI}"\n')

    return data


def groupingTitles(f_author, authors, year, title, f_lett):
    if f_author != vacio:
        if f_lett.lower() in index:
            if f_author in index[f_lett]:
                if year in index[f_lett][f_author]:
                    if authors in index[f_lett][f_author][year]:
                        if title in index[f_lett][f_author][year][authors]:
                            pass

        # for letters in index:
        #     if letters['indice'] == f_lett:
        #         for authors_i in letters[f_lett]:
        #             if authors_i['authors'] == f_author:
        #     else:

    # else:
    # print(refr)


'''/////////////////////////////////////////////// Codigo para leer un archivo bib, iterar cada articulo
e ir extrayendo las referencias para extraer los autores de la referencia, el año y la referencia misma
para añadirla como columna.'''

with open("merged.bib", encoding="utf-8") as bibtex_file:  # Variable que toma el archivo
    bib_database = bibtexparser.load(bibtex_file)
    listArticulos = bib_database.get_entry_list()
    print('Artículos: {0} entries in file'.format(len(listArticulos)))

    # Genero el archivo y la cabecera para guardar toda la info
    with open(nomarRef + "1.csv", "w", encoding="utf-8") as arRef:
        """ AÑADIR UNA NUEVA COLUMNA LLAMADA TITLE
        
            EXTRAER LA FRECUENCIA DE LOS TITULOS QUE SE REPITEN,
            COMO TIENEN MINÚSCULAS Y MAYÚSCULAS, TILDES, YA QUE ESTAS
            COMPLICAN A LA HORA DE VER QUE TANTO SE REPITEN.
                        
            Carl M., (2000) Agency Theory of last, CEO, california
            Carl M., (2000) Agency Theory of Last, CEO, , america
            Carl M., (2000) agency theory of last, Ceo, journal
            Carl M., agency theory of last, Ceo (2000)
            Famm S., Crish S., (1997) the firm of
            Famm S., Crish S., the firm of (1997)
            Famm S., Crish S., (1997) the Firm of, calif 
            Famm S., Crish S., (1997) The Firm Of, cali
            Bar C, the firm of (2000)
            
            VER QUE TANTO SE PARECEN UNAS CADENAS DE CARACTERES COMO LA DE ARRIBA
            BUSCAR EL NIVEL DE SIMILITUD ENTRE REFERENCIAS PARA SACAR UNA FRECUENCIA.
        
        """
        arRef.write("yearArticle| authorArticle| year| authorFirst| authorLast|"
                    " authors| article| number| line| title\n")

    # Genero el archivo de errores
    with open("referenciasDañadas.csv", "w", encoding="utf-8") as refDa:
        refDa.write('articulo\n')

    for articulo in listArticulos:
        # Agregamos los autores
        if 'author' in articulo:
            autor = articulo['author']
        elif 'authors' in articulo:
            autor = articulo['authors']
        else:
            autor = vacio

        # Tomo el primer autor
        autorArt = autor.split(' and ')[0]

        # Tomo el año si existe
        yearArt = articulo['year'] if 'year' in articulo else vacio

        formatReferencia = quest_name_refer(articulo)

        if formatReferencia:
            listRefers = articulo[formatReferencia]

            listRefers = listRefers.split(';') if formatReferencia == 'references' else re.findall(r'\S.+\.',
                                                                                                   listRefers)

            numRefArticle = len(listRefers)  # número de referencias del artículo
            numRefArts += numRefArticle  # Acumulador de todas las referencias del archivo
            complRefArticle = 0  # Porcentaje de las referencias del artículo
            conrefArticle = 1  # Número de las referencias del artículo

            for refer in listRefers:
                if formatReferencia == 'cited-references' and 'No title captured' not in refer:
                    # Separamos los datos de la referencia por los campos que tenemos
                    dataRef = addReferenceWoS(refer, autorArt, yearArt)
                else:
                    if re.search(r',', refer) is None:  # Preguntamos si no es un valor bruto
                        # Si está dañado se lo guarda en este archivo
                        with open("referenciasDañadas.csv", "a", encoding="utf-8") as refDan:
                            refDan.write(refer + "\n")
                    else:
                        # Separamos los datos de la referencia por los campos que tenemos
                        dataRef = addReference(refer, autorArt, yearArt)

                # Añadimos la referencia al archivo
                with open(nomarRef + "1.csv", "a", encoding="utf-8") as arRef:
                    arRef.write(dataRef['line'])

                # Proceso para titulos duplicados de las referencias de un artículo
                # En algún momento si se ve necesario preguntaremos si queremos hacer este proceso u obviarlo,
                # para disminuir tiempos.

                # if decission:
                # groupingTitles(dataRef['firstAuthor'], dataRef['authors'], dataRef['year'], dataRef['refr'],
                #                dataRef['refr'][0])

                complRefArticle = round(conrefArticle / numRefArticle * 100, 2)
                print(f"Artículo: {conArc}  |  referencias: {conrefArticle}/{numRefArticle}  |  {dataRef['firstAuthor']}")

                conrefArticle += 1

        else:
            daniados.append(articulo)

        complete = round(conArc / len(listArticulos) * 100, 2)
        print(f"Artículos: {conArc}/{len(listArticulos)}  |  Porcentaje: {complete}%  |  Título: {articulo['title']}")

        conArc += 1

print('Articulos: ', conArc-1)
print('Artículos sin referencias: ', len(daniados))
print('Referencias de artículos: ', numRefArts)

for pr in pruebas:
    print(pr)

"""/////////////////////////////"""
print("*"*50, "\nREFERENCIAS EXTRAIDAS...[COMPLETADO]\n", "*"*50 ,"\n")
"""/////////////////////////////"""

'''/////////////////////////////////////////////// Codigo para sacar los autores top.'''
# Ordeno (sorted) el TopAuthors de mayor a menor por valor
sortedAuthors = {key: value for key, value in sorted(TopAuthors.items(), key=lambda item: item[1], reverse=True)}

# Creo el top donde guardaré los primeros 10 autores más referenciados
Top10Authors = {}
Top = 10  # Coloco el top que deseo, puede ser el top 100 o 5

# Añado los 10 autores y su cantidad
for key, quant in sortedAuthors.items():

    Top10Authors[key] = quant
    # Pregunto por el top
    # if len(Top10Authors) < Top:
    #     Top10Authors[key] = quant
    # else:
    #     # Salgo cuando los tenga a los 10
    #     break

"""/////////////////////////////"""
print("*"*50, "\nTOP DE AUTORES...[COMPLETADO]\n", "*"*50 ,"\n")
"""/////////////////////////////"""

'''/////////////////////////////////////////////// Codigo para guardar el abstract de los 10 autores.'''

# Guardamos los autores(como key) y año y abstract's (como value en una lista)
abstractsAut = {}

for article in listArticulos:
    # Preguntamos si existe un abstract en el artículo
    if 'abstract' in article:
        formatReferencia = quest_name_refer(article)
        if formatReferencia:
            for autor in Top10Authors:
                # Se pregunta si el autor iterado del Top está dentro de las referencias del artículo
                if autor in article[formatReferencia]:
                    # Codigo y el abstracto convertido con unidecode
                    codeArticle = ud.unidecode(article['code'])
                    abstractArticle = ud.unidecode(article['abstract'])
                    # Si existe se añadirá una  nueva referencia
                    if autor in abstractsAut:
                        abstractsAut[autor][1].update({codeArticle: abstractArticle})
                    else:
                        # Si no, se lo crea
                        abstractsAut[autor] = [article['year'], {codeArticle: abstractArticle}]
                        # articleExists = True

        # file_Text.write("**** *")


# Ordeno un diccionario desordenado comparándolo con otro igual (llaves iguales) pero ordenado
def sortDict(dictionary_ordered, dictionary_messy):
    orderedData = {}
    # Pregunto si tienen las mismas claves
    if set(dictionary_ordered.keys()) != set(dictionary_messy.keys()):
        return False

    # Itero para ordenarlo en caso las llaves sean iguales
    for key in dictionary_ordered:
        orderedData[key] = dictionary_messy[key]
    return orderedData


abstractsAutOrder = sortDict(Top10Authors, abstractsAut)
cont = 1
if abstractsAutOrder:
    for key, content in abstractsAutOrder.items():
        abstracts = content[1]
        # Guardamos por cada autor los abstract en un solo archivo de texto
        # with open(f"FilesAbstracts/abstract_{key}_{cont}.txt", "a", encoding="utf-8") as fileTxt:
        with open(f"FilesAbstracts/abstractALL.txt", "a", encoding="utf-8") as fileTxt:
            # print("*" * 10, f"{key} : {len(abstracts)}", "*" * 10)
            for key2, abstract in abstracts.items():
                fileTxt.write(f"**** *ID_{key2}_{content[0]}_\n{abstract}\n")
        cont += 1

print("*" * 20, f"Reporte del Top de {Top} autores", "*" * 20)
print("Autor | Conteo")
for autor, conteo in Top10Authors.items():
    print(f"{autor}: {conteo}")


"""/////////////////////////////"""
print("*"*50, "\nLISTA DE ABSTRACTS...[COMPLETADO]\n", "*"*50, "\n")
"""/////////////////////////////"""
