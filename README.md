# Consulta Localidade API IBGE

## Objetivo
  Consumir a API do IBGE de localidade.
  
## Preparação do ambiente
  ### Banco de dados
  <p> A aplicação utiliza um banco de dados em MS SQL Server. Antes de rodar a aplicação, criar o modelo de dados utilizando o script incluído no projeto "CreateDatabaseIBGELocalidade.sql". Não foi criado uma carga ou um backup porque a própria aplicação tem uma opção para consulta e carga do modelo relacional, na opção 3 do menu.
  O modelo é representaro pelo diagrama abaixo.</p>
  ![Screenshot](https://github.com/israelss1-git/Consulta_localidade_API_IBGE/blob/master/Cortex/DiagramaDadosIBGELocalidade.png)
  ![alt text]()
 
  
  
  Para facilitar a demonstração, foi criado um menu com algumas opções para execução dos scripts.
  para rodar a aplicação inicial, deve ser chamado o script main.py.
