import streamlit as st
from roi_selection import select_roi
from data_processing import extract_first_frame, preprocess_roi
from design import add_background, start_content_container, end_content_container

# Configuración del fondo
add_background("asset/FondoLeptospiras4.jpg")  # Cambia la URL por tu imagen

# Iniciar contenedor estilizado
start_content_container()

# Contenido principal
st.title("Sistema de Identificación de Leptospira Interrogans")
st.write("Este sistema permite cargar videos, analizar muestras y generar reportes interactivos.")

# Widgets de ejemplo
uploaded_file = st.file_uploader("Sube tu video de muestra", type=["mp4", "avi"])
if uploaded_file:
    st.success("¡Video cargado exitosamente!")

options = st.selectbox("Selecciona un modelo de análisis:", ["Modelo A", "Modelo B", "Modelo C"])
st.write(f"Modelo seleccionado: {options}")

st.button("Iniciar Análisis")

# Finalizar contenedor estilizado
end_content_container()

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
