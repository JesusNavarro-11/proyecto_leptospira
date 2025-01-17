import streamlit as st

# Carga de videos
st.header("Carga de Video")
uploaded_file = st.file_uploader("Sube un video en formato MP4 o AVI", type=["mp4", "avi"])
if uploaded_file:
    st.success(f"Archivo '{uploaded_file.name}' cargado exitosamente.")
    st.video(uploaded_file)
