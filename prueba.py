# Ordenar una lista de coches almacenados como diccionarios
# diccionarios_coches = [
#     {'colores': 'Rojo', 'matricula': '4859-A', 'cambio': 'A'},
#     {'color': 'Azul', 'matricula': '2901-Z', 'cambio': 'M'},
#     {'color': 'Gris', 'matricula': '1892-B', 'cambio': 'M'}
# ]
import unidecode as ud

d_ord = {'uno': 1, 'dos': 5, 'tres': 30, 'cuatro': 3230, 'cinco': 530, 'seis': 450, 'siete': 35, 'ocho': 50}
d_mess = {'ocho': 50, 'dos': 5, 'cincos': 530, 'seis': 450, 'tres': 30, 'cuatro': 3230, 'uno': 1, 'siete': 35}


def sortDict(dictionary_ordered, dictionary_messy):
    orderedData = {}
    # Pregunto si tienen las mismas claves
    if set(dictionary_ordered.keys()) != set(dictionary_messy.keys()):
        return False

    for key in dictionary_ordered:
        orderedData[key] = dictionary_messy[key]
    return orderedData


print(sortDict(d_ord, d_mess))

sorted_d = sorted(d_ord.values(), reverse=True)
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
