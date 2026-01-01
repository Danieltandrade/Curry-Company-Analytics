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
import numpy as np
from haversine import haversine as hs
from pathlib import Path
from plotly import express as px

# Adiciona a raiz do projeto ao sys.path para garantir que o python encontre o 'src'
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(project_root)

# Importando módulos do projeto
from src.analysis_tools import filtros, festival_mean_std, mean_std_tempo_cidade
from src.analysis_tools import mean_std_dataframe, tempo_medio_ent_cidade
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
    st.set_page_config(page_title="Marketplace - Curry Company", page_icon='🍔', layout="wide")
    st.title("Marketplace - Visão Restaurantes")

    logger.info("Usuário acessou a pagina Visão Restaurantes.")

    # Criando a barra lateral
    image_path = 'images/logo.png'
    date_slider, traffic_options, weather_cond, cities = sidebar(image_path)

    # Aplicando os filtros no dataframe
    df = filtros(df, date_slider, traffic_options, weather_cond, cities)

    st.markdown("""---""")

    with st.container():
        st.markdown("## Métricas Gerais", text_alignment='center')

        col1, col2, col3, col4, col5, col6 = st.columns(6, border=True)

        with col1:
            ent_unicos = df.loc[:, 'Delivery_person_ID'].nunique()
            col1.metric("#### Entregadores \nÚnicos", ent_unicos)

        with col2:
            cols = [
                'Delivery_location_latitude', 
                'Delivery_location_longitude',
                'Restaurant_latitude', 
                'Restaurant_longitude'
            ]

            # Realizando o cálculo da distância entre restaurante e local de entrega com apply
            df['Distance'] = df.loc[:, cols].apply(
                lambda x: hs((x[cols[0]], x[cols[1]]), 
                (x[cols[2]], x[cols[3]])), 
                axis=1
            )
            media_dist = df.loc[:, 'Distance'].mean()
            col2.metric("#### Distância \nMédia (km)", f"{media_dist:.2f}")

        with col3:

            cols = ['Time_taken(min)', 'Festival']
            avg_festival = festival_mean_std(df, cols, 'Yes', 'Avg_time')
            st.metric("#### Tempo Médio \nFestival (min)", f"{avg_festival.values[0]:.1f}")

        with col4:

            std_festival = festival_mean_std(df, cols, 'Yes', 'Std_time')
            st.metric("#### Desvio Padrão \nFestival (min)", f"{std_festival.values[0]:.1f}")

        with col5:

            avg_no_festival = festival_mean_std(df, cols, 'No', 'Avg_time')
            st.metric("#### Tempo Médio \nFestival (min)", f"{avg_no_festival.values[0]:.1f}")

        with col6:

            std_no_festival = festival_mean_std(df, cols, 'No', 'Std_time')
            st.metric("#### Desvio Padrão \nFestival (min)", f"{std_no_festival.values[0]:.1f}")

    st.markdown("""---""")

    with st.container():
        st.markdown("## Entregas no tempo", text_alignment='center')

        col1, col2 = st.columns(2, border=True)

        with col1:

            st.markdown("### Média e desvio padrão do tempo por cidade", text_alignment='center')

            fig = mean_std_tempo_cidade(df)
            col1.plotly_chart(fig, width='stretch')

        with col2:
            st.markdown("### Distribuição de distância", text_alignment='center')

            df_aux = mean_std_dataframe(
                df, 
                cols=['Time_taken(min)', 'City', 'Type_of_order'], 
                cols_groupby=['City', 'Type_of_order']
            )
            st.dataframe(df_aux, width='stretch')

    st.markdown("""---""")

    with st.container():
        st.markdown("## Distribuição no tempo", text_alignment='center')

        col1, col2 = st.columns(2, border=True)

        with col1:
            st.markdown("### Tempo médio de entrega por cidade", text_alignment='center')

            fig = tempo_medio_ent_cidade(df)
            st.plotly_chart(fig, width='stretch')

        with col2:
            st.markdown(
                "### Tempo médio de entrega por cidade e tipo de tráfego", 
                text_alignment='center'
            )

            df_aux = mean_std_dataframe(
                df, 
                cols=['Time_taken(min)', 'City', 'Road_traffic_density'], 
                cols_groupby=['City', 'Road_traffic_density']
            )

            fig2 = px.sunburst(
                df_aux,
                path=['City', 'Road_traffic_density'],
                values='Avg_time',
                color='Std_time',
                color_continuous_scale='RdBu',
                color_continuous_midpoint=np.average(df_aux['Std_time'])
            )
            st.plotly_chart(fig2, width='stretch')

if __name__ == "__main__":
    main()
