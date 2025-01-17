import streamlit as st

def add_background(image_url):
    """
    Agrega un fondo personalizado a la aplicación.
    
    Args:
        image_url (str): URL o ruta local de la imagen a usar como fondo.
    """
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        .content-container {{
            background-color: rgba(0, 0, 0, 0.7); /* Fondo negro semitransparente */
            padding: 20px;
            border-radius: 10px;
            width: 80%;
            margin: 20px auto;
            color: white; /* Texto blanco para buen contraste */
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5); /* Sombra */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def start_content_container():
    """
    Inicia el contenedor de contenido estilizado.
    """
    st.markdown('<div class="content-container">', unsafe_allow_html=True)

def end_content_container():
    """
    Finaliza el contenedor de contenido estilizado.
    """
    st.markdown('</div>', unsafe_allow_html=True)
