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
    st.title("Marketplace - Visão Empresarial")

    # Filtro de datas
    datas_selecionadas = df['Order_Date'] < date_slider[1]
    df = df.loc[datas_selecionadas, :]

    # Filtro de transito
    transito_selecionado = df['Road_traffic_density'].isin(traffic_options)
    df = df.loc[transito_selecionado, :]

    # Filtro de clima
    clima_selecionado = df['Weatherconditions'].isin(weather_cond)
    df = df.loc[clima_selecionado, :]
    st.markdown(f"Clima: {weather_cond}")


    # Criando abas para diferentes visões
    tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

    # Conteúdo da aba Visão Gerencial
    with tab1:
        st.subheader("Visão Gerencial")

        with st.container(border=True):

            cols1 = ['ID', 'Order_Date']
            df_aux = df.loc[:, cols1].groupby('Order_Date').count().reset_index()

            fig1 = px.bar(df_aux, x='Order_Date', y='ID')
            st.plotly_chart(fig1, width='stretch')

        with st.container(border=True):

            col1, col2 = st.columns(2, border=True)
            with col1:
                st.markdown("### Pedidos por Tipo de Tráfego")

                cols2 = ['ID', 'Road_traffic_density']

                df_aux = df.loc[:, cols2].groupby('Road_traffic_density').count().reset_index()
                df_aux['Perc_entregas'] = df_aux['ID'] / df_aux['ID'].sum()

                fig2 = px.pie(df_aux, values='Perc_entregas', names='Road_traffic_density')
                st.plotly_chart(fig2, width='stretch')

            with col2:
                st.markdown("### Pedidos por Cidade e Tipo de Tráfego")

                cols3 = ['ID', 'City', 'Road_traffic_density']

                df_aux = df.loc[:, cols3].groupby(['City', 'Road_traffic_density']).count().reset_index()

                fig3 = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')
                st.plotly_chart(fig3, width='stretch')

    with tab2:
        st.subheader("Visão Tática")

        with st.container(border=True):
            st.markdown("### Pedidos por Semana")

            cols4 = ['ID', 'Week_of_Year']
            df_aux1 = df.loc[:, cols4].groupby('Week_of_Year').count().reset_index()

            fig4 = px.line(df_aux1, x='Week_of_Year', y='ID')
            st.plotly_chart(fig4, width='stretch')

        with st.container(border=True):
            st.markdown("### Pedidos por Entregador por Semana")

            cols5 = ['Delivery_person_ID', 'Week_of_Year']

            df_aux1 = df.loc[:, cols4].groupby('Week_of_Year').count().reset_index()
            df_aux2 = df.loc[:, cols5].groupby('Week_of_Year').nunique().reset_index()

            df_aux = pd.merge(df_aux1, df_aux2, how='inner')
            df_aux['Order_by_Deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']

            fig5 = px.line(df_aux, x='Week_of_Year', y='Order_by_Deliver')
            st.plotly_chart(fig5, width='stretch')

    with tab3:
        st.subheader("Visão Geográfica")

        with st.container(border=True):
            st.markdown("### Mapa de Entregas")

            cols6 = ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']

            df_aux = df.loc[:, cols6].groupby(['City', 'Road_traffic_density']).median().reset_index()

            mapa = folium.Map()

            for index, location_info in df_aux.iterrows():
                # Criando o conteúdo do popup como uma string formatada
                popup_content = f"""
                    <b>Cidade:</b> {location_info['City']}<br>
                    <b>Tráfego:</b> {location_info['Road_traffic_density']}
                """

                # Adicionando o marcador ao mapa
                folium.Marker([location_info['Delivery_location_latitude'],
                            location_info['Delivery_location_longitude']],
                            popup=popup_content).add_to(mapa)

            st_folium(mapa, width=1024, height=600)

if __name__ == "__main__":
    main()
