"""
Projeto para construção de um Dashboard interativo utilizando Python e Streamlit.

Autor: Daniel Torres de Andrade
Data: 28 de Dezembro de 2025
Descrição: Este script inicializa o aplicativo Streamlit e exibe uma mensagem de boas-vindas.

"""

# Importando Bibliotecas
import folium
import pandas as pd
import streamlit as st
from dataframe import dataframe
from config import sidebar
from plotly import express as px
from streamlit_folium import st_folium

def main():
    # Carregando dados e criando o DataFrame
    path = 'data/train.csv'
    df = dataframe(path, df_clean=True)

    # Criando a barra lateral
    image_path = 'images/logo.png'
    date_slider, traffic_options, weather_cond = sidebar(image_path)

    # Configurando a página do Streamlit
    st.set_page_config(page_title="Marketplace - Cury Company", layout="wide")
    st.title("Marketplace - Visão Entregadores")

    # Filtro de datas
    datas_selecionadas = df['Order_Date'] < date_slider
    df = df.loc[datas_selecionadas, :]

    # Filtro de transito
    transito_selecionado = df['Road_traffic_density'].isin(traffic_options)
    df = df.loc[transito_selecionado, :]

    # Filtro de clima
    clima_selecionado = df['Weatherconditions'].isin(weather_cond)
    df = df.loc[clima_selecionado, :]
    st.markdown(f"Clima: {weather_cond}")

    st.markdown("""---""")

    with st.container():
        st.title("Métricas Gerais")

        col1, col2, col3, col4 = st.columns(4, gap='large', border=True)

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
        st.title("Avaliações")

        col1, col2 = st.columns(2, gap='large', border=True)

        with col1:
            st.markdown("### Avaliação Média por Entregador")
            cols = ['Delivery_person_Ratings', 'Delivery_person_ID']

            df_avg_rat_del = df.loc[:, cols].groupby('Delivery_person_ID').mean().reset_index()
            st.dataframe(df_avg_rat_del)
        with col2:
            st.markdown("### Avaliação Média por Transito")
            cols = ['Delivery_person_Ratings', 'Road_traffic_density']

            # Agrupamento por trânsito
            df_avg_std_rating_by_traf = (df.loc[:, cols]
                                    .groupby('Road_traffic_density')
                                    .agg({'Delivery_person_Ratings': ['mean', 'std']})
                                )
            df_avg_std_rating_by_traf.columns = ['Delivery_mean', 'Delivery_std']
            df_avg_std_rating_by_traf = df_avg_std_rating_by_traf.reset_index()
            st.dataframe(df_avg_std_rating_by_traf)

            st.markdown("### Avaliação Média por Clima")
            cols = ['Delivery_person_Ratings', 'Weatherconditions']

            # Agrupamento por clima
            df_avg_std_rating_by_wet = (df.loc[:, cols]
                                        .groupby('Weatherconditions')
                                        .agg({'Delivery_person_Ratings': ['mean', 'std']})
                                    )
            df_avg_std_rating_by_wet.columns = ['Delivery_mean', 'Delivery_std']
            df_avg_std_rating_by_wet = df_avg_std_rating_by_wet.reset_index()
            st.dataframe(df_avg_std_rating_by_wet)

    st.markdown("""---""")

    with st.container():
        st.title("Velocidade de Entrega")

        col1, col2 = st.columns(2, gap='large', border=True)

        with col1:
            st.markdown("#### Top Entregadores mais Rápidos por Cidade")
            cols = ['Delivery_person_ID', 'City', 'Time_taken(min)']

            # Agrupamento por entregadores mais rápidos por cidade
            df_aux = (df.loc[:, cols]
                        .groupby(['City', 'Delivery_person_ID'])
                        .mean()
                        .sort_values(['City', 'Time_taken(min)'], ascending=True)
                        .reset_index()
                    )
            df2 = df_aux.loc[df_aux['City'] == 'Metropolitian', :].head(10)
            df3 = df_aux.loc[df_aux['City'] == 'Semi-Urban', :].head(10)
            df4 = df_aux.loc[df_aux['City'] == 'Urban', :].head(10)

            df_delivery_fast_by_city = pd.concat([df2, df3, df4]).reset_index(drop=True)
            st.dataframe(df_delivery_fast_by_city)

        with col2:
            st.markdown("#### Top Entregadores mais Lentos por Cidade")
            cols = ['Delivery_person_ID', 'City', 'Time_taken(min)']

            # Agrupamento por entregadores mais lentos por cidade
            df_aux = (df.loc[:, cols]
                        .groupby(['City', 'Delivery_person_ID'])
                        .mean()
                        .sort_values(['City', 'Time_taken(min)'], ascending=False)
                        .reset_index()
                    )
            df2 = df_aux.loc[df_aux['City'] == 'Metropolitian', :].head(10)
            df3 = df_aux.loc[df_aux['City'] == 'Semi-Urban', :].head(10)
            df4 = df_aux.loc[df_aux['City'] == 'Urban', :].head(10)

            df_delivery_slow_by_city = pd.concat([df2, df3, df4]).reset_index(drop=True)
            st.dataframe(df_delivery_slow_by_city)

if __name__ == "__main__":
    main()
