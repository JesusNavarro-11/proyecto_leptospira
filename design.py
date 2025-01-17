import streamlit as st

def display_header_with_logo():
    """
    Muestra el logo y el título de la aplicación de forma modular.
    """
    # Dividir la pantalla en dos columnas para el logo y el título
    col1, col2 = st.columns([1, 5])  # Ajusta las proporciones según sea necesario
    with col1:
        st.image("assets/logo.png", width=80)  # Ruta del logo
    with col2:
        st.markdown(
            """
            <h1 style="color: #333; font-size: 28px; margin-top: 20px;">
                Sistema de Identificación de Leptospira Interrogans
            </h1>
            """,
            unsafe_allow_html=True
        )
