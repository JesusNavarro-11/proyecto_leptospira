import streamlit as st
from PIL import Image
import cv2

def select_roi(frame):
    """
    Permite seleccionar un punto en la imagen para calcular la ROI.

    Args:
        frame (numpy array): Fotograma del video.

    Returns:
        tuple: Coordenadas de la ROI (x1, y1, x2, y2) o None si no se seleccionó un punto.
    """
    try:
        # Convertir el fotograma a formato PIL
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)

        # Redimensionar la imagen para despliegue
        st.write("Haz clic en la zona de interés para seleccionar la ROI:")
        clicked = st.image(image, use_column_width=True, output_format="auto")
        
        # Inicializar estado para las coordenadas si no existe
        if "roi_coords" not in st.session_state:
            st.session_state.roi_coords = None

        # Procesar clic en la imagen
        if clicked and st.session_state.roi_coords is None:
            x, y = 200, 200  # Simulación de coordenadas
            st.session_state.roi_coords = (x, y)

        # Si ya tenemos coordenadas, calcular ROI
        if st.session_state.roi_coords:
            x, y = st.session_state.roi_coords
            st.write(f"Punto seleccionado: ({x}, {y})")

            # Calcular ROI alrededor del punto seleccionado
            half_size = 150  # Mitad de 300x300
            x1, y1 = max(0, x - half_size), max(0, y - half_size)
            x2, y2 = min(frame.shape[1], x + half_size), min(frame.shape[0], y + half_size)

            # Mostrar vista previa de la ROI
            roi = frame[y1:y2, x1:x2]
            st.image(roi, caption="ROI Seleccionada")
            return (x1, y1, x2, y2)

        st.info("Haz clic en la imagen para seleccionar un punto.")
        return None
    except Exception as e:
        st.error(f"Error al seleccionar la ROI: {e}")
        return None
