import bibtexparser

entradas = {}


def addEntry(diccionario):
    # print(diccionario)
    for xentry in diccionario:
        # print(xentry)
        if xentry in entradas:
            entradas[xentry] = entradas[xentry] + 1
        else:
            entradas[xentry] = 1


with open('merged.bib', encoding="utf8") as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)
#     cont = 0
# print("|" * 100)
# for fuente in bib_database.entries:
#     if fuente['keywords'] == fuente['author_keywords']:
#         print(fuente['keywords'], "\n", fuente['author_keywords'])
#     elif fuente['keywords'] == fuente['keywords-plus']:
#         print(fuente['keywords'], "\n", fuente['keywords-plus'])
#     elif fuente['author_keywords'] == fuente['keywords-plus']:
#         print(fuente['author_keywords'], "\n", fuente['keywords-plus'])
#         cont += 1
    # print("**" * 5, "   "*5, fuente['title'], "   "*5, "**" * 5, "\n")
    # for field in fuente:
    #     if field == 'keywords':
    #         print(field, " : ", fuente[field])
    #     if field == 'keywords-plus':
    #         print(field, " : ", fuente[field])
    #     if field == 'author_keywords':
    #         print(field, " : ", fuente[field])
    #         cont += 1
# print(cont)


with open('merged.bib', encoding="utf8") as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

for fuente in bib_database.entries:
    addEntry(list(fuente.keys()))
arcEntry = open("entryList.csv", "w")
arcEntry.write("entry;count;" + chr(13))
for entryF in entradas:
    arcEntry.write(entryF + ";" + str(entradas[entryF]) + ";" + chr(13))
    ##print(entryF,"->",entradas[entryF])
arcEntry.close()
