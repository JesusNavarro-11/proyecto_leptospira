import streamlit as st
from PIL import Image
from data_processing import preprocess_roi, extract_first_frame

st.title("Sistema de Identificación de Leptospira Interrogans")

st.header("Selección de ROI y Preprocesamiento")

# Cargar video
uploaded_file = st.file_uploader("Sube un video para análisis", type=["mp4", "avi"])
if uploaded_file:
    try:
        # Extraer el primer fotograma del video
        frame = extract_first_frame(uploaded_file)

        # Mostrar el primer fotograma como referencia
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        st.image(image, caption="Selecciona manualmente la ROI en esta imagen.")

        # Ingresar coordenadas de la ROI
        st.write("Ingresa las coordenadas de la ROI:")
        x1 = st.number_input("x1", min_value=0, max_value=frame.shape[1], value=50)
        y1 = st.number_input("y1", min_value=0, max_value=frame.shape[0], value=50)
        x2 = st.number_input("x2", min_value=x1, max_value=frame.shape[1], value=350)
        y2 = st.number_input("y2", min_value=y1, max_value=frame.shape[0], value=350)

        # Procesar ROI
        if st.button("Procesar ROI"):
            roi_preprocessed = preprocess_roi(frame, (x1, y1, x2, y2))
            st.write("ROI preprocesada lista para el modelo.")
            st.image(roi_preprocessed[0], caption="ROI Redimensionada (300x300)")

    except ValueError as e:
        st.error(f"Error al procesar el video: {e}")
