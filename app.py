# Streamlit app principal
import streamlit as st

# Título de la app
st.title("Sistema de Identificación de Leptospira Interrogans")


# Subida de archivos
st.header("Carga de archivo")
uploaded_file = st.file_uploader("Sube un video o imagen para análisis", type=["mp4", "png", "jpg"])

if uploaded_file:
    # Mostrar archivo cargado
    st.success(f"Archivo '{uploaded_file.name}' cargado exitosamente.")
    if uploaded_file.name.endswith(".mp4"):
        st.video(uploaded_file)
    else:
        st.image(uploaded_file)


# Punto de entrada
if __name__ == "__main__":
    st.write("Interfaz en construcción...")
