"""
Home Page da aplicação Streamlit.
Aqui o usuário encontra uma visão geral do dashboard e instruções de uso.
"""

import streamlit as st
from src import setup_logging

setup_logging()

st.set_page_config(page_title="Home", page_icon="🏠", layout='wide')

st.markdown("# Curry Company Dashboard")
st.markdown("""
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar esse Growth Dashboard?
    - **Visão Empresa:** Acompanhamento dos pedidos e entregas.
    - **Visão Entregadores:** Acompanhamento da performance dos entregadores.
    - **Visão Restaurantes:** Acompanhamento da qualidade dos restaurantes.
""")
