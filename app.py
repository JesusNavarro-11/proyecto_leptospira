import streamlit as st
from utils import data_processing, analysis, visualization

# Título de la aplicación
st.title("Sistema de Identificación de Leptospira Interrogans")

# Menú principal
menu = st.sidebar.selectbox("Seleccione una opción", ["Carga y Preprocesamiento", "Análisis de Muestras", "Visualización de Resultados"])

if menu == "Carga y Preprocesamiento":
    st.header("Carga y Preprocesamiento de Videos")
    data_processing.process_videos()

elif menu == "Análisis de Muestras":
    st.header("Análisis de Muestras")
    analysis.analyze_samples()

elif menu == "Visualización de Resultados":
    st.header("Visualización de Resultados")
    visualization.show_results()
