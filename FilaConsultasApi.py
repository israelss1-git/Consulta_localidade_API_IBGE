'''
Exercício 1 - B:
O serviço também deverá ser capaz de utilizar JOBS para execução de consultas através de CRON cadastradas anteriormente
em banco de dados, depositando os dados obtidos no em arquivos em formatos de sua preferência.
'''

import os
import ConsultaLocalidadesApi
import datetime

def executa_consulta_lote():
    # Verifica se tem arquivo de fila para consulta
    if os.path.isfile('C:\\fila_de_consulta.txt') is True:

        count_lista = 0
        f = open(r"C:\fila_de_consulta.txt", "r", encoding="windows-1252")
        for line in f:
            spl_line = line.split(';')
            id = int(spl_line[0])
            nome = spl_line[1]

            resp_api = ConsultaLocalidadesApi.cons_municipio_id(id)

            for js in resp_api:
                regiao = (js['microrregiao']['mesorregiao']['UF']['regiao']['nome'])
                estado = (js['microrregiao']['mesorregiao']['UF']['nome'])
                mesorregiao = (js['microrregiao']['mesorregiao']['nome'])
                microrregiao = (js['microrregiao']['nome'])
                cidade = (js['nome'])
                id = (js['id'])

                # ESCREVE O ARQUIVO COM AS INFORMAÇÕES RETORNADAS
                f = open(r"C:\Consulta_"+str(id)+'_'+nome.rstrip()+".txt", "a")
                f.write(f'Solicitante: {nome}'
                        f'ID: {id} \n'
                        f'Cidade: {cidade} \n'
                        f'Microrregião: {microrregiao} \n'
                        f'Mesorregiao: {mesorregiao} \n'
                        f'Estado: {estado} \n'
                        f'Região: {regiao}')
                f.close()

        f.close()

        t = datetime.datetime.now().strftime("%Y%m%d%H%M")

        path = r"C:\fila_de_consulta.txt"
        new_path = r"C:\fila_de_consulta_"+t+".txt"

        # RENOMEIA O ARQUIVO PARA GUARDAR HISTÓRICO E NÃO EFETUAR NOVAMENTE
        os.rename(path, new_path)

    else:
        print("Não há requisições aguardando na fila")

if __name__ == '__main__':
    executa_consulta_lote()