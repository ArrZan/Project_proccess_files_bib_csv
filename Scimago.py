# Conexión a la base de datos PostgreSQL
import psycopg2
import os
host = 'localhost'
database = 'SCIMAGO'
user = 'postgres'
password = '050101'

sql = "INSERT INTO  \"public\".\"SRHM\" (authors,articulo) values(\'" + par1.strip().strip(
                        ",") + " " + par2.strip().strip(",") + "\',\'" + articulo.strip(",") + "\');\n"
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

conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password
)
cursor = conn.cursor()


cursor.execute("""
    INSERT INTO JOURNAL (Rank, Sourceid, Title, Type, Issn, SJR, SJR_Best_Quartile, H_index,
                         Total_Docs_2022, Total_Docs_3years, Total_Refs, Total_Cites_3years,
                         Citable_Docs_3years, Cites_Doc_2years, Ref_Doc, Country, Region, Publisher,
                         Coverage)
    VALUES (%(Rank)s, %(Sourceid)s, %(Title)s, %(Type)s, %(Issn)s, %(SJR)s, %(SJR_Best_Quartile)s,
            %(H_index)s, %(Total_Docs_2022)s, %(Total_Docs_3years)s, %(Total_Refs)s,
            %(Total_Cites_3years)s, %(Citable_Docs_3years)s, %(Cites_Doc_2years)s, %(Ref_Doc)s,
            %(Country)s, %(Region)s, %(Publisher)s, %(Coverage)s)
""", journal_data)

conn.commit()


cursor.close()
conn.close()