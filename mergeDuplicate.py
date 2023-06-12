import os

from libs import deleteKeyDuplicated
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


def union(key, entrykey):
    s1 = '{0}='.format(key)
    s3 = '{0}{{{1}}},'.format(s1, entrykey)
    return s3 + '\n'


def format_bibtex_entry(entry):
    global vacias, kwvacia, kwpvacia, akwvacia, listaKeys, listKw, listKwp, listKwa
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

    # Now build up our entry string
    # ENTRYTYPE
    s = '@{type}{{{id},\n'.format(type=entry['ENTRYTYPE'],
                                  id=entry['ID'])
    for field, fmt, wrap in field_order:
        if field in entry:
            s1 = '{0}='.format(field)
            s2 = fmt.format(entry[field])
            s3 = '{0}{1}'.format(s1, s2)
            s += s3 + '\n'

    keyword = 0
    keywords_plus = 0
    author_keywords = 0

    for field in extra_fields:
        if field in entry:

            if field == kw:
                keyword = 1
                tempKeys[field] = entry[field]
                listaKeys = deleteKeyDuplicated.keyDel(entry[field], listaKeys)
                listKw = deleteKeyDuplicated.keyDel(entry[field], listKw)
            elif field == kwp:
                keywords_plus = 1
                tempKeys[field] = entry[field]
                listaKeys = deleteKeyDuplicated.keyDel(entry[field], listaKeys)
                listKwp = deleteKeyDuplicated.keyDel(entry[field], listKwp)
            elif field == kwa:
                author_keywords = 1
                tempKeys[field] = entry[field]
                listaKeys = deleteKeyDuplicated.keyDel(entry[field], listaKeys)
                listKwa = deleteKeyDuplicated.keyDel(entry[field], listKwa)

            if field != kw and field != kwp and field != kwa:
                s += union(field, entry[field])

    if (keyword + keywords_plus + author_keywords) == 0:
        vacias += 1

        s += union(kw, " ")  # Keywords
        s += union(kwp, " ")  # keywords-plus
        s += union(kwa, " ")  # author_keywords

    elif keyword == 0 and keywords_plus == 0 and author_keywords == 1:
        s += union(kw, " ")
        s += union(kwp, tempKeys[kwa])
        s += union(kwa, " ")

    elif keyword == 0 and keywords_plus == 1 and author_keywords == 0:
        s += union(kw, " ")
        s += union(kwp, entry[kwp])
        s += union(kwa, " ")

    elif keyword == 0 and keywords_plus == 1 and author_keywords == 1:
        s += union(kw, " ")
        s += union(kwp, tempKeys[kwp] + " ; " + tempKeys[kwa])
        s += union(kwa, entry[kwa])

    elif keyword == 1 and keywords_plus == 0 and author_keywords == 0:
        s += union(kw, " ")
        s += union(kwp, tempKeys[kw])
        s += union(kwa, " ")

    elif keyword == 1 and keywords_plus == 0 and author_keywords == 1:
        s += union(kw, entry[kw])
        s += union(kwp, tempKeys[kw] + " ; " + tempKeys[kwa])
        s += union(kwa, entry[kwa])

    elif keyword == 1 and keywords_plus == 1 and author_keywords == 0:
        s += union(kw, entry[kw])
        s += union(kwp, tempKeys[kwp] + " ; " + tempKeys[kw])
        s += union(kwa, " ")

    elif keyword == 1 and keywords_plus == 1 and author_keywords == 1:
        s += union(kw, entry[kw])
        s += union(kwp, tempKeys[kw] + " ; " + tempKeys[kwp] + " ; " + tempKeys[kwa])
        s += union(kwa, entry[kwa])

    if keyword == 0:
        kwvacia += 1  # Contador de keywords vacíos
    if keywords_plus == 0:
        kwpvacia += 1  # Contador de keywords-plus vacíos
    if author_keywords == 0:
        akwvacia += 1  # Contador de author_keywords vacíos

    s += '\n}\n\n'
    return s


if os.path.exists('merged.bib'):
    os.unlink('merged.bib')

with open('scopus.bib', encoding="utf8") as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)
    entries1 = bib_database.get_entry_list()
print('SCOPUS: {0} entries in file 1'.format(len(entries1)))

with open('wos.bib', encoding="utf8") as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)
    entries2 = bib_database.get_entry_list()
print('WOS: {0} entries in file 1'.format(len(entries2)))

# Now, let see how many duplicates there are. It is easy to use sets for this.
entry1_keys = set([entry['title'] for entry in entries1])
entry2_keys = set([entry['title'] for entry in entries2])

duplicates = entry1_keys & entry2_keys
print('There are {0} duplicates'.format(len(duplicates)))


for entry in entries1:
    with open('merged.bib', 'a', encoding="utf8") as f:
        f.write(format_bibtex_entry(entry))

# store keys to check for duplicates
entry1_keys = [entry['title'] for entry in entries1]

for entry in entries2:
    if not entry['title'] in entry1_keys:
        with open('merged.bib', 'a', encoding="utf8") as f:
            try:
                f.write(format_bibtex_entry(entry))
            except:
                print("An exception occurred")

print("vacias : ", vacias)
print("kwvacia : ", kwvacia)
print("kwpvacia: ", kwpvacia)
print("Akwvacia: ", akwvacia)

for entry in entries1:
    with open('merged.bib', 'a', encoding="utf8") as f:
        f.write(format_bibtex_entry(entry))


with open('merged.bib', encoding="utf8") as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)
    entries2 = bib_database.get_entry_list()
print('MERGED: {0} entries in file 1'.format(len(entries2)))


#  Aquí reunimos todas las palabras claves
keywordsAll = open("keywordsAllList.csv", "w")
keywordsAll.write("keywords;count;" + chr(13))
for keywords in listaKeys:
    keywordsAll.write(keywords + ";" + str(listaKeys[keywords]) + ";" + chr(13))
keywordsAll.close()

#  Aquí reunimos todas las palabras claves de keywords únicamente
listKeywords = open("keywordsList.csv", "w")
listKeywords.write("keywords;count;" + chr(13))
for keywords in listKw:
    listKeywords.write(keywords + ";" + str(listKw[keywords]) + ";" + chr(13))
listKeywords.close()

#  Aquí reunimos todas las palabras claves de keywords-plus únicamente
listKeywordsPlus = open("keywordsPlusList.csv", "w")
listKeywordsPlus.write("keywords;count;" + chr(13))
for keywords in listKwp:
    listKeywordsPlus.write(keywords + ";" + str(listKwp[keywords]) + ";" + chr(13))
listKeywordsPlus.close()

#  Aquí reunimos todas las palabras claves de author_keywords únicamente
listKeywordsAuthor = open("keywordsAuthorList.csv", "w")
listKeywordsAuthor.write("keywords;count;" + chr(13))
for keywords in listKwa:
    listKeywordsAuthor.write(keywords + ";" + str(listKwa[keywords]) + ";" + chr(13))
listKeywordsAuthor.close()


# with open('unido1.bib', encoding="utf8") as bibtex_file:
#     bib_database = bibtexparser.load(bibtex_file)
#     entries1 = bib_database.get_entry_list()
# print('Artículos: {0} entries in file'.format(len(entries1)))
#
# cont=1
# for entry in entries1:
#
#     # check if the count of sweet is > 1 (repeating item)
#     if entries1.count(entry['title']) > 1:
#         # if True, remove the first occurrence of sweet
#         entries1.remove(entry)
#         print(cont, ",", entry['title'])
#         cont += 1
#
# # print(entries1)
#
#
# entry1_keys = set([entry['title'] for entry in entries1])
# print('Hay {0} archivos que se pueden extraer'.format((len(entries1)-len(entry1_keys))))
