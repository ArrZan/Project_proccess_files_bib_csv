class Project:
    def __init__(self, ):
        self.abstracts = {}
        self.bibFile = {}
        # self.merged = {}
        self.
        # REVISAR ATRIBUTOS DE CLASE E INSTANCIA

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

