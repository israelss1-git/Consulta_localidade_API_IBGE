'''
Exercício 1 - A:
Construa uma aplicação que irá consumir dados da API do IBGE.
Deve ser possível realizar uma chamada através de API REST contendo os parâmetros necessários como exemplo abaixo:

id: 1600303

- Consula API do IBGE, retornando dados de uma cidade, passando o parâmetro id para busca.
- Imprime o resultado no console para utilização através de linha de comando
- Retorna o JSOM da requisição para uma chamada externa

'''
import requests
import sys
import os

# Realiza uma chamada ao serviço do IBGE e retona um json
def requisicao_api(url):
    resposta = requests.get(url)
    if resposta.status_code == 200:
        print('API disponível.')
        return resposta.json()
    else:
        return resposta.status_code

'''
    Consulta se um determinado registro já está cadastrado na tabela.
    Retorna um True para existente e false para não
'''
def cons_municipio_id (id):

    url = f'https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{id}'

    resp_api = [requisicao_api(url)]

    for js in resp_api:
        regiao = (js['microrregiao']['mesorregiao']['UF']['regiao']['nome'])
        estado = (js['microrregiao']['mesorregiao']['UF']['nome'])
        mesorregiao = (js['microrregiao']['mesorregiao']['nome'])
        microrregiao = (js['microrregiao']['nome'])
        cidade = (js['nome'])
        id = (js['id'])

        # IMPRIME NO TERMINAL PARA CONSULTAS FEITAS PELO SO
        print(f'\nID: {id} \n'
              f'Cidade: {cidade} \n'
              f'Microrregião: {microrregiao} \n'
              f'Mesorregiao: {mesorregiao} \n'
              f'Estado: {estado} \n'
              f'Região: {regiao}')

    return resp_api

if __name__ == '__main__':
    cons_municipio_id(sys.argv[1])

