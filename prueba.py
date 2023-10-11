# Ordenar una lista de coches almacenados como diccionarios
# diccionarios_coches = [
#     {'colores': 'Rojo', 'matricula': '4859-A', 'cambio': 'A'},
#     {'color': 'Azul', 'matricula': '2901-Z', 'cambio': 'M'},
#     {'color': 'Gris', 'matricula': '1892-B', 'cambio': 'M'}
# ]
import csv

import unidecode as ud
import os

# d_ord = {'uno': 1, 'dos': 5, 'tres': 30, 'cuatro': 3230, 'cinco': 530, 'seis': 450, 'siete': 35, 'ocho': 50}
# d_mess = {'ocho': 50, 'dos': 5, 'cincos': 530, 'seis': 450, 'tres': 30, 'cuatro': 3230, 'uno': 1, 'siete': 35}
#
# from convert_CSV_x_BIB import generateRoute
#
# generateRoute("History Projects")

# def sortDict(dictionary_ordered, dictionary_messy):
#     orderedData = {}
#     # Pregunto si tienen las mismas claves
#     if set(dictionary_ordered.keys()) != set(dictionary_messy.keys()):
#         return False
#
#     for key in dictionary_ordered:
#         orderedData[key] = dictionary_messy[key]
#     return orderedData
#
#
# print(sortDict(d_ord, d_mess))
#
# sorted_d = sorted(d_ord.values(), reverse=True)

"""Intento tomar todos los entries de un bib y no solo articles"""
# import bibtexparser
#
# with open('prueba2.bib', encoding="utf-8") as bibtex_file:
#     bib_database = bibtexparser.load(bibtex_filePrueb)
#     entries1 = bib_database.get_entry_list()
# print('Artículos: {0} entries in file'.format(len(entries1)))

#
# d.update({'uno': 3})
# print(d)
#
# texto = "ID_Mirić201863_1982_"
# print(texto)
# print(ud.unidecode(texto))


# tos = [(key,value) for key, value in TopAuthors.items() if value >= 700]

# print(sorted_d)
#
# for key, value in d.items():
#     print()

# for i in diccionarios_coches:
#     dicciNew = {k.upper(): v for k, v in i.items()}
#     print('cOlorEs' in dicciNew)
#     print(dicciNew)


""" PORCENTAJE DE SIMILITUD """

# # Cargar el modelo de lenguaje de spaCy
# nlp = spacy.load("en_core_web_sm")
#
# # Lista de oraciones
# sentences = [
#     "Carl M., (2000) Agency Theory of Last, CEO, California",
#     "Carl M., (2000) Agency Theory of Last, CEO, America",
#     "Carl M., (2000) Agency Theory of Last, CEO, Journal",
#     "Famm S., Crish S., (1997) The Firm of"
# ]
#
# # Procesar las oraciones y convertirlas en vectores de términos de palabras
# sentence_vectors = [nlp(sentence).vector for sentence in sentences]
#
# # Calcular el porcentaje de similitud entre todas las combinaciones de oraciones
# similarities = []
# for pair in combinations(sentence_vectors, 2):
#     similarity = cosine_similarity([pair[0]], [pair[1]])[0][0]
#     similarities.append(similarity)
#
# # Calcular el porcentaje promedio de similitud
# average_similarity = sum(similarities) / len(similarities)
#
# print(f"Porcentaje de similitud promedio entre oraciones: {average_similarity * 100:.2f}%")

import re
from thefuzz import fuzz

# Lista de referencias
# references = [
#     "Venkatraman, N., Strategic orientation of business enterprises: The construct, dimensionality, and measurement (1989) Management science, 35, pp. 942-962",
#     "Venkatraman, N., strategic orientation of business enterprises: the construct, dimensionality, and measurement (1989) Management Science",
#     "Venkatraman, N., Strategic Orientation Of Business Enterprises: The Construct, Dimensionality, And Measurement (1989) Management Science",
#     "Venkatraman, N., (1989) Strategic orientation of business enterprises The construct dimensionality and measurement, , Management Science, 35, pp. 942-962",
#     "Venkatraman, N., (1989) Strategic orientation of business enterprises: The construct, dimensionality, 'and measurement'"
# ]
references = [
    "Carl M., (2000) Agency Theory of last, CEO, california",
    "Carl M., (2000) Agency Theory of Last, CEO, , america",
    "Carl M., (2000) agency theory of last, Ceo, journal",
    "Carl M., agency theory of last, Ceo (2000)",
    "Famm S., Crish S., (1997) the firm of",
    "Famm S., Crish S., the firm of (1997)",
    "Famm S., Crish S., (1997) the Firm of, calif",
    "Famm S., Crish S., (1997) The Firm Of, cali",
    "Bar C, the firm of (2000)"
]

title1 = "A behavioral theory of labor negotiation"
title2 = "A Behavioral Theory of Labor Relations"

