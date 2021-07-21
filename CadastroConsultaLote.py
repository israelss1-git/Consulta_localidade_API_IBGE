'''
Cadastra uma fila de consultas na api, para reaclização de consultas em lote.
O script escreve um arquivo em C:\fila_de_consulta.txt onde será buscado a sequencia das
consultas.

'''
import datetime

def cadastro_consulta():
    id_cidade = input("ID da cidade pesquisada: ")
    nome_solic = input("Nome do solicitante: ")
    email_solic = input("E-mail do solicitante: ")

    dth_solicitacao = datetime.datetime.now().strftime("%d/%m/%Y %H%M%S")

    reg = id_cidade+';'+nome_solic+';'+email_solic+';'+dth_solicitacao+'\n'

    print(reg)

    f = open(r"C:\fila_de_consulta.txt", "a")
    f.write(reg)
    f.close()

if __name__ == '__main__':
    cadastro_consulta()