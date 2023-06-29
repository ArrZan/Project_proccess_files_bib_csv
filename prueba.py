# Ordenar una lista de coches almacenados como diccionarios
diccionarios_coches = [
    {'colores': 'Rojo', 'matricula': '4859-A', 'cambio': 'A'},
    {'color': 'Azul', 'matricula': '2901-Z', 'cambio': 'M'},
    {'color': 'Gris', 'matricula': '1892-B', 'cambio': 'M'}
]

for i in diccionarios_coches:
    dicciNew = {k.upper(): v for k, v in i.items()}
    print('cOlorEs' in dicciNew)
    print(dicciNew)


# golasd