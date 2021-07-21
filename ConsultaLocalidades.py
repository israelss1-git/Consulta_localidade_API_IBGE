import pyodbc
import requests
import os

'''
Consulta as localidades, no banco de dados ou na api, através do nome.
'''

# Conexão com o DB.
def conexaoDB():
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-DPP33GN;'
                          'Database=BD_IBGE_LOCALIDADE2;'
                          'UID=sa;'
                          'PWD=sa;')

    return conn.cursor()


# Realiza uma chamada ao serviço do IBGE e retona um json
def requisicao_api():
    resposta = requests.get('https://servicodados.ibge.gov.br/api/v1/localidades/distritos')
    if resposta.status_code == 200:
        print('API disponível.')
        return resposta.json()
    else:
        return resposta.status_code


'''
    Consulta se um determinado registro já está cadastrado na tabela.
    Retorna um True para existente e false para não
'''
def consulta_localidade_cidade_api(cidade):

    resp_api = requisicao_api()
    rownum = 0
    for js in resp_api:
        nome = (js['municipio']['nome'])
        if nome == cidade:
            rownum += 1
            regiao = (js['municipio']['microrregiao']['mesorregiao']['UF']['regiao']['nome'])
            estado = (js['municipio']['microrregiao']['mesorregiao']['UF']['nome'])
            mesorregiao = (js['municipio']['microrregiao']['mesorregiao']['nome'])
            microrregiao = (js['municipio']['microrregiao']['nome'])
            cidade = (js['municipio']['nome'])
            distrito = (js['nome'])

            print(f'{rownum} Regiao: {regiao} - Estado: {estado} - Mesorregiao: {mesorregiao} - Microrregião: {microrregiao} - Cidade: {cidade} - Distrito: {distrito}')


def consulta_localidade_cidade_bd(cidade):

    conn = conexaoDB()

    cons = conn.execute(f"SELECT DISTINCT "
                        f"	DIST.ID_CIDADE AS ID, "
                        f"	DIST.NOME AS DISTRITO, "
                        f"	MUN.NOME AS CIDADE, "
                        f"	MICRO.NOME AS MICRORREGIAO, "
                        f"	MESO.NOME AS MESORREGIAO, "
                        f"	UF.NOME AS ESTADO, "
                        f"	REG.NOME AS REGIAO "           
                        f"FROM REGIAO REG "
                        f"INNER JOIN UF ON REG.ID = UF.ID_REGIAO "
                        f"INNER JOIN MESORREGIAO MESO ON UF.ID = MESO.ID_UF "
                        f"INNER JOIN MICRORREGIAO MICRO ON MESO.ID = MICRO.ID_MESORREGIAO "
                        f"INNER JOIN MUNICIPIO AS MUN ON MICRO.ID = MUN.ID_MICRORREGIAO "
                        f"INNER JOIN DISTRITO AS DIST ON MUN.ID = DIST.ID_CIDADE "
                        f"WHERE MUN.NOME = '{cidade}' "
                        f"ORDER BY REG.NOME, UF.NOME, MESO.NOME, MICRO.NOME, DIST.NOME DESC")
    for rs in cons:
        print(rs)

    conn.close()

if __name__ == '__main__':
    consulta_localidade_cidade_api('Mangaratiba')