from datetime import datetime
import streamlit as st


def sidebar(image_path: str) -> tuple[tuple[datetime, datetime], list[str], list[str]]:
    """
    Cria a barra lateral do dashboard utilizando funções do Streamlit.
    A barra lateral inclui uma imagem, um slider para seleção de datas
    e uma caixa de seleção múltipla para condições de trânsito.

    Args:
        image_path (str): Caminho para a imagem do logo.

    Returns:
        tuple[datetime, list[str]]: Data selecionada e condições de trânsito selecionadas.
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
        default=["Low", "Medium", "High", "Jam"]
    )

    st.sidebar.markdown("""---""")

    opcoes = ['Cloudy', 'Fog', 'Sandstorms', 'Storms', 'Sunny', 'Windy']
    opcoes_climaticas = st.sidebar.segmented_control(
        "Cindições Climáticas", 
        opcoes, 
        selection_mode="multi", 
        default=opcoes, 
        width='stretch'
    )

    st.sidebar.markdown("""---""")
    st.sidebar.markdown("Powered by Daniel Torres de Andrade")

    return date_slider, traffic_options, opcoes_climaticas
