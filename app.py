import streamlit as st
import data_processing
import analysis
import visualization

st.title("Sistema de Identificación de Leptospira Interrogans")

menu = st.sidebar.selectbox("Seleccione una opción", ["Carga de Videos", "Análisis", "Visualización"])

if menu == "Carga de Videos":
    data_processing.process_videos()
elif menu == "Análisis":
    analysis.analyze_samples()
elif menu == "Visualización":
    visualization.show_results()
