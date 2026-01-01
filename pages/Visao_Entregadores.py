"""
Projeto para construção de um Dashboard interativo utilizando Python e Streamlit.

Autor: Daniel Torres de Andrade
Data: 28 de Dezembro de 2025
Descrição: Este script inicializa o aplicativo Streamlit e exibe uma mensagem de boas-vindas.

"""

# Importando Bibliotecas
import logging
import streamlit as st
import os
import sys
from pathlib import Path

# Adiciona a raiz do projeto ao sys.path para garantir que o python encontre o 'src'
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(project_root)

# --- IMPORTS DO SEU PROJETO ---
from src.analysis_tools import filtros, avaliacao_media_desvio_padrao, top_entregadores
from src.data_cleaning import df_cleaning
from src.sider import sidebar
from src.log_config import setup_logging

# Inicializa o logger
setup_logging()
logger = logging.getLogger(__name__)

def main():
    # Define a raiz do projeto dinamicamente
    ROOT_DIR = Path(__file__).parent.parent
    DATA_PATH = ROOT_DIR / 'data' / 'raw' / 'train.csv'

    # Carregando e limpando os dados
    df = df_cleaning(str(DATA_PATH), df_clean=True)

    if df is None:
        st.error("Erro ao carregar os dados. Verifique os logs para mais detalhes.")
        return

    # Configurando a página do Streamlit
    st.set_page_config(page_title="Marketplace - Curry Company", page_icon='🚚', layout="wide")
    st.title("Marketplace - Visão Entregadores")

    logger.info("Usuário acessou a pagina Visão Entregadores.")

    # Criando a barra lateral
    image_path = 'images/logo.png'
    date_slider, traffic_options, weather_cond, cities = sidebar(image_path)

    # Aplicando os filtros no dataframe
    df = filtros(df, date_slider, traffic_options, weather_cond, cities)

    st.markdown("""---""")

    with st.container():
        st.title("Métricas Gerais", text_alignment='center')

        col1, col2, col3, col4 = st.columns(4, gap='large', border=True, width='stretch')

        with col1:

            maior_idade = df.loc[:, 'Delivery_person_Age'].max()
            col1.metric("Maior Idade", maior_idade)
        with col2:

            menor_idade = df.loc[:, 'Delivery_person_Age'].min()
            col2.metric("Menor Idade", menor_idade)
        with col3:

            melhor_cond_veic = df.loc[:, 'Vehicle_condition'].max()
            col3.metric("Melhor Condição de Veículo", melhor_cond_veic)
        with col4:

            pior_cond_veic = df.loc[:, 'Vehicle_condition'].min()
            col4.metric("Pior Condição de Veículo", pior_cond_veic)

    st.markdown("""---""")

    with st.container():
        st.title("Avaliações", text_alignment='center')

        col1, col2 = st.columns(2, gap='medium', border=True)

        with col1:
            st.markdown("### Avaliação Média por Entregador", text_alignment='center')

            df_avg_rat_del = (
                df.loc[:, ['Delivery_person_Ratings', 'Delivery_person_ID']]
                .groupby('Delivery_person_ID')
                .mean()
                .reset_index()
            )

            st.dataframe(df_avg_rat_del)

        with col2:
            st.markdown("### Avaliação Média por Transito", text_alignment='center')

            # Agrupamento por transito
            df_avg_std_rating_by_traf = avaliacao_media_desvio_padrao(df, 'Road_traffic_density')
            st.dataframe(df_avg_std_rating_by_traf)

            st.markdown("### Avaliação Média por Clima", text_alignment='center')

            # Agrupamento por clima
            df_avg_std_rating_by_wet = avaliacao_media_desvio_padrao(df, 'Weatherconditions')
            st.dataframe(df_avg_std_rating_by_wet)

    st.markdown("""---""")

    with st.container():
        st.title("Velocidade de Entrega", text_alignment='center')
        
        col1, col2 = st.columns(2, gap='medium', border=True)

        with col1:
            st.markdown("#### Top Entregadores mais Rápidos")
            # ascending=True -> Menor tempo (Mais rápido)
            df_fastest = top_entregadores(df, ascending_order=True)
            st.dataframe(df_fastest)

        with col2:
            st.markdown("#### Top Entregadores mais Lentos")
            # ascending=False -> Maior tempo (Mais lento)
            df_slowest = top_entregadores(df, ascending_order=False)
            st.dataframe(df_slowest)

    st.markdown("""---""")

if __name__ == "__main__":
    main()
