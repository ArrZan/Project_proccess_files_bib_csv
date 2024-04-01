import csv
import os
from libs import libMerged as lm
import bibtexparser

vacias = 0
kwvacia = 0
kwpvacia = 0
akwvacia = 0

kw = 'keywords'
kwp = 'keywords-plus'
kwa = 'author_keywords'

tempKeys = {}  # Diccionario de los keywords por cada iteración del entry
listaKeys = {}  # Lista de los keywords sin repetir y contadas
listKw = {}  # Lista de keywords
listKwp = {}  # Lista de keywords plus
listKwa = {}  # Lista de author keywords
contTitle = 1  # Contador para poner al lado del titulo


def addQuartile(journal, issn, eissn):
    with open("scimagojr 2022.csv", encoding="utf8") as csv_file:
        # Crea un objeto reader similar a un diccionario delimitado por la barra |
        scimagoFile = csv.DictReader(csv_file, delimiter=';')

        for row in scimagoFile:
            if issn and issn.replace("-", "") in row["Issn"]:
                return row["SJR Best Quartile"]

            if eissn and eissn.replace("-", "") == row["Issn"]:
                return row["SJR Best Quartile"]

            if journal and journal.upper() == row["Title"].upper():
                return row["SJR Best Quartile"]

        return "Undefined"


def format_bibtex_entry(entry):
    global vacias, kwvacia, kwpvacia, akwvacia, listaKeys, listKw, listKwp, listKwa, contTitle

    # field, format, wrap or not
    field_order = [(u'author', '{{{0}}},\n', True),
                   (u'title', '{{{0}}},\n', True),
                   (u'journal', '{{{0}}},\n', True),
                   (u'volume', '{{{0}}},\n', True),
                   (u'number', '{{{0}}},\n', True),
                   (u'pages', '{{{0}}},\n', True),
                   (u'year', '{{{0}}},\n', True),
                   (u'doi', '{{{0}}},\n', False)]
    keys = set(entry.keys())
    extra_fields = keys.difference([f[0] for f in field_order])

    # we do not want these in our entry
    extra_fields.remove('ENTRYTYPE')
    extra_fields.remove('ID')

    # Now build our input string and add the code sorted by year
    # ENTRYTYPE
    s = '@{type}{{{id},\ncode={{{code}}},\n\n'.format(type=entry['ENTRYTYPE'],
                                                      id=entry['ID'], code=contTitle)

    for field, fmt, wrap in field_order:
        if field in entry:
            # This commented code was to add a counter to the title, as we already put it in code, I comment this.
            if field == 'title':
                s += lm.union(field, '{0} {1}'.format(contTitle, entry[field]))
            else:
                s1 = '{0}='.format(field)
                s2 = fmt.format(entry[field])
                s3 = '{0}{1}'.format(s1, s2)
                s += s3 + '\n'

    eissn = entry["eissn"] if "eissn" in entry else None
    issn = entry["issn"] if "issn" in entry else None
    journal = entry["journal"] if "journal" in entry else None

    # We add a new field for quartiles :p
    s += lm.union('Quartil', addQuartile(journal=journal, issn=issn, eissn=eissn))

    keyword = 0
    keywords_plus = 0
    author_keywords = 0

    for field in extra_fields:
        if field in entry:

            if field == kw:
                keyword = 1
                tempKeys[field] = entry[field]
                listaKeys = lm.keyDel(entry[field], listaKeys)
                listKw = lm.keyDel(entry[field], listKw)
            elif field == kwp:
                keywords_plus = 1
                tempKeys[field] = entry[field]
                listaKeys = lm.keyDel(entry[field], listaKeys)
                listKwp = lm.keyDel(entry[field], listKwp)
            elif field == kwa:
                author_keywords = 1
                tempKeys[field] = entry[field]
                listaKeys = lm.keyDel(entry[field], listaKeys)
                listKwa = lm.keyDel(entry[field], listKwa)

            if field != kw and field != kwp and field != kwa:
                s += lm.union(field, entry[field])

    if (keyword + keywords_plus + author_keywords) == 0:
        vacias += 1

        s += lm.union(kw, " ")  # Keywords
        s += lm.union(kwp, " ")  # keywords-plus
        s += lm.union(kwa, " ")  # author_keywords

    elif keyword == 0 and keywords_plus == 0 and author_keywords == 1:
        s += lm.union(kw, " ")
        s += lm.union(kwp, tempKeys[kwa])
        s += lm.union(kwa, " ")

    elif keyword == 0 and keywords_plus == 1 and author_keywords == 0:
        s += lm.union(kw, " ")
        s += lm.union(kwp, entry[kwp])
        s += lm.union(kwa, " ")

    elif keyword == 0 and keywords_plus == 1 and author_keywords == 1:
        s += lm.union(kw, " ")
        s += lm.union(kwp, tempKeys[kwp] + " ; " + tempKeys[kwa])
        s += lm.union(kwa, entry[kwa])

    elif keyword == 1 and keywords_plus == 0 and author_keywords == 0:
        s += lm.union(kw, " ")
        s += lm.union(kwp, tempKeys[kw])
        s += lm.union(kwa, " ")

    elif keyword == 1 and keywords_plus == 0 and author_keywords == 1:
        s += lm.union(kw, entry[kw])
        s += lm.union(kwp, tempKeys[kw] + " ; " + tempKeys[kwa])
        s += lm.union(kwa, entry[kwa])

    elif keyword == 1 and keywords_plus == 1 and author_keywords == 0:
        s += lm.union(kw, entry[kw])
        s += lm.union(kwp, tempKeys[kwp] + " ; " + tempKeys[kw])
        s += lm.union(kwa, " ")

    elif keyword == 1 and keywords_plus == 1 and author_keywords == 1:
        s += lm.union(kw, entry[kw])
        s += lm.union(kwp, tempKeys[kw] + " ; " + tempKeys[kwp] + " ; " + tempKeys[kwa])
        s += lm.union(kwa, entry[kwa])

    if keyword == 0:
        kwvacia += 1  # Contador de keywords vacíos
    if keywords_plus == 0:
        kwpvacia += 1  # Contador de keywords-plus vacíos
    if author_keywords == 0:
        akwvacia += 1  # Contador de author_keywords vacíos

    s += '\n}\n\n'
    contTitle += 1
    return s


