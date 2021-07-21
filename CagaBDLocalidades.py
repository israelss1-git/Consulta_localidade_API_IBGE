import pyodbc
import requests

'''
Objetivo: consulta de API de localidade do IBGE para verificação de localidades nível distrito.

Estratégia
    A API do IBGE apresenta instabilidade em algumas ocasiões. Para garantir a informação com
o crescimento da demanda, julguei interessante realizar uma consuta e carga em banco de dados,
em um esquema relacional, reproduzindo a hierarquia da estrutura reportada no JSON.
    Uma vez ao mês ou por demanda, o job agendado fará uma nova fotografia da estrutura atual, 
afim de refletir as novas alterações. Ele deletará todos os dados e irá carregar novamente. 


'''
# Conexão com o DB.
def conexaoDB():
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-DPP33GN;'
                          'Database=BD_SQL_GAMMA_IBGE;'
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
def consulta_tabela(tabela, id):
    conn = conexaoDB()

    cons = conn.execute(f"SELECT id FROM {tabela} WHERE ID = ?", id)
    s = [True for x in cons if x[0] == id]
    resp = False
    if len(s) == 1:
        resp = True

    conn.close()

    return resp


'''
    Verifica se o registro existe e seão existir, carrega na tabela
'''
def consulta_carrega(tabela, id, nome, sigla='', fk=0, fk2=0):
    conn = conexaoDB()

    cons = consulta_tabela(tabela, id)
    if cons != True:
        if tabela == 'REGIAO':
            conn.execute(f"INSERT INTO {tabela} VALUES (?,?,?)", id, sigla, nome)
        elif tabela == 'UF':
            conn.execute(f"INSERT INTO {tabela} VALUES (?,?,?,?)", id, sigla, nome, fk)
        elif tabela == 'MUNICIPIO':
            conn.execute(f"INSERT INTO {tabela} VALUES (?,?,?,?)", id, nome, fk, fk2)
        else:
            conn.execute(f"INSERT INTO {tabela} VALUES (?,?,?)", id, nome, fk)
        conn.commit()


'''
    Deleta todos os dados do schema para receber uma nova foto da estrutura
de localidades do IBGE.

'''
def prepara_carga():
    print('Preparando BD para nova carga.')
    conn = conexaoDB()
    tabelas = ['DISTRITO', 'MUNICIPIO', 'REGIAO_IMEDIATA', 'REGIAO_INTERMEDIARIA', 'MICRORREGIAO', 'MESORREGIAO', 'UF',
               'REGIAO']

    for tab in tabelas:
        conn.execute(f"DELETE FROM {tab}")
        conn.commit()

    conn.close()


'''
    Realiza uma consulta ao serviço e recebe um json para ser iterado
    Durante a iteração, verifica se o distrito já está cadastrado na tabela. Se não estive
    percorre toda a hierarquia, verificando e cadastrando as dependências até cadatrar o 
    distrito.
'''
def carrega_db_localidades():

    prepara_carga()

    resposta = requisicao_api()
    print('Carregando DB.')

    for js in resposta:
        id_dist = (js['id'])
        ex = consulta_tabela('DISTRITO', id_dist)

        if ex != True:
            # REGIAO
            id = (js['municipio']['microrregiao']['mesorregiao']['UF']['regiao']['id'])
            sigla = (js['municipio']['microrregiao']['mesorregiao']['UF']['regiao']['sigla'])
            nome = (js['municipio']['microrregiao']['mesorregiao']['UF']['regiao']['nome'])
            consulta_carrega('REGIAO', id, nome, sigla)

            # UF
            id = (js['municipio']['microrregiao']['mesorregiao']['UF']['id'])
            sigla = (js['municipio']['microrregiao']['mesorregiao']['UF']['sigla'])
            nome = (js['municipio']['microrregiao']['mesorregiao']['UF']['nome'])
            fk = (js['municipio']['microrregiao']['mesorregiao']['UF']['regiao']['id'])
            consulta_carrega('UF', id, nome, sigla, fk)

            # Mesorregiao
            id = (js['municipio']['microrregiao']['mesorregiao']['id'])
            nome = (js['municipio']['microrregiao']['mesorregiao']['nome'])
            fk = (js['municipio']['microrregiao']['mesorregiao']['UF']['id'])
            sigla = ''
            consulta_carrega('MESORREGIAO', id, nome, sigla, fk)

            # Região intermediária - Está no mesmo nível que mesorregião
            id = (js['municipio']['regiao-imediata']['regiao-intermediaria']['id'])
            nome = (js['municipio']['regiao-imediata']['regiao-intermediaria']['nome'])
            fk = (js['municipio']['regiao-imediata']['regiao-intermediaria']['UF']['id'])
            sigla = ''
            consulta_carrega('REGIAO_INTERMEDIARIA', id, nome, sigla, fk)

            # Microrregiao
            id = (js['municipio']['microrregiao']['id'])
            nome = (js['municipio']['microrregiao']['nome'])
            fk = (js['municipio']['microrregiao']['mesorregiao']['id'])
            sigla = ''
            consulta_carrega('MICRORREGIAO', id, nome, sigla, fk)

            # Região imediata - Está no mesmo nível de microrregião
            id = (js['municipio']['regiao-imediata']['id'])
            nome = (js['municipio']['regiao-imediata']['nome'])
            fk = (js['municipio']['regiao-imediata']['regiao-intermediaria']['id'])
            sigla = ''
            consulta_carrega('REGIAO_IMEDIATA', id, nome, sigla, fk)

            # Cidade: cidades são a mesma coisa que municípios.
            id = (js['municipio']['id'])
            nome = (js['municipio']['nome'])
            fk = (js['municipio']['microrregiao']['id'])
            fk2 = (js['municipio']['regiao-imediata']['id'])
            sigla = ''
            consulta_carrega('MUNICIPIO', id, nome, sigla, fk, fk2)

            # Distrito: uma subdivisão de cidade. um conjunto de distritos definemuma região metropolitana dentro de um municipio
            id = (js['id'])
            nome = (js['nome'])
            fk = (js['municipio']['id'])
            sigla = ''
            consulta_carrega('DISTRITO', id, nome, sigla, fk)

    print('Carga concluída.')

if __name__ == '__main__':
    carrega_db_localidades()