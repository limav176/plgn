# Extrator de Curva DI x Pré - B3

Script Python para extração automatizada da curva de taxas **DI x Pré** da B3 (Bolsa de Valores brasileira).

## Sobre o Projeto

Este projeto é uma **Proof of Concept (PoC)** que realiza web scraping da página da B3 para extrair dados da curva de taxas de referência DI x Pré, retornando os dados estruturados em um DataFrame do pandas.

Resumo do projeto

## Objetivo
- Pipeline ETL para extrair taxas de referência (DI x Pré) da B3 e processá-las em camadas (Bronze → Silver → Gold).

## Arquivos 
** plgn.py
- Extrai dados da B3 via web scraping
- Função principal: extract_di_pre() retorna DataFrame com taxas
** dagAirflow.py
- DAG do Airflow que orquestra o pipeline
- 6 tasks: valida dia útil → extrai → valida → transforma → publica → atualiza controle
** test_plgn.py
- Testa a função extract_di_pre() isoladamente
** test_dag_simples.py
- Testa o pipeline completo sem Airflow (simula as tasks)
** test_dag.py
- Teste completo simulando contexto do Airflow

##  Funcionalidades

-  Extração automatizada da curva DI x Pré da B3
-  Suporte para qualquer data-base válida
-  Retorno em formato DataFrame (pandas)
-  Implementação simples e direta
-  Tratamento básico de erros HTTP

## Tecnologias Utilizadas

- **Python 3.9+**
- **requests** - Requisições HTTP
- **pandas** - Manipulação de dados
- **BeautifulSoup4** - Parsing de HTML

## Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone o repositório ou baixe os arquivos

2. Instale as dependências:

```bash
pip install requests pandas beautifulsoup4
```

Ou usando requirements.txt (se disponível):

```bash
pip install -r requirements.txt
```

## 💻 Como Usar

### Executar diretamente

```bash
python plgn.py
```

O script irá extrair os dados.


## Estrutura dos Dados

O DataFrame retornado contém as seguintes colunas:

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `curva` | string | Nome da curva (sempre "DI_PRE") |
| `data_base` | date | Data-base da extração |
| `vertice_dias` | int | Vértice em dias |
| `taxa` | float | Taxa de referência |

### Exemplo de Saída

```
   curva data_base  vertice_dias    taxa
0  DI_PRE 2024-01-15           1  13.25
1  DI_PRE 2024-01-15          21  13.30
2  DI_PRE 2024-01-15          42  13.35
...
```

## 🔍 Explicação do Código

### Bloco 1: Imports

### Bloco 2: URL da B3

### Bloco 3: Função Principal

- **Entrada**: Data-base 
- **Saída**: DataFrame com os dados extraídos

### Fluxo de Execução

1. **Preparação**: Formata a data no padrão brasileiro (dd/mm/yyyy)
2. **Requisição**: Faz GET na URL da B3 com os parâmetros
3. **Parsing**: Converte o HTML em objeto navegável (BeautifulSoup)
4. **Extração**: Localiza a tabela e extrai os dados linha por linha
5. **Transformação**: Converte os dados em DataFrame estruturado

##  Observações Importantes

-  Requer **conexão com internet** (faz requisição HTTP)

##  Licença

Este projeto é uma PoC. Desenvolvido como parte de entrega em candidatura a vaga de engenheiro de dados.

## Autor
limav176



