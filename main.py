'''
Case Cortex
Os exercícios são baseados em parametrizações que serão solicitadas na hora da apresentação.

Dica: Quanto menos hardcoded, melhor :)

Observações:
Você pode utilizar um banco de dados relacional ou não relacional como PostgreSQL, Oracle, MYSQL, H2, HSQLDB, MongoDB,
dentro outros, arquivos em disco, estrutura em memória ou qualquer outro serviço relacionado desejado.

Ao enviar o código final, deve estar claro como rodar os projetos feitos e quais serviços precisam ser
configurados/acessados.

Preferencialmente, recomendamos uso de NodeJS, Python ou Java mas você pode utilizar qualquer linguagem
e/ou tecnologia que queira.

Se você disponibilizar os serviços em algum lugar para rodarmos diretamente, como um Heroku, você ganha pontos extras.

Caso não consiga terminar algum exercício, sinalize no readme a dificuldade encontrada e/ou o que você faria diferente
se tivesse mais tempo.

Exercícios
Exercício 1 - A: ConsultaLocalidadesApi.py

Exercício 1 - B: FilaConsultaApi.py

Exercício 2:
Faça um esquema de uma arquitetura utilizando o serviço feito no Exercício 1. A arquitetura deve atender os requisitos
abaixo:

Deve existir um esquema de filas para orquestração das chamadas à API do IBGE. Exemplo: A aplicação irá receber um
requisição REST ou ler na base as consultas que devem ser executadas de acordo com a CRON e disparar mensagens para um
consumidor da API do IBGE.

O resultado desse exercício deve ser um diagrama, um esquema. Você pode complementar com um texto, explicando como os
itens da arquitetura se comunicam e como pensou para fazer o desenho da mesma.

Você pode também utilizar várias filas em diferentes lugares. Outras coisas não descritas na arquitetura também podem
ser incluídas, como banco de dados (diversos), sistemas de logs, métricas, etc. É obrigatório ter ao menos uma fila.

Exercício 3:
Implemente a arquitetura desenhada no exercício 2. Considere, caso a arquitetura fique muito complexa, implementar
apenas uma parte dela. Desejável ao menos a parte da fila.


'''

import CagaBDLocalidades
import ConsultaLocalidades
import CadastroConsultaLote
import FilaConsultasApi

def option_from_user():
    print('\n' + '-- CONSULTA LOCALIDADE API IBGE --'.center(80) + '\n'
            '1 - CONSULTAR LOCALIDADE API\n'
            '2 - CONSULTAR LOCALIDADE BD\n'
            '3 - ATUALIZAR BANCO DE DADOS\n'
            '4 - CADASTRAR CONSULTA EM LOTE\n'
            '5 - EXECUTAR FILA DE CONSULTAS\n'
            "6 - FECHAR PROGRAMA\n")

    option = 0
    while option < 1 or option > 6:
        try:
            option = int(input("DIGITE A OPÇÃO DESEJADA: "))
        except ValueError:
            print("ENTRADA INVÁLIDA!".center(80))
            option = 0
            continue
        if option < 1 or option > 6:
            print("OPÇÃO INVÁLIDA. DIGITE UMA OPÇÃO VÁLIDA DE ACORDO COM O MENU ACIMA!".center(80))

    return option


if __name__ == '__main__':

    option = 0

    while option >= 0 and option <= 6:

        if option == 0:  # Voltar ao menu principal
            option = option_from_user()

        if option == 1:  #
            localidade = input('Entre com o Cidade: ')
            ConsultaLocalidades.consulta_localidade_cidade_api(localidade)
            option = 0

        if option == 2:  #
            localidade = input('Entre com a Cidade: ')
            ConsultaLocalidades.consulta_localidade_cidade_bd(localidade)
            option = 0

        if option == 3:  #
            print('NOVA CARGA NO BANCO DE DADOS - AGUARDE')
            CagaBDLocalidades.carrega_db_localidades()
            option = 0

        if option == 4:  #
            CadastroConsultaLote.cadastro_consulta()
            print('NOVA CARGA NO BANCO DE DADOS - AGUARDE')
            option = 0

        if option == 5:  #
            FilaConsultasApi.executa_consulta_lote()
            print('NOVA CARGA NO BANCO DE DADOS - AGUARDE')
            option = 0

        if option == 6:  #
            print("PROGRAMA FINALIZADO!".center(80))
            break