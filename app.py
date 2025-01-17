import streamlit as st
from design import display_centered_image
from roi_selection import select_roi
from data_processing import extract_first_frame, preprocess_roi
from PIL import Image

st.title("Sistema de Identificación de Leptospira Interrogans")

st.header("Carga de Video y Análisis Interactivo")

# Cargar video
uploaded_file = st.file_uploader("Sube un video para análisis", type=["mp4", "avi"])

if uploaded_file:
    try:
        # Extraer el primer fotograma
        frame = extract_first_frame(uploaded_file)
        display_centered_image(Image.fromarray(frame), caption="Fotograma Inicial", width=800)

        # Selección interactiva de ROI
        roi_coords = select_roi(frame)

        if roi_coords:
            x1, y1, x2, y2 = roi_coords
            st.write(f"Coordenadas de ROI seleccionada: ({x1}, {y1}), ({x2}, {y2})")

            # Preprocesar ROI
            roi_preprocessed = preprocess_roi(frame, (x1, y1, x2, y2))
            st.success("ROI preprocesada y lista para el modelo.")
            display_centered_image(Image.fromarray(roi_preprocessed[0]), caption="ROI Redimensionada (300x300)", width=300)
    except ValueError as e:
        st.error(f"Error: {e}")
