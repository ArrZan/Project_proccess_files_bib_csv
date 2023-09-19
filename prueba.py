# Ordenar una lista de coches almacenados como diccionarios
# diccionarios_coches = [
#     {'colores': 'Rojo', 'matricula': '4859-A', 'cambio': 'A'},
#     {'color': 'Azul', 'matricula': '2901-Z', 'cambio': 'M'},
#     {'color': 'Gris', 'matricula': '1892-B', 'cambio': 'M'}
# ]
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



title = "the Firm of, (1997)"
title2 = "Carl M., (2000) Agency Theory of last, CEO, california"

# title = re.sub(r'[^\w\s]', '', title)
# title2 = re.sub(r'[^\w\s]', '', title2)

print(fuzz.token_set_ratio(title.lower(), title2.lower()))

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

ref = 'INT BLACK SEA CONF.'

refMatch = re.search(r'(DOI)\s(.+)', ref)

print(refMatch)