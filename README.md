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

#### Consultas
<p> Na opção 1 do menu principal "CONSULTAR LOCALIDADE API", o script realiza uma consulta por nome diretamente na API do IBGE, se passar pelo ssuporte ao banco de dados. Essa consulta foi idealizada por nome para ser parecida com a consulta na base de dados. Esse opção foi elaborada a fim de comparação com a consulta realizada no banco de dados que pode ser feita na opção 2 do menu principa "CONSULTAR LOCALIDADE BD".</p>

**Caso não seja possível suporte a banco de dados, as opções 2 e 3 nãoestarão disponíveis.**

### Linha de desenvolvimento 2
<p>A segunda linha de desenvolvimento foi pensada para atender mais precisamente ao que foi solicitado e para garantir o funcionamento caso não seja possível o suporte ao banco de dados cometado.</p>

    Exercício 1 : Construa uma aplicação que irá consumir dados da API do IBGE. Deve ser possível realizar uma chamada através 
    de API REST contendo os parâmetros necessários como ...
    O serviço também deverá ser capaz de utilizar JOBS para execução de consultas através de CRON cadastradas anteriormente em 
    banco de dados, depositando os dados obtidos no em arquivos em formatos de sua preferência.

<p>Para este exercício, foi desenvolvido o script "ConsultaLocalidadesApi.py, que consome o mesmo serviço utilizado acima. Esta requisição necessita passar o ID do município para a consulta, o que não é muito prático, mas é o critério adotado. </p>
<p>Pode ser testado na opção 6 do menu principal "CONSULTA LOCALIDADE POR ID" </p>
<p>Pode ser testado no terminal, indo até a pasta dos onde estão os scripts, chamar o script seguido do id.</p>

    Exemplo: "ConsultaLocalidadesApi.py 1100015"
    
<p>O script de consulta recebe um parâmetro, consulta na API, imprime os resultados na tela ou retorna o request para a chamada da função.
  
    Exercício 2 ... Deve existir um esquema de filas para orquestração das chamadas à API do IBGE. Exemplo: A aplicação irá 
    receber um requisição REST ou ler na base as consultas que devem ser executadas de acordo com a CRON e disparar mensagens 
    para um consumidor da API do IBGE...
    
    Implemente a arquitetura desenhada no exercício 2. Considere, caso a arquitetura fique muito complexa, implementar apenas uma 
    parte dela. Desejável ao menos a parte da fila.

<p>Para os exercícios 2 e 3, foram desenvolvidos scripts para tratamento da fila através de arquivo.</p>
