# Consulta Localidade API IBGE

## Objetivo
  Consumir a API de localidade do IBGE.
  
## Preparação do ambiente
  ### Banco de dados
  <p> A aplicação utiliza um banco de dados em MS SQL Server. Antes de rodar a aplicação, criar o modelo de dados utilizando o script incluído no projeto "Cortex/Cortex/CreateDatabaseIBGELocalidade.sql". Não foi criado uma carga ou um backup porque a própria aplicação tem uma opção para consulta e carga do modelo relacional, na opção 3 do menu. Nesta mesma pasta há também consultas para testes da carga diretamente no banco de dados.
  O modelo é representado pelo diagrama abaixo.
</p>  
   <img src="https://github.com/israelss1-git/Consulta_localidade_API_IBGE/blob/master/Cortex/DiagramaDadosIBGELocalidade.png" width="600" title="Diagrama de Banco de Dados">
  
### Configuração de usuário
  
  Após a criação do banco de dados, configurar o usuário e senha no arquivo "ConexaoDB.py" nas linhas 5 e 6. Após as configurações, executar o script main.py para execução do menu de opções.

## Propostas
<p>
  Foram adotadas duas linhas de desenvolvimento. Uma com suporte a banco de dados e uma com controle de arquivo.
</p>

### Linha de desenvolvimento 1
<p> Por experiência anterior com a API, desidi fazer uma opção em que, retornado o JSOM, as informações persistissem em um banco de dados relacional, com a mesma estrutura do documento. Para isso, foi criado o modelo mencionado acima e criado um script para popular o modelo.</p>
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
<p> Na opção 1 do menu principal "CONSULTAR LOCALIDADE API", o script realiza uma consulta por nome do município diretamente na API do IBGE, sem passar pelo suporte ao banco de dados. Essa consulta foi idealizada por nome para ser parecida com a consulta na base de dados. Essa opção foi elaborada a fim de comparação com a consulta realizada no banco de dados que pode ser feita na opção 2 do menu principal "CONSULTAR LOCALIDADE BD".</p>

**Caso não seja possível suporte a banco de dados, as opções 2 e 3 não estarão disponíveis.**

### Linha de desenvolvimento 2
<p>A segunda linha de desenvolvimento foi pensada para atender mais precisamente ao que foi solicitado e para garantir o funcionamento caso não seja possível o suporte ao banco de dados comentado.</p>

    Exercício 1: Construa uma aplicação que irá consumir dados da API do IBGE. Deve ser possível realizar uma chamada através 
    de API REST contendo os parâmetros necessários como ...
    O serviço também deverá ser capaz de utilizar JOBS para execução de consultas através de CRON cadastradas anteriormente em 
    banco de dados, depositando os dados obtidos no em arquivos em formatos de sua preferência.

<p>Para este exercício, foi desenvolvido o script "ConsultaLocalidadesApi.py, que consome o mesmo serviço utilizado acima. Esta requisição necessita passar o ID do município para a consulta, o que não é muito prático, mas é o critério adotado. </p>
<p>Pode ser testado na opção 6 do menu principal "CONSULTA LOCALIDADE POR ID" </p>
<p>Pode ser testado no terminal, indo até a pasta dos onde estão os scripts, chamar o script seguido do id.</p>

    ConsultaLocalidadesApi.py 1100015
    
<p>O script de consulta recebe um parâmetro, consulta na API, imprime os resultados na tela ou retorna o request para a chamada da função.
  
    Exercício 2: ... Deve existir um esquema de filas para orquestração das chamadas à API do IBGE. Exemplo: A aplicação irá 
    receber um requisição REST ou ler na base as consultas que devem ser executadas de acordo com a CRON e disparar mensagens 
    para um consumidor da API do IBGE...
    
    Exercício 3: Implemente a arquitetura desenhada no exercício 2. Considere, caso a arquitetura fique muito complexa, implementar apenas uma 
    parte dela. Desejável ao menos a parte da fila.

#### Arquitetura do serviço
  
<p>Para os exercícios 2 e 3, foram desenvolvidos scripts para tratamento da fila através de arquivo. Foi elaborado o esquema abaixo para exemplificar o fluxo.</p>

<img src="https://github.com/israelss1-git/Consulta_localidade_API_IBGE/blob/master/Cortex/ArquiteturaServico.png" width="600" title="Diagrama de Banco de Dados">

1. Schedule chama o script agendado para a execução de consultas à API em lote.
2. O Script verifica se há arquivo com uma lista de execução para ser realizada. Se houver, carrega em uma lista. O arquivo deve conter id do município e nome do solicitante.
3. Percorre a lista consultando a api com o id do município.
4. Salva o resulta em um arquivo com o ID da consulta. Um arquivo para cada consulta.
5. Renomeia o arquivo com um prefixo com data e hora para guardar histórico. O arquivo não será mais chamado.
6. Escreve no arqvivo de log, detalhes da consulta realizada e do solicitante.

<p>Abaixo no esquema, tem um exemplos de outros modulos que podem ser agregados em scripts separados. Um exemplo é um script que, agendado de tempos em tempos, veifica o arquivo de log e envia e-mais, notificando os solicitantes.</p>

#### Implementação
<p>Para facilitar o teste, a opção 4 "CADASTRAR CONSULTA EM LOTE" do menu principal, possibiita cadastrar uma solicitação para ser processada no arquivo. O arquivo com a lista e os arquivos gerados ficam no C:, necessitando que o SO tenha esta unidade. O arquivo "fila_de_consulta.txt" pode ser escrito em outros editores e disponibiizados neste caminho para execução via terminal.</p>
<p>A opção 5 do menu principal "EXECUTAR FILA DE CONSULTAS" executa a consulta em lote das solicitações em arquivo e os disponibiliza com o resultado no diretório C. Essa opção chama o script FilaConsultasApi.py, que não necessita de argumentos. O script pode ser chamado pelo terminal e essa é a forma ideal para a chamada, uma vez que o propósito é agendar em uma CRON a chamada periódica deste serviço. Abaixo, um exemplo para a chamada do serviço</p>

    FilaConsultasApi.py

## Conclusão
O resultado deste trabalho é para demonstrar uma ideia de utilização do serviço. Pode ser melhorado, refatorado, incrementado com arquivos de configuração, log, classes, patterns e várias outras formas. Espero ter alcançado a ideia e cumprido o propósito do exercício.
