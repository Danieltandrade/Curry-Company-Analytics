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

# Adiciona a raiz do projeto ao sys.path
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(project_root)

# --- IMPORTS DO SEU PROJETO ---
from src.analysis_tools import filtros, pedidos_por_trafego, pedidos_por_dia, pedidos_cidade_trafego
from src.analysis_tools import pedidos_por_semana, pedidos_por_ent_semana, mapa_entregas
from src.data_cleaning import df_cleaning
from src.sider import sidebar
from src.log_config import setup_logging

# Inicializa o logger
setup_logging()
logger = logging.getLogger(__name__)

# O decorador @st.cache_data faz o Streamlit guardar o resultado na memória.
@st.cache_data
def load_data(path):
    return df_cleaning(path, df_clean=True)

def main():

    st.set_page_config(page_title="Marketplace - Curry Company", page_icon='📊', layout="wide")

    # Verifica se a chave 'logged_empresarial' já existe na sessão do usuário.
    # Se não existir, loga e cria a chave. Se existir, pula o log.

    logger.info("Usuário acessou a pagina Visão Empresarial.")
    
    st.title("Marketplace - Visão Empresarial")

    # Define a raiz do projeto dinamicamente
    ROOT_DIR = Path(__file__).parent.parent
    DATA_PATH = ROOT_DIR / 'data' / 'raw' / 'train.csv'

    # Carregando dados (Agora usando a função com Cache)
    df = load_data(str(DATA_PATH))

    if df is None:
        st.error("Erro ao carregar os dados. Verifique os logs para mais detalhes.")
        return

    # Criando a barra lateral
    image_path = 'images/logo.png'

    # Adicionamos tratamento de erro na sidebar para robustez
    try:
        date_slider, traffic_options, weather_cond, cities = sidebar(image_path)
    except Exception as e:
        st.error("Erro ao carregar filtros laterais.")
        logger.error(f"Erro na sidebar: {e}")
        return

    # Aplicando os filtros no dataframe
    # Nota: Filtros são rápidos, geralmente não precisam de cache, mas o resultado muda sempre.
    df = filtros(df, date_slider, traffic_options, weather_cond, cities)

    # Criando abas
    tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

    # Conteúdo da aba Visão Gerencial
    with tab1:
        st.subheader("Visão Gerencial")

        with st.container(border=True):
            st.markdown("### Total de Pedidos por Dia")
            fig = pedidos_por_dia(df)
            st.plotly_chart(fig, width='stretch')

        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### Pedidos por Tipo de Tráfego")
                fig = pedidos_por_trafego(df)
                st.plotly_chart(fig, width='stretch')

            with col2:
                st.markdown("### Pedidos por Cidade e Tipo de Tráfego")
                fig = pedidos_cidade_trafego(df)
                st.plotly_chart(fig, width='stretch')

    # Conteúdo da aba Visão Tática
    with tab2:
        st.subheader("Visão Tática")

        with st.container(border=True):
            st.markdown("### Pedidos por Semana")
            fig = pedidos_por_semana(df)
            st.plotly_chart(fig, width='stretch')

        with st.container(border=True):
            st.markdown("### Pedidos por Entregador por Semana")
            fig = pedidos_por_ent_semana(df)
            st.plotly_chart(fig, width='stretch')

    # Conteúdo da aba Visão Geográfica
    with tab3:
        st.subheader("Visão Geográfica")

        with st.container(border=True):
            st.markdown("### Mapa de Entregas")
            mapa_entregas(df)

if __name__ == "__main__":
    main()