if os.path.exists('merged.bib'):
    os.unlink('merged.bib')

"""# /////////////////////////////////////////////// Este codigo une los archivos"""
# pathSource = 'input Files/'   # Ruta de donde se guardan los archivos en bruto para recogerlos y procesarlos
# pathDestination = 'Output Files/'  # Ruta donde se guardan los datos procesados del path por ejecución de un proyecto
# pathProject = 'History Projects/'  # Ruta donde se guardan todos los proyectos
# pathUnidos = pathDestination + 'unidos.bib'  # La ruta y nombre del archivo que unirá todos los archivos del path
# fileNames = os.listdir(pathSource)  # Saco una lista de los archivos que haya en el path
#
# # Se pregunta si existe el directorio de salida de los archivos, si no, se creará
# try:
#     if not os.path.isdir(pathDestination):
#         os.mkdir(pathDestination)
#     else:
#
#         # filesNamesOut = os.listdir(pathDestination)
#         # filesExists = len(filesNamesOut) != 0
#         if filesExists:
#             for name in filesNamesOut:
#                 shutil.move(pathSource, pathProject)
#
#         # Se crea el nuevo archivo
#         with open(pathUnidos, "w", encoding='utf-8') as new_file:
#             # Se itera los nombres de los archivos en el path
#             for name in fileNames:
#                 rootFile = pathSource + name
#                 with open(rootFile, encoding='utf-8') as file:
#                     for line in file:
#                         new_file.write(line)
#
#                     new_file.write("\n")
#
# except FileNotFoundError as msgErr:
#     print('No existe el directorio: ', msgErr)


"""# /////////////////////////////////////////////// Este codigo es para quitar duplicados entre dos archivos y fusionarlos
"""
# with open('scopus.bib', encoding="utf8") as bibtex_file:
#     bib_database = bibtexparser.load(bibtex_file)
#     entries1 = bib_database.get_entry_list()
# print('SCOPUS: {0} entries in file 1'.format(len(entries1)))
#
# with open('wos.bib', encoding="utf8") as bibtex_file:
#     bib_database = bibtexparser.load(bibtex_file)
#     entries2 = bib_database.get_entry_list()
# print('WOS: {0} entries in file 1'.format(len(entries2)))
#
# # Now, let see how many duplicates there are. It is easy to use sets for this.
# entry1_keys = set([entry['title'] for entry in entries1])
# entry2_keys = set([entry['title'] for entry in entries2])
#
# duplicates = entry1_keys & entry2_keys
# print('There are {0} duplicates'.format(len(duplicates)))
# print(duplicates)
#
# for entry in entries1:
#     with open('merged.bib', 'a', encoding="utf8") as f:
#         f.write(format_bibtex_entry(entry))
#
# # store keys to check for duplicates
# entry1_keys = [entry['title'] for entry in entries1]
#
# for entry in entries2:
#     if not entry['title'] in entry1_keys:
#         with open('merged.bib', 'a', encoding="utf8") as f:
#             try:
#                 f.write(format_bibtex_entry(entry))
#             except:
#                 print("An exception occurred")
#
# print("vacias : ", vacias)
# print("kwvacia : ", kwvacia)
# print("kwpvacia: ", kwpvacia)
# print("Akwvacia: ", akwvacia)
#
# with open('merged.bib', encoding="utf8") as bibtex_file:
#     bib_database = bibtexparser.load(bibtex_file)
#     entries2 = bib_database.get_entry_list()
# print('MERGED: {0} entries in file 1'.format(len(entries2)))

