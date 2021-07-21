# Consulta Localidade API IBGE

## Objetivo
  Consumir a API de localidade do IBGE.
  
## Preparação do ambiente
  ### Banco de dados
  <p> A aplicação utiliza um banco de dados em MS SQL Server. Antes de rodar a aplicação, criar o modelo de dados utilizando o script incluído no projeto "CreateDatabaseIBGELocalidade.sql". Não foi criado uma carga ou um backup porque a própria aplicação tem uma opção para consulta e carga do modelo relacional, na opção 3 do menu.
  O modelo é representado pelo diagrama abaixo.
</p>  
   <img src="https://github.com/israelss1-git/Consulta_localidade_API_IBGE/blob/master/Cortex/DiagramaDadosIBGELocalidade.png" width="600" title="Diagrama de Banco de Dados">
  
### Configuração de usuário
  
  Após a criação do banco de dados, configurar o usuário e senha no arquivo do arquivo "ConexaoDB.py" nas linhas 5 e 6

## Propostas
<p>
  Foram adotadas duas linhas de desenvolvimento. Uma com suporte a banco de dados e uma com controle de arquivo.
</p>

### Linha de desenvolvimento 1
<p> Por experiência anterior com a API, desici fazer uma opção em que, retornado o JSOM, as informações persistissem em um banco de dados relacional, com a mesma estrutura do documento. Para isso, foi criado o modelo mencionado acima e criado um script para popular o modelo.</p>
<p> Na opção 3 do menu principal "ATUALIZAR BANCO DE DADOS", o script deleta todas as informações do banco de dados para importar uma nova foto da estrutura de localidades. Faz uma requisição a API, retorna todas as localidades e percorre, inserindo na BD toda a hierarquia. Antes de inserir um novo distrito, que é a unidade mais baixa, ele verifica se ele já existe, existindo ele pula. Isso á para, se caso a conexão caia, na reconexão ele comece de onde parou.</p>
<p> Para manter integridade das constrains, ele vai inserindo as demais tabelas do nível mais alto (região) para o mais baixo (distrito), sempre verificando o nível já existe. Se existir ele pula, senão cadastra.</p>

#### Vantagens

* A consulta é muito mais rápida
* Não sofre com indisponibilidade do serviço
* Pode ser relacionado com outras bases de dados

#### Desvantagens

* Necessita de atualização para carregar mudanças
* Não é exatamente a proposta do exercício
* Necessita de suporte a banco de dados e configuração

### Linha de desenvolvimento 2
  
