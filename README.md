# Curry-Company-Analytics

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/DanielTorresAndrade/Curry-Company-Analytics)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Python Version](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-000000?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=Kaggle&logoColor=white)](https://www.kaggle.com/datasets/gauravmalik26/food-delivery-dataset)
[![Versão do Projeto](https://img.shields.io/badge/Vers%C3%A3o-1.0-blue?style=for-the-badge)](https://github.com/DanielTorresAndrade/Curry-Company-Analytics)

Este projeto tem como objetivo analisar um conjunto de dados de entregas de comida online, com o intuito de extrair conhecimento e insights a partir desses dados. O projeto utilizará bibliotecas como Pandas, NumPy, Matplotlib e Plotly para realização de análises e visualizações de dados.

O objetivo do projeto é demonstrar como os dados podem ser utilizados para melhorar a eficiência e o desempenho dos negócios, identificando oportunidades de melhoria e otimização. Além disso, o projeto visa também proporcionar uma visão geral a respeito dos dados, permitindo que os usuários compreendam melhor como os dados podem ser utilizados para tomar decisões informadas.

Este projeto foi desenvolvido como parte do curso de Formação em Ciência de Dados da Comunidade DS, com o objetivo de demonstrar como a análise de dados pode ser utilizada para melhorar a eficiência e o desempenho dos negócios.

O dataset utilizado neste projeto está disponível no site do Kaggle, e pode ser acessado atraves do link abaixo:

[Food Delivery Dataset](https://www.kaggle.com/datasets/gauravmalik26/food-delivery-dataset/data)

## Objetivos do Projeto

- Analisar um conjunto de dados de entregas de comida online, com o intuito de extrair conhecimento e insights a partir desses dados.

- Utilizar bibliotecas como Pandas, NumPy, Matplotlib e Plotly para realização de análises e visualizações de dados.

- Demonstrar como os dados podem ser utilizados para melhorar a eficiência e o desempenho dos negócios, identificando oportunidades de melhoria e otimização.

- Uso do Framework Streamlit para desenvolvimento de dashboards interativos para serem utilizados pelos times de negócios da empresa.

## Bibliotecas Utilizadas

- pandas
- numpy
- matplotlib
- plotly
- streamlit

## Estrutura do Projeto

O projeto foi estruturado da seguinte maneira:

- `src`: Conteúdo do projeto, incluindo scripts, funções e classes.
- `data`: Arquivos de dados utilizados no projeto.
- `images`: Imagens utilizadas no projeto.
- `logs`: Logs gerados pelo projeto.
- `notebooks`: Notebooks utilizados para a criação do projeto.
- `pages`: Páginas do projeto que serão renderizadas pelo Streamlit.
- `.python-version`: Versão do Python utilizada no projeto.
- `pyproject.toml`: Arquivo de configuração do projeto.
- `Home.py`: Arquivo principal do projeto.
- `README.md`: Arquivo de documentação do projeto.
- `uv.lock`: Arquivo de lock do projeto.

Abaixo será apresentado a estrutura completa do projeto:

```bash
project_root
├── data
│   ├── processed
│   └── raw
│       └── train.csv
├── Home.py
├── images
│   └── logo.png
├── logs
│   └── app_logs.log
├── notebooks
│   └── analises.ipynb
├── pages
│   ├── __init__.py
│   ├── Visao_Empresarial.py
│   ├── Visao_Entregadores.py
│   └── Visao_Restaurantes.py
├── pyproject.toml
├── README.md
├── src
│   ├── analysis_tools.py
│   ├── data_cleaning.py
│   ├── __init__.py
│   ├── log_config.py
│   ├── __pycache__
│   │   ├── analysis_tools.cpython-313.pyc
│   │   ├── data_cleaning.cpython-313.pyc
│   │   ├── __init__.cpython-313.pyc
│   │   ├── log_config.cpython-313.pyc
│   │   └── sider.cpython-313.pyc
│   └── sider.py
└── uv.lock
```

## Como Baixar o Projeto

Para baixar o projeto do GitHub, basta clonar o repositorio utilizando o seguinte comando:

```bash
git clone https://github.com/Danieltandrade/Curry-Company-Analytics.git
```

## Como Executar o Projeto

### Opção 1: Usando UV (Recomendado)

Este projeto utiliza [uv](https://github.com/astral-sh/uv) para gerenciamento de dependências. Se você tiver o `uv` instalado:

```bash
uv sync
```

```bash
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
```

```bash
streamlit run Home.py
```

### Opção 2: Usando PIP (Padrão)

Para executar o projeto utilizando o PIP, basta instalar as dependências e executar o seguinte comando:

```bash
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

```bash
streamlit run Home.py
```

## Habilidades Desenvolvidas

Neste projeto pude desenvolver e aprimorar as seguintes habilidades:

- Manipulação de dados com Pandas e NumPy
- Visualização de dados com Matplotlib e Plotly
- Criação de dashboards interativos com Streamlit
- Utilização de bibliotecas de terceiros como Folium e Haversine

## License

Distributed under the [MIT License](https://choosealicense.com/licenses/mit/)

## Contato

- Email: danieltorresandrade@gmailcom
- GitHub: https://github.com/Danieltandrade

## Conclusão

Com este projeto consegui desenvolver minhas habilidades em análise de dados voltadas para questões de negócio da empresa focando em trazer insights que ajudem a melhorar o desempenho dos negócios. Também consegui aprimorar minhas habilidades em manipulação de dados e criação de dashboards interativos com Streamlit.

## Agradecimentos

Agradeço a [Comunidade DS](https://comunidadeds.com/) e ao [Kaggle](https://www.kaggle.com/datasets/gauravmalik26/food-delivery-dataset) por fornecer os dados utilizados neste projeto.
