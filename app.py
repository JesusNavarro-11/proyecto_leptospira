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

st.header("Carga de Video y Análisis Interactivo")

# Cargar video
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

        # Selección interactiva de ROI
        roi_coords = select_roi(frame)

        if roi_coords:
            x1, y1, x2, y2 = roi_coords
            st.write(f"Coordenadas de ROI seleccionada: ({x1}, {y1}), ({x2}, {y2})")
        
            # Preprocesar ROI
            roi_preprocessed = preprocess_roi(frame, (x1, y1, x2, y2))
            st.success("ROI preprocesada y lista para el modelo.")
        
            # Verificar y corregir el formato para visualización
            st.write(f"Forma de ROI preprocesada: {roi_preprocessed.shape}")
            st.write(f"Tipo de datos de ROI preprocesada: {roi_preprocessed.dtype}")
        
            # ROI debe ser escalada y convertida a uint8
            roi_for_display = (roi_preprocessed[0] * 255).astype("uint8")  # Escalar y convertir
            st.write(f"Forma después de ajuste: {roi_for_display.shape}")
            st.write(f"Tipo de datos después de ajuste: {roi_for_display.dtype}")
        
            # Verificar si es escala de grises o RGB
            if len(roi_for_display.shape) == 2:  # Escala de grises
                roi_image = Image.fromarray(roi_for_display)
            elif len(roi_for_display.shape) == 3 and roi_for_display.shape[2] == 3:  # RGB
                roi_image = Image.fromarray(roi_for_display)
            else:
                raise ValueError("La ROI tiene un formato inesperado para su visualización.")
        
            # Mostrar la ROI redimensionada
            display_centered_image(roi_image, caption="ROI Redimensionada (300x300)", width=300)

    except ValueError as e:
        st.error(f"Error: {e}")


# Preguntar al usuario si desea registrar información
register_info = st.radio("¿Desea registrar información sobre la muestra?", ("Sí", "No"))

patient_data = None
if register_info == "Sí":
    patient_data = collect_patient_info()

# Simular la selección de ROI y procesamiento
st.subheader("Procesamiento de Video")
uploaded_video_path = "sample_video.mp4"  # Ruta simulada de video
roi_coords = (50, 50, 350, 350)  # Coordenadas simuladas de la ROI

with st.spinner("Procesando el video..."):
    result = process_frames_with_clahe(uploaded_video_path, roi_coords)
    st.success("Procesamiento finalizado.")
    st.write(result)

if patient_data:
    st.subheader("Información del Paciente")
    st.json(patient_data)
