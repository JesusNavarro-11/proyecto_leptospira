import streamlit as st

def process_videos():
    uploaded_file = st.file_uploader("Sube un video", type=["mp4", "avi", "mov"])
    if uploaded_file:
        st.success(f"Archivo '{uploaded_file.name}' cargado exitosamente.")
        st.video(uploaded_file)
