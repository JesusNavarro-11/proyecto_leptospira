import streamlit as st
from roi_selection import select_roi
from data_processing import extract_first_frame, preprocess_roi
from design import add_background  # Importar el módulo de diseño

st.title("Sistema de Identificación de Leptospira Interrogans")

# Agregar fondo
add_background("assets/FondoLeptospiras1.png")  # Ajusta la ruta según tu estructura


st.header("Carga de Video y Análisis Interactivo")

# Cargar video
uploaded_file = st.file_uploader("Sube un video para análisis", type=["mp4", "avi"])

if uploaded_file:
    try:
        # Extraer el primer fotograma
        frame = extract_first_frame(uploaded_file)

        # Selección interactiva de ROI
        roi_coords = select_roi(frame)

        if roi_coords:
            x1, y1, x2, y2 = roi_coords
            st.write(f"Coordenadas de ROI seleccionada: ({x1}, {y1}), ({x2}, {y2})")

            # Preprocesar ROI
            roi_preprocessed = preprocess_roi(frame, (x1, y1, x2, y2))
            st.success("ROI preprocesada y lista para el modelo.")
            st.image(roi_preprocessed[0], caption="ROI Redimensionada (300x300)")
    except ValueError as e:
        st.error(f"Error: {e}")
