import streamlit as st
import base64
from io import BytesIO
from PIL import Image

def display_header_with_logo():
    """
    Muestra el logo y el título de la aplicación de forma modular.
    """
    col1, col2 = st.columns([1, 5])  # Ajustar las proporciones entre logo y título
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

def display_centered_image(image, caption=None, width=None):
    """
    Muestra una imagen centrada en la interfaz de Streamlit.

    Args:
        image (str or PIL.Image): Ruta o imagen a mostrar.
        caption (str): Texto opcional para mostrar debajo de la imagen.
        width (int): Ancho opcional para la imagen.
    """
    # Si es una imagen PIL, conviértela a base64
    if isinstance(image, Image.Image):
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        image_src = f"data:image/png;base64,{img_base64}"
    else:
        # Si es una ruta de imagen
        image_src = image

    html_code = f"""
        <div style="text-align: center;">
            <img src="{image_src}" style="width: {width}px; max-width: 100%;" alt="Imagen">
            {'<p style="font-size: 14px; color: #555;">' + caption + '</p>' if caption else ''}
        </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)
