import streamlit as st
import base64  # Asegúrate de importar la biblioteca base64

def add_background(image_path):
    """
    Agrega una imagen de fondo a la aplicación de Streamlit.

    Args:
        image_path (str): Ruta relativa de la imagen de fondo.
    """
    try:
        with open(image_path, "rb") as f:
            base64_image = base64.b64encode(f.read()).decode()  # Corrección aquí
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: url("data:image/jpeg;base64,{base64_image}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.error(f"Error: La imagen de fondo no se encontró en la ruta {image_path}. Verifica la ubicación.")
    except Exception as e:
        st.error(f"Error inesperado al cargar el fondo: {e}")
