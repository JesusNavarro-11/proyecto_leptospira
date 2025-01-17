import streamlit as st
from design import display_header_with_logo, display_centered_image
from roi_selection import select_roi
from data_processing import convert_to_mp4, extract_first_frame, preprocess_roi
from video_processing import process_frames_with_clahe
from patient_info import collect_patient_info
from PIL import Image
import os

# Mostrar el encabezado con logo y título
display_header_with_logo()

st.header("Sistema de Identificación de Leptospira Interrogans")

# Paso 1: Cargar video
uploaded_file = st.file_uploader("Sube un video para análisis", type=["mp4", "avi", "mov", "mkv"])

if uploaded_file:
    try:
        # Obtener la extensión del archivo cargado
        file_extension = os.path.splitext(uploaded_file.name)[1][1:]  # Extraer extensión sin punto

        # Convertir a MP4 si es necesario
        st.info("Procesando el archivo...")
        mp4_video_path = convert_to_mp4(uploaded_file, original_format=file_extension)
        st.success("Archivo listo para el análisis.")

        # Extraer el primer fotograma
        frame = extract_first_frame(mp4_video_path)
        display_centered_image(Image.fromarray(frame), caption="Fotograma Inicial", width=800)

        # Paso 2: Selección de ROI
        roi_coords = select_roi(frame)

        if roi_coords:
            x1, y1, x2, y2 = roi_coords
            st.write(f"Coordenadas de ROI seleccionada: ({x1}, {y1}), ({x2}, {y2})")

            # Preprocesar ROI
            roi_preprocessed = preprocess_roi(frame, (x1, y1, x2, y2))
            st.success("ROI preprocesada y lista para el modelo.")
            
            # Mostrar ROI redimensionada
            roi_for_display = (roi_preprocessed[0] * 255).astype("uint8")
            roi_image = Image.fromarray(roi_for_display)
            display_centered_image(roi_image, caption="ROI Redimensionada (300x300)", width=300)

            # Paso 3: Preguntar si desea registrar información
            register_info = st.radio("¿Desea registrar información sobre la muestra?", ("Sí", "No"))

            patient_data = None
            if register_info == "Sí":
                patient_data = collect_patient_info()

            # Paso 4: Procesar el video
            if st.button("Procesar Video"):
                with st.spinner("Procesando el video..."):
                    result = process_frames_with_clahe(mp4_video_path, roi_coords)
                    st.success("Procesamiento finalizado.")
                    st.write(result)

                # Mostrar información del paciente si existe
                if patient_data:
                    st.subheader("Información del Paciente")
                    st.json(patient_data)
    except ValueError as e:
        st.error(f"Error: {e}")
else:
    st.info("Por favor, sube un video para comenzar.")
