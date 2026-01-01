"""
Cria a barra lateral do dashboard utilizando funções do Streamlit.
A barra lateral inclui uma imagem, um slider para seleção de datas
e uma caixa de seleção múltipla para condições de trânsito.
"""

from datetime import datetime
import streamlit as st


def sidebar(image_path: str) -> tuple[tuple[datetime, datetime], list[str], list[str], list[str]]:
    """
    Cria a barra lateral do dashboard utilizando funções do Streamlit.
    A barra lateral inclui uma imagem, um slider para seleção de datas
    e uma caixa de seleção múltipla para condições de trânsito.

    Args:
        image_path (str): Caminho para a imagem do logo.

    Returns:
        tuple[datetime, list[str]]: Data selecionada e condições de trânsito selecionadas.
        list[str]: Lista de Strings com opções de transito
        list[str]: Lista de Strings com opções climáticas
        list[str]: Lista de Strings com opções de cidades
        None: Se ocorrer algum erro.
    """

    st.sidebar.image(image_path, width=270)
    
    st.sidebar.markdown("# Bem-vindo ao Dashboard!")
    st.sidebar.markdown("## Fastest Delivery in Town")
    st.sidebar.markdown("""---""")

    date_slider = st.sidebar.slider(
        "Pesquise por intervalo de datas!",
        min_value=datetime(2022, 2, 11),
        max_value=datetime(2022, 4, 5),
        value=(datetime(2022, 2, 11), datetime(2022, 4, 5)),
        format="YYYY-MM-DD"
    )

    st.sidebar.markdown("""---""")

    traffic_options = st.sidebar.multiselect(
        "Condições de Trânsito",
        ["Low", "Medium", "High", "Jam"],
        default=["Low", "Medium", "High", "Jam"],
        width='stretch'
    )

    st.sidebar.markdown("""---""")

    opcoes_wet_cond = ['Cloudy', 'Fog', 'Sandstorms', 'Storms', 'Sunny', 'Windy']
    wet_cond_options = st.sidebar.multiselect(
        "Cindições Climáticas", 
        opcoes_wet_cond,
        default=opcoes_wet_cond, 
        width='stretch'
    )

    st.sidebar.markdown("""---""")

    opcoes_city = ['Metropolitian', 'Semi-Urban', 'Urban']
    cities_options = st.sidebar.multiselect(
        "Cidades",
        opcoes_city,
        default=opcoes_city,
        width='stretch'
    )

    st.sidebar.markdown("""---""")
    st.sidebar.markdown("Powered by Daniel Torres de Andrade")

    return date_slider, traffic_options, wet_cond_options, cities_options
