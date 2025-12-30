"""
Projeto para construção de um Dashboard interativo utilizando Python e Streamlit.

Autor: Daniel Torres de Andrade
Data: 28 de Dezembro de 2025
Descrição: Este script inicializa o aplicativo Streamlit e exibe uma mensagem de boas-vindas.

"""

# Importando Bibliotecas
import numpy as np
import streamlit as st
from dataframe import dataframe
from config import sidebar
from haversine import haversine as hs
from plotly import express as px
import plotly.graph_objects as go

def main():
    # Carregando dados e criando o DataFrame
    path = 'data/train.csv'
    df = dataframe(path, df_clean=True)

    # Criando a barra lateral
    image_path = 'images/logo.png'
    date_slider, traffic_options, weather_cond = sidebar(image_path)

    # Configurando a página do Streamlit
    st.set_page_config(page_title="Marketplace - Cury Company", layout="wide")
    st.title("Marketplace - Visão Restaurantes", text_alignment='center', width='stretch')

    # Filtro de datas
    datas_selecionadas = df['Order_Date'] < date_slider[1]
    df = df.loc[datas_selecionadas, :]

    # Filtro de transito
    transito_selecionado = df['Road_traffic_density'].isin(traffic_options)
    df = df.loc[transito_selecionado, :]

    # Filtro de clima
    clima_selecionado = df['Weatherconditions'].isin(weather_cond)
    df = df.loc[clima_selecionado, :]

    st.markdown("""---""")

    with st.container():
        st.markdown("# Métricas Gerais", text_alignment='center')
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

            #Realizando o cálculo da distância entre restaurante e local de entrega com apply
            df['Distance'] = df.loc[:, cols].apply(
                lambda x: hs((x[cols[0]], x[cols[1]]), 
                (x[cols[2]], x[cols[3]])), 
                axis=1
            )
            media_dist = df.loc[:, 'Distance'].mean()
            col2.metric("#### Distância \nMédia (km)", f"{media_dist:.2f}")

        with col3:
            # Novo DF com média e desvio padrão por cidade
            df_aux = (
                df.loc[:, ['Time_taken(min)', 'Festival']]
                .groupby('Festival')
                .agg({'Time_taken(min)': ['mean', 'std']}))

            # Renomeando colunas
            df_aux.columns = ['Time_mean(min)', 'Time_std(min)']
            df_aux = df_aux.reset_index()

            avg_festival = df_aux.loc[df_aux['Festival'] == 'Yes', 'Time_mean(min)']
            st.metric("#### Tempo Médio \nFestival (min)", f"{avg_festival.values[0]:.1f}")

        with col4:
            std_festival = df_aux.loc[df_aux['Festival'] == 'Yes', 'Time_std(min)']
            st.metric("#### Desvio Padrão \nFestival (min)", f"{std_festival.values[0]:.1f}")

        with col5:
            avg_no_festival = df_aux.loc[df_aux['Festival'] == 'No', 'Time_mean(min)']
            st.metric("#### Tempo Médio \nFestival (min)", f"{avg_no_festival.values[0]:.1f}")

        with col6:
            std_no_festival = df_aux.loc[df_aux['Festival'] == 'No', 'Time_std(min)']
            st.metric("#### Desvio Padrão \nFestival (min)", f"{std_no_festival.values[0]:.1f}")

    with st.container():
        col1, col2 = st.columns(2, border=True)

        with col1:

            st.markdown("### Média e desvio padrão do tempo por cidade", text_alignment='center')
            # Novo DF com média e desvio padrão por cidade
            df_aux = (
                df.loc[:, ['Time_taken(min)', 'City']]
                .groupby('City')
                .agg({'Time_taken(min)': ['mean', 'std']})
            )

            # Renomeando colunas
            df_aux.columns = ['Time_mean(min)', 'Time_std(min)']
            df_aux = df_aux.reset_index()

            fig2 = go.Figure()
            fig2.add_trace(
                go.Bar(
                    name='Controle',
                    x=df_aux['City'],
                    y=df_aux['Time_mean(min)'],
                    error_y=dict(type='data', 
                    array=df_aux['Time_std(min)'])
                )
            )

            fig2.update_layout(barmode='group')
            col1.plotly_chart(fig2, width='stretch')

        with col2:
            st.markdown("### Distribuição de distância", text_alignment='center')

            # Novo DF com média e desvio padrão por cidade e tipo de pedido
            df_aux = (
                df.loc[:, ['Time_taken(min)', 'City', 'Type_of_order']]
                .groupby(['City', 'Type_of_order'])
                .agg({'Time_taken(min)': ['mean', 'std']})
            )

            # Renomeando colunas
            df_aux.columns = ['Time_mean(min)', 'Time_std(min)']
            df_aux.reset_index()

            st.dataframe(df_aux, width='stretch')

    with st.container():
        st.markdown("### Distribuição do tempo")
        col1, col2 = st.columns(2, border=True)

        with col1:
            st.markdown("### Tempo médio de entrega por cidade", text_alignment='center')
            cols = [
                'Delivery_location_latitude', 
                'Delivery_location_longitude', 
                'Restaurant_latitude', 
                'Restaurant_longitude'
            ]

            #Realizando o cálculo da distância entre restaurante e local de entrega com apply
            df['Distance'] = df.loc[:, cols].apply(
                lambda x: hs((x[cols[0]], x[cols[1]]), 
                (x[cols[2]], x[cols[3]])), 
                axis=1
            )
            media_dist = df.loc[:, ['City', 'Distance']].groupby('City').mean().reset_index()

            fig1 = go.Figure(data=[go.Pie(labels=media_dist['City'], 
                                        values=media_dist['Distance'], 
                                        pull=[0, 0.1, 0])]
            )
            st.plotly_chart(fig1, width='stretch')

        with col2:
            st.markdown(
                "### Tempo médio de entrega por cidade e tipo de tráfego", 
                text_alignment='center'
            )

            # Novo DF com média e desvio padrão por cidade e tipo de tráfego
            df_aux = (
                df.loc[:, ['Time_taken(min)', 'City', 'Road_traffic_density']]
                    .groupby(['City', 'Road_traffic_density'])
                    .agg({'Time_taken(min)': ['mean', 'std']})
            )

            # Renomeando colunas
            df_aux.columns = ['Time_mean(min)', 'Time_std(min)']
            df_aux = df_aux.reset_index()

            fig3 = px.sunburst(
                df_aux,
                path=['City', 'Road_traffic_density'],
                values='Time_mean(min)',
                color='Time_std(min)',
                color_continuous_scale='RdBu',
                color_continuous_midpoint=np.average(df_aux['Time_std(min)'])
            )
            st.plotly_chart(fig3, width='stretch')

if __name__ == "__main__":
    main()
