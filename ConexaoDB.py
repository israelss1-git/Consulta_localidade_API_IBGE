import pyodbc

# Conexão com o DB.
def conexaoDB():
    usuario = 'sa'
    senha = 'sa'

    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-DPP33GN;'
                          'Database=BD_IBGE_LOCALIDADE2;'
                          f'UID={usuario};' 
                          f'PWD={senha};')

    return conn.cursor()