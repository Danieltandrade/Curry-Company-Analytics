"""
Docstring para src.analysis_tools
"""

import folium
import pandas as pd
from plotly import express as px
from streamlit_folium import st_folium

def filtros(df: pd.Series | pd.DataFrame, date_slider: tuple , traffic_options: list, weather_cond: list) -> pd.Series | pd.DataFrame:
    # Filtro de datas
    datas_selecionadas = df['Order_Date'] < date_slider[1]
    df = df.loc[datas_selecionadas, :]

    # Filtro de transito
    transito_selecionado = df['Road_traffic_density'].isin(traffic_options)
    df = df.loc[transito_selecionado, :]

    # Filtro de clima
    clima_selecionado = df['Weatherconditions'].isin(weather_cond)
    df = df.loc[clima_selecionado, :]

    return df

def pedidos_por_dia(df: pd.Series | pd.DataFrame):
    """
    Função para criar um gráfico de barras mostrando o total de pedidos por dia.

    Args:
        df (pd.Series | pd.DataFrame): DataFrame contendo os dados dos pedidos.

    Returns:
        fig (plotly.graph_objs._figure.Figure): Gráfico de barras.

    Example:
    fig = pedidos_por_dia(df)
    """

    df_aux = df.loc[:, ['ID', 'Order_Date']].groupby('Order_Date').count().reset_index()

    # Criando o gráfico de barras
    fig = px.bar(df_aux, x='Order_Date', y='ID')
    
    return fig

def pedidos_por_trafego(df: pd.Series | pd.DataFrame):
    """
    Função para criar um gráfico de pizza mostrando a porcentagem de pedidos por 
    tipo de tráfego.
                    
    Args:
       df (pd.Series | pd.DataFrame): DataFrame contendo os dados dos pedidos.
                        
    Returns:
        fig (plotly.graph_objs._figure.Figure): Gráfico de pizza.

    Example:
        fig = pedidos_por_trafego(df)   
    """

    df_aux = (
        df.loc[:, ['ID', 'Road_traffic_density']]
        .groupby('Road_traffic_density')
        .count()
        .reset_index()
    )
    df_aux['Perc_entregas'] = df_aux['ID'] / df_aux['ID'].sum()

    # Criando o gráfico de pizza
    fig = px.pie(df_aux, values='Perc_entregas', names='Road_traffic_density')

    return fig

def pedidos_cidade_trafego(df: pd.Series | pd.DataFrame):
    """
    Função para criar um gráfico de dispersão mostrando a quantidade de pedidos
    por cidade e tipo de tráfego.

    Args:
        df (pd.Series | pd.DataFrame): DataFrame contendo os dados dos pedidos.

    Returns:
        fig (plotly.graph_objs._figure.Figure): Gráfico de dispersão.

    Example:
        fig = pedidos_cidade_trafego(df)
    """

    df_aux = (
        df.loc[:, ['ID', 'City', 'Road_traffic_density']]
        .groupby(['City', 'Road_traffic_density'])
        .count()
        .reset_index()
    )

    # Criando o gráfico de dispersão
    fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')

    return fig

def pedidos_por_semana(df: pd.Series | pd.DataFrame):
    """
    Função para criar um gráfico de linha mostrando o total de pedidos por semana.

    Args:
        df (pd.Series | pd.DataFrame): DataFrame contendo os dados dos pedidos.

    Returns:
        fig (plotly.graph_objs._figure.Figure): Gráfico de linha.

    Example:
        fig = pedidos_por_semana(df)
    """

    df_aux1 = (
        df.loc[:, ['ID', 'Week_of_Year']]
        .groupby('Week_of_Year')
        .count()
        .reset_index()
    )

    # Criando o gráfico de linha
    fig = px.line(df_aux1, x='Week_of_Year', y='ID')
    
    return fig

def pedidos_por_ent_semana(df: pd.Series | pd.DataFrame):
    """
    Função para criar um gráfico de linhas mostrando a média de pedidos por entregador por semana.

    Args:
        df (pd.Series | pd.DataFrame): DataFrame contendo os dados dos pedidos.

    Returns:
        fig (plotly.graph_objs._figure.Figure): Gráfico de linhas.

    Example:
        fig = pedidos_por_entregador_semana(df)
    """

    df_aux1 = df.loc[:, ['ID', 'Week_of_Year']].groupby('Week_of_Year').count().reset_index()
    df_aux2 = df.loc[:, ['Delivery_person_ID', 'Week_of_Year']].groupby('Week_of_Year').nunique().reset_index()

    df_aux = pd.merge(df_aux1, df_aux2, how='inner')
    df_aux['Order_by_Deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']

    # Criando o gráfico de linhas
    fig = px.line(df_aux, x='Week_of_Year', y='Order_by_Deliver')

    return fig

def mapa_entregas(df: pd.Series | pd.DataFrame) -> None:
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
        folium.Marker(
            [location_info['Delivery_location_latitude'],
            location_info['Delivery_location_longitude']],
            popup=popup_content
        ).add_to(mapa)

    st_folium(mapa, width=1024, height=600)

    return None