"""# /////////////////////////////////////////////// Este codigo es para quitar duplicados de un solo archivo"""
with open('unidos.bib', encoding="utf-8") as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)
    

    """ COMPROBACIÓN DE NÚMERO DE ARTÍCULOS """ 
    # entries_prub = bib_database.entries
    # print("Entries: ")
    # for entri in entries_prub:
    #     print(entri)
    # print(" "*100)
    # print(" "*100)

    # print("Cantidad de entries: {}".format(len(entries_prub)))

    
    """ COMPROBACIÓN DE UNA CANTIDA DE ARTÍCULOS PARA VER SU ESTRUCTURA """ 
    entries1 = bib_database.get_entry_list()
    # print('Artículos: {0} entries in file'.format(len(entries1)))






# for i, entry in enumerate(entries1):
   
#     print(f"Entry {i + 1}: {entry}")

# Se setea los títulos del archivo, quitando los repetidos
titleEnt = list(set([entry['title'].upper() for entry in entries1]))
print('Duplicados: {0} in file 1'.format(len(entries1) - len(titleEnt)))

# Cantidad de titulos seteados
print("Cantidad de titulos seteados: ", len(titleEnt))

# Ordenamos los artículos por año de menor a mayor
OrderEntrys = sorted(entries1, key=lambda artic: int(artic['year']))

# Se va iterando el archivo original
for entry in OrderEntrys:
    # Preguntamos por el titulo de la iteración si está en los titulos seteados, si está, se lo agrega al archivo merged
    if entry['title'].upper() in titleEnt:
        with open('merged.bib', 'a', encoding="utf8") as f:
            f.write(format_bibtex_entry(entry))

        # y se lo quita de los titulos seteados
        titleEnt.remove(entry['title'].upper())

# Se vuelve a abrir el archivo para contar los archivos que quedaron
with open('merged.bib', encoding="utf8") as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)
    merged = bib_database.get_entry_list()
print('MERGED: {0} entries in file 1'.format(len(merged)))

"""" /////////////////////////////////////////////// Aquí reunimos y guardamos todas las palabras claves"""
with open("keywordsAllList.csv", "w", encoding='utf-8') as keywordsAll:
    keywordsAll.write("keywords;count;" + chr(13))
    for keywords in listaKeys:
        keywordsAll.write(keywords + ";" + str(listaKeys[keywords]) + ";" + chr(13))

#  Aquí reunimos todas las palabras claves de keywords únicamente
with open("keywordsList.csv", "w", encoding='utf-8') as listKeywords:
    listKeywords.write("keywords;count;" + chr(13))
    for keywords in listKw:
        listKeywords.write(keywords + ";" + str(listKw[keywords]) + ";" + chr(13))

#  Aquí reunimos todas las palabras claves de keywords-plus únicamente
with open("keywordsPlusList.csv", "w", encoding='utf-8') as listKeywordsPlus:
    listKeywordsPlus.write("keywords;count;" + chr(13))
    for keywords in listKwp:
        listKeywordsPlus.write(keywords + ";" + str(listKwp[keywords]) + ";" + chr(13))

#  Aquí reunimos todas las palabras claves de author_keywords únicamente
with open("keywordsAuthorList.csv", "w", encoding='utf-8') as listKeywordsAuthor:
    listKeywordsAuthor.write("keywords;count;" + chr(13))
    for keywords in listKwa:
        listKeywordsAuthor.write(keywords + ";" + str(listKwa[keywords]) + ";" + chr(13))

print('Quantity of all types of keywords: {0}'.format(len(listaKeys)))
print('Quantity of keywords: {0}'.format(len(listKw)))
print('Quantity of keywords-plus: {0}'.format(len(listKwp)))
print('Quantity of author-keywords: {0}'.format(len(listKwa)))
