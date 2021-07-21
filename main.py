'''
Código de orquestração da solução. Apresenta um Menu para acesso as funcionalidades
do script.

'''

import CagaBDLocalidades
import ConsultaLocalidades
import ConsultaLocalidadesApi
import CadastroConsultaLote
import FilaConsultasApi

def option_from_user():
    print('\n' + '-- CONSULTA LOCALIDADE API IBGE --'.center(80) + '\n'
            '1 - CONSULTAR LOCALIDADE API\n'
            '2 - CONSULTAR LOCALIDADE BD\n'
            '3 - ATUALIZAR BANCO DE DADOS\n'
            '4 - CADASTRAR CONSULTA EM LOTE\n'
            '5 - EXECUTAR FILA DE CONSULTAS\n'
            '6 - CONSULTA LOCALIDADE POR ID\n'
            "7 - FECHAR PROGRAMA\n")

    option = 0
    while option < 1 or option > 7:
        try:
            option = int(input("DIGITE A OPÇÃO DESEJADA: "))
        except ValueError:
            print("ENTRADA INVÁLIDA!".center(80))
            option = 0
            continue
        if option < 1 or option > 7:
            print("OPÇÃO INVÁLIDA. DIGITE UMA OPÇÃO VÁLIDA DE ACORDO COM O MENU ACIMA!".center(80))

    return option


if __name__ == '__main__':

    option = 0

    while option >= 0 and option <= 7:

        if option == 0:  # Voltar ao menu principal
            option = option_from_user()

        if option == 1:  # CONSULTAR LOCALIDADE API
            localidade = input('Entre com o Cidade: ')
            ConsultaLocalidades.consulta_localidade_cidade_api(localidade)
            option = 0

        if option == 2:  # CONSULTAR LOCALIDADE BD
            localidade = input('Entre com a Cidade: ')
            ConsultaLocalidades.consulta_localidade_cidade_bd(localidade)
            option = 0

        if option == 3:  # ATUALIZAR BANCO DE DADOS
            print('NOVA CARGA NO BANCO DE DADOS - AGUARDE')
            CagaBDLocalidades.carrega_db_localidades()
            option = 0

        if option == 4:  # CADASTRAR CONSULTA EM LOTE
            CadastroConsultaLote.cadastro_consulta()
            print('NOVA CARGA NO BANCO DE DADOS - AGUARDE')
            option = 0

        if option == 5:  # EXECUTAR FILA DE CONSULTAS
            FilaConsultasApi.executa_consulta_lote()
            option = 0

        if option == 6:  # CONSULTA LOCALIDADE POR ID
            ident = input("Entre com o ID do município: ")
            ConsultaLocalidadesApi.cons_municipio_id(ident)
            option = 0

        if option == 7:  # FECHAR PROGRAMA
            print("PROGRAMA FINALIZADO!".center(80))
            break