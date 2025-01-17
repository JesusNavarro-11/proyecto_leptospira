import streamlit as st

def add_background(image_path):
    """
    Agrega una imagen de fondo a la aplicación de Streamlit.

    Args:
        image_path (str): Ruta relativa de la imagen de fondo.
    """
    try:
        with open(image_path, "rb") as f:
            base64_image = f.read().encode("base64").decode()  # Convierte la imagen a base64
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: url("data:image/png;base64,{base64_image}");
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

