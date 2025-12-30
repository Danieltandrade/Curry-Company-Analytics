"""
Docstring para dataframe.data_manipulation

Função para manipulação de DataFrames utilizando Pandas.
"""

# Importando Bibliotecas
import os
import pandas as pd
import streamlit as st

@st.cache_data
def dataframe(path: str, df_clean: bool = True) -> pd.DataFrame:
    """
    Função para ler e opcionalmente limpar um arquivo CSV em um DataFrame do Pandas.

    Args:
        path (str): Caminho para o arquivo CSV.
        df_clean (bool): Indica se o DataFrame deve ser limpo. Padrão é True.
    Returns:
        pd.DataFrame: DataFrame do Pandas, limpo ou original.
    """

    # 1. Verificação de segurança do caminho do arquivo
    if not os.path.exists(path):
        raise FileNotFoundError(f"O arquivo não foi encontrado: {path}")
    
    # 2. Lendo o arquivo CSV
    try:
        df = pd.read_csv(path)

        if df_clean:
        
            # Copiando o Dataframe para manipulação
            df1 = df.copy()

            # Convertendo a coluna 'Delivery_person_Age' para número inteiro
            linhas_selecionadas = df1['Delivery_person_Age'] != "NaN "
            df1 = df1.loc[linhas_selecionadas, :].copy()
            df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

            # Convertendo a coluna 'Delivery_person_Ratings' para número decimal
            df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

            # Convertendo a coluna 'Order_Date' para data
            df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')

            # Eliminando 'NaN ' da coluna 'Weatherconditions'
            linhas_selecionadas = df1['Weatherconditions'] != "conditions NaN"
            df1 = df1.loc[linhas_selecionadas, :].copy()

            # Convertendo a coluna 'multiple_deliveries' para número inteiro
            linhas_selecionadas = df1['multiple_deliveries'] != "NaN "
            df1 = df1.loc[linhas_selecionadas, :].copy()
            df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

            # Eliminando 'NaN ' da coluna 'City'
            linhas_selecionadas = df1['City'] != "NaN "
            df1 = df1.loc[linhas_selecionadas, :].copy()

            # Eliminando 'NaN ' da coluna 'Festival'
            linhas_selecionadas = df1['Festival'] != "NaN "
            df1 = df1.loc[linhas_selecionadas, :].copy()

            # Eliminando '(min) ' da coluna 'Time_taken(min)' e convertendo para inteiro
            df1['Time_taken(min)'] = df1['Time_taken(min)'].str.extract(r'(\d+)').astype(int)

            # Retirando espaços dos conteúdos presentes nas colunas
            df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
            df1.loc[:, 'Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
            df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
            df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
            df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
            df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
            df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()

            # Mudando o conteúdo da coluna 'Weatherconditions'
            cond_clim_alteradas = {
                'conditions Cloudy': 'Cloudy',
                'conditions Fog': 'Fog',
                'conditions Sandstorms': 'Sandstorms',
                'conditions Stormy': 'Stormy',
                'conditions Sunny': 'Sunny',
                'conditions Windy': 'Windy'
            }
            df1['Weatherconditions'] = df1['Weatherconditions'].replace(cond_clim_alteradas)

            # Criando a coluna com as semanas do ano
            df1['Week_of_Year'] = df1['Order_Date'].dt.isocalendar().week

            # Realizando reset do index
            df1 = df1.reset_index(drop=True)

            # Retornando o Dataframe tratado "df1"
            return df1

        else:
            # Retornando o Dataframe original "df"
            return df
       
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
        return pd.DataFrame() # Retorna vazio em caso de erro crítico
