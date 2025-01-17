import streamlit as st

import streamlit as st

def display_centered_image(image, caption=None, width=None):
    """
    Muestra una imagen centrada en la interfaz de Streamlit.

    Args:
        image (str or PIL.Image): Ruta o imagen a mostrar.
        caption (str): Texto opcional para mostrar debajo de la imagen.
        width (int): Ancho opcional para la imagen.
    """
    html_code = f"""
        <div style="text-align: center;">
            <img src="data:image/png;base64,{image}" alt="image" style="width: {width}px; max-width: 100%;">
            <p style="font-size: 14px; color: #555;">{caption}</p>
            <

def display_header_with_logo():
    """
    Muestra el logo y el título de la aplicación de forma modular.
    """
    # Dividir la pantalla en dos columnas para el logo y el título
    col1, col2 = st.columns([1, 5])  # Ajusta las proporciones según sea necesario
    with col1:
        st.image("assets/FondoLeptospiras4.jpg", width=80)  # Ruta del logo
    with col2:
        st.markdown(
            """
            <h1 style="color: #333; font-size: 28px; margin-top: 20px;">
                Sistema de Identificación de Leptospira Interrogans
            </h1>
            """,
            unsafe_allow_html=True
        )