# title = re.sub(r'[^\w\s]', '', title)
# title2 = re.sub(r'[^\w\s]', '', title2)
#
# print(fuzz.ratio(title1, title2))
# print(fuzz.partial_ratio(title1, title2))
# print(fuzz.token_set_ratio(title1, title2))
# print(fuzz.token_sort_ratio(title1, title2), "v")
# print(fuzz.partial_token_sort_ratio(title1, title2), "v")

""" Se escoge 94 como porcentaje para comparación de títulos """

# # Función para encontrar títulos similares
# def find_similar_titles(references):
#     similar_titles = {}
#
#     for reference in references:
#
#         # Tomar la segunda parte como el título
#         title = reference
#
#         # Comprobar si ya existe un título similar
#         for existing_title, score in similar_titles.items():
#             similarity_score = fuzz.ratio(title.lower(), existing_title.lower())
#             if similarity_score > score:
#                 similar_titles[existing_title] = similarity_score
#                 break
#         else:
#             similar_titles[title] = 0
#
#     return similar_titles
#
# similar_titles = find_similar_titles(references)
#
# # Imprime los títulos similares
# for title, similarity_score in similar_titles.items():
#     print(f"Título: {title} (Puntaje de similitud: {similarity_score}%)")


import re

vacio = "Vacio"

""" Proceso para la tercera opción del titulo"""
# ref = "Himmelberg, C. P., Petersen, B. C., R & D and Internal Finance: A Panel Study of Small Firms in High-Tech Industries (1994) The Review of Economics and Statistics, 76 (1), pp. 38-51"

# refMatch = re.search(r"(([a-zA-ZÀ-ÿ-']+),\s(([A-Z].?\s?)+)), (.)+\(([1-2]\d{3})\)", ref)
#
# # Buscamos los autores de la línea con el siguiente regex
# authors = re.findall(r"(([a-zA-ZÀ-ÿ-']+),\s(([A-Z].?\s?)+)),", ref)
#
# posLastAut = authors[-1][0]
# posTitle = refMatch.group().find(posLastAut) + len(posLastAut) + 1  # Sumamos 1 por la coma final de autores
# title = refMatch.group()[posTitle:-6]  # Restamos 6 por el len del year

"""Como estamos en prueba, debemos ver cuales valores no lee para adentrarlo en el patron"""

# # ref = "(1991) Measuring and controlling large credit exposures, , January 1991"
#
# refMatch = re.search(r"(([-\w'? ]+),\s(([A-Z-]\.?\s?)+)),", ref)
#
# # Extraemos el año siempre que sea mayor a 1000 o menor 2999
# yearExiste = re.search(r'\(([1-2]\d{3})\)', ref)
#
# # Si es None, pondrá vacio, si no tomará el año
# yearRef = vacio if yearExiste is None else yearExiste.group(1)
#
#
# authors = re.findall(r"(([a-zA-ZÀ-ÿ-']+),\s(([A-Z].?\s?)+)),", ref)
#
# posLastAut = 0
#
# for author in authors:
#     posLastAut = posLastAut + len(author[0]) + 2
#
# posYear = yearExiste.regs[0][1]
#
# # Si el año está al comienzo... year, author, title
# if yearExiste.regs[0][0] == 0:
#     posComa = ref.find(",")
#     title = ref[posYear + 1:posComa]  # Sumamos 1 por la coma o espacio
# # Si el año está en la mitad... author, year, title
# elif "," in ref[posYear-9:posYear]:
#     if re.search(r',\s\d+\s\(\d+\)', ref) is not None:
#         posVolNum = re.search(r',\s\d+\s\(\d+\)', ref).group()
#         posEnd = ref[posYear:].find(posVolNum)
#     elif ", pp" in ref:
#         posEnd = ref[posYear:].find(", pp")
#     elif ", ," in ref:
#         posEnd = ref[posYear:].find(", ,")
#     else:
#         posEnd = ref[posYear:].find(",")
#
#     title = ref[posYear:posEnd+posYear]
# else:
#     title = ref[posLastAut:posYear-6]  # Restamos por el len de year
#
# print(title)
# print(authors)
# print(yearRef)
# print(ref)

""

# index = {}
# f_author = "amilton M"
# authors = "amilton M"
# f_lett = authors[0]
# year = "1974"
# index[f_lett] = {f_author: {year: {authors: []}}}
# print(index)

#
# """ Vamos a comparar los datos del csv con el bib y guardar el tipo de Quartil que tiene """
# with open("scimagojr 2022.csv", encoding="utf8") as csv_file:
#     # Crea un objeto reader similar a un diccionario delimitado por la barra |
#     listFile = csv.DictReader(csv_file, delimiter=';')
#
#     for row in listFile:
#         print(row["Title"].upper())


a = 1
b = 2
c = {a: {5: 5}, b: {1: 2}}
c[a] |= c[b]
print(c)
