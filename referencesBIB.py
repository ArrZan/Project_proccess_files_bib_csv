import re

import bibtexparser

import unidecode as unidecode

# nomarRefSql = "archivos\\referenciasContar"


daniados = []  # Guardamos los archivos que no se pueden procesar por que no cumplen con los parametros
# numLines = 0
nomarRef = "archivos\\referenciasContar"  # Dirección y nombre del archivo csv
conArc = 1  # Contador para el Artículo
vacio = 'Vacio'
ArtSinRef = 0  # Contador para los artículos sin referencia

TopAuthors = {}  # Diccionario de los autores y de la cantidad de veces que fueron referenciados

def addReference(refr, autorArt, anioArt):
    # Guardaremos los datos extraídos de la referencia (year,authorFirst, authorLast, authors,article,number,line)
    data = {}
    # Transformo los caracteres con diéresis a su forma básica (ä -> a)
    unidecode.unidecode(refr)

    # Elimino las lineas que empiezan con una comilla o espacio o si están al final
    refr = re.sub(r'^\s|\s$|^"|"$', '', refr)

    tempRef = refr
    # Buscamos los autores de la línea con el siguiente regex
    authors = re.findall(r'([a-zA-ZÀ-ÿ .-]+,\s([A-Z].-[A-Z].|[A-Z].)+)+,\s', tempRef)
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

    return f'"{anioArt}","{autorArt}","{yearRef}","{data["authors"][0]}","{data["authors"][-1]}","{tempauts}","{conArc}","1","{refr}"\n'


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
    unidecode.unidecode(refr)

    # Separamos los campos de la referencia
    tempRef = refr.split(',')

    # Variable para indicar si existe y toma el valor del año
    yearExiste = re.search(r'(\d{4})', tempRef[1])

    if tempRef[0] is not vacio:
        # Añadir los autores
        TopAuthors[tempRef[0]] = tempRef[0] + 1 if tempRef[0] in TopAuthors else 1

    # Si es None, pondrá vacio, si no tomará el año
    yearRef = vacio if yearExiste is None else yearExiste.group(1)

    return f'"{anioArt}","{autorArt}","{yearRef}","{tempRef[0]}","{tempRef[0]}","{tempRef[0]}","{conArc}","1","{refr}"\n'


'''/////////////////////////////////////////////// Codigo para leer un archivo bib, iterar cada articulo
e ir extrayendo las referencias para extraer los autores de la referencia, el año y la referencia misma
para añadirla como columna.'''

listArticulos = []

with open("merged.bib", encoding="utf-8") as bibtex_file:  # Variable que toma el archivo
    bib_database = bibtexparser.load(bibtex_file)
    listArticulos = bib_database.get_entry_list()

    # Genero el archivo y la cabecera para guardar toda la info
    with open(nomarRef + "1.csv", "w", encoding="utf-8") as arRef:
        arRef.write("yearArticle, authorArticle, year, authorFirst, authorLast, authors, article, number, line\n")

    # Genero el archivo de errores
    with open("referenciasDañadas.csv", "w", encoding="utf-8") as refDa:
        refDa.write('articulo\n')

    for articulo in listArticulos:

        # Agregamos el autor
        if 'author' in articulo:
            autor = articulo['author']
        elif 'authors' in articulo:
            autor = articulo['authors']
        else:
            autor = vacio

        autor = autor.split(' and ')[0]

        year = articulo['year'] if 'year' in articulo else vacio

        formatReferencia = quest_name_refer(articulo)

        if formatReferencia:
            listRefers = articulo[formatReferencia]

            listRefers = listRefers.split(';') if formatReferencia == 'references' else re.findall(r'\S.+\.',
                                                                                                   listRefers)
            for refer in listRefers:
                if formatReferencia == 'cited-references' and 'No title captured' not in refer:
                    # Separamos los datos de la referencia por los campos que tenemos
                    lineSave = addReferenceWoS(refer, autor, year)
                else:
                    if re.search(r',', refer) is None:  # Preguntamos si no es un valor bruto
                        # Si está dañado se lo guarda en este archivo
                        with open("referenciasDañadas.csv", "a", encoding="utf-8") as refDan:
                            refDan.write(refer + "\n")
                    else:
                        # Separamos los datos de la referencia por los campos que tenemos
                        lineSave = addReference(refer, autor, year)

                # Añadimos la referencia al archivo
                with open(nomarRef + "1.csv", "a", encoding="utf-8") as arRef:
                    arRef.write(lineSave)

        else:
            daniados.append(articulo)

        conArc += 1

print('Articulos: ', conArc)
print('Dañados: ', len(daniados))


'''/////////////////////////////////////////////// Codigo para sacar los autores top.'''
# Ordeno (sorted) el TopAuthors de mayor a menor por valor
sortedAuthors = {key: value for key, value in sorted(TopAuthors.items(), key=lambda item: item[1], reverse=True)}

# Creo el top donde guardaré los primeros 10 autores más referenciados
Top10Authors = {}
Top = 10

# Añado los 10 autores y su cantidad
for key, quant in sortedAuthors.items():
    # Pregunto por el top
    if len(Top10Authors) < Top:
        Top10Authors[key] = quant
    else:
        # Salgo cuando los tenga a los 10
        break

'''/////////////////////////////////////////////// Codigo para guardar el abstract de los 10 autores.'''

# Guardamos los autores y abstract
abstAut = {}

# with open('abstracts_Authors.txt', 'w', encoding="utf-8") as file_Text:
for article in listArticulos:
    formatReferencia = quest_name_refer(article)
    if 'abstract' in article:
        if formatReferencia:
            # Preguntamos si existe en el absAut
            articleExists = False

            # Trato de preguntar si el abstract ya fue llamado en cualquiera de los otros autores
            # para poder agregarlo y evitar repeticiones
            for autor in Top10Authors:
                if autor in article[formatReferencia]:
                    # print(f"{article['ID']} : {article['abstract']}")
                    if autor in abstAut:
                        abstAut[autor][1].update({article['ID']: article['abstract']})
                    else:
                        abstAut[autor] = [article['year'], {article['ID']: article['abstract']}]
                        # articleExists = True

        # file_Text.write("**** *")

# def printAbstract(key, abstract):

cont = 1
for key, content in abstAut.items():
    abstracts = content[1]
    # Guardamos por cada autor los abstract en un solo archivo de texto
    with open(f"FilesAbstracts/abstract_{key}_{cont}.txt", "a", encoding="utf-8") as fileTxt:
        # print("*" * 10, f"{key} : {len(abstracts)}", "*" * 10)
        for key2, abstract in abstracts.items():
            fileTxt.write(f"**** *ID_{key2}_{content[0]}_\n{abstract}\n")
    cont += 1

print(f"*********Reporte del Top de {Top} autores*********")
print("Autor | Conteo")
for autor, conteo in Top10Authors.items():
    print(f"{autor}: {conteo}")
