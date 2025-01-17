import streamlit as st
from streamlit_click_detector import click_detector
from PIL import Image
import cv2

def select_roi(frame):
    """
    Permite seleccionar el punto central de la ROI haciendo clic en el fotograma.

    Args:
        frame (numpy array): Fotograma del video.

    Returns:
        tuple: Coordenadas de la ROI (x1, y1, x2, y2) o None si no se seleccionó un punto.
    """
    try:
        # Convertir el fotograma a formato PIL
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)

        # Mostrar imagen y capturar clic
        st.write("Haz clic en la zona de interés para seleccionar la ROI:")
        result = click_detector(image, key="image_click")

        # Procesar coordenadas del clic
        if result:
            x, y = result["x"], result["y"]
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
