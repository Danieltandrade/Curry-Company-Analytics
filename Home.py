"""
Home Page da aplicação Streamlit.
Aqui o usuário encontra uma visão geral do dashboard e instruções de uso.
"""

import logging
import os
import streamlit as st
from src import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Home", 
    page_icon="🏠", 
    layout='wide'
)

# Captura acesso acesso a página pelo usuário
logger.info("Usuário acessou a Home Page.")

if os.path.exists('images/logo.png'):
    st.sidebar.image('images/logo.png', width=270)
else:
    # Se a imagem sumir, o app não quebra, mas você fica sabendo no log.
    logger.warning(f"Logo não encontrado no caminho: {'images/logo.png'}. Exibindo apenas texto.")
    st.sidebar.markdown("### Curry Company")

st.sidebar.markdown("# Bem-vindo ao Dashboard!")
st.sidebar.markdown("## Fastest Delivery in Town")
st.sidebar.markdown("""---""")

st.markdown("# Curry Company Dashboard")

st.markdown("""---""")

st.markdown("""
    ##### Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.

    ---

    ### Como utilizar esse Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Insights de geolocalização.
    - Visão Entregadores:
        - Acompanhamento dos indicadores semanais de crescimento.
    - Visão Restaurantes:
        - Indicadores semanais de crescimento dos restaurantes.

    ---

    ### Ask for Help:
        danieltorresandrade@gmail.com
""")

# Confirma que a página inteira foi renderizada sem erros ocultos
logger.debug("Home Page renderizada com sucesso.")
