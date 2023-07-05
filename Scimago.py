# Conexión a la base de datos PostgreSQL
import psycopg2
import os,csv
host = 'localhost'
database = 'SCIMAGO'
user = 'postgres'
password = '050101'

#Rank	Sourceid	Title	Type	Issn	SJR	SJR Best Quartile	H index	Total Docs. (2022)	Total Docs. (3years)	Total Refs.	Total Cites (3years)	Citable Docs. (3years)	Cites / Doc. (2years)	Ref. / Doc.	Country	Region	Publisher	Coverage	Categories	Areas

journal_data = {
    'Rank': 1,
    'Sourceid': 28773,
    'Title': 'Ca-A Cancer Journal for Clinicians',
    'Type': 'journal',
    'Issn': '15424863, 00079235',
    'SJR': 86.091,
    'SJR_Best_Quartile': 'Q1',
    'H_index': 198,
    'Total_Docs_2022': 44,
    'Total_Docs_3years': 118,
    'Total_Refs': 4268,
    'Total_Cites_3years': 30318,
    'Citable_Docs_3years': 85,
    'Cites_Doc_2years': 299.99,
    'Ref_Doc': 97,
    'Country': 'United States',
    'Region': 'Northern America',
    'Publisher': 'Wiley-Blackwell',
    'Coverage': '1950-2022'
}
with open("scimagojr 2022.csv", encoding="utf8") as csv_file:
    # Crea un objeto reader similar a un diccionario delimitador por la barra |
    listFile = csv.DictReader(csv_file, delimiter=';')
    bigFile = []
    # Itero el objeto reader para añadirlo en una lista
    for row in listFile:
        bigFile.append(row)
print(bigFile)

print(journal_data)

# conn = psycopg2.connect(
#     host=host,
#     database=database,
#     user=user,
#     password=password
# )
# cursor = conn.cursor()
#
#
# cursor.execute("""
#     INSERT INTO JOURNAL (Rank, Sourceid, Title, Type, Issn, SJR, SJR_Best_Quartile, H_index,
#                          Total_Docs_2022, Total_Docs_3years, Total_Refs, Total_Cites_3years,
#                          Citable_Docs_3years, Cites_Doc_2years, Ref_Doc, Country, Region, Publisher,
#                          Coverage)
#     VALUES (%(Rank)s, %(Sourceid)s, %(Title)s, %(Type)s, %(Issn)s, %(SJR)s, %(SJR_Best_Quartile)s,
#             %(H_index)s, %(Total_Docs_2022)s, %(Total_Docs_3years)s, %(Total_Refs)s,
#             %(Total_Cites_3years)s, %(Citable_Docs_3years)s, %(Cites_Doc_2years)s, %(Ref_Doc)s,
#             %(Country)s, %(Region)s, %(Publisher)s, %(Coverage)s)
# """, journal_data)
#
# conn.commit()
#
#
# cursor.close()
# conn.close()