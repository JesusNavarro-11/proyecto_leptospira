import streamlit as st
from PIL import Image
import cv2
import numpy as np

def select_roi(frame):
    """
    Permite seleccionar un punto en la imagen usando controles interactivos de Streamlit.

    Args:
        frame (numpy array): Fotograma del video.

    Returns:
        tuple: Coordenadas de la ROI (x1, y1, x2, y2) o None si no se seleccionó un punto.
    """
    try:
        # Convertir el fotograma a formato PIL
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)

        # Redimensionar la imagen para mostrarla en Streamlit
        display_width = 800
        aspect_ratio = image.height / image.width
        display_height = int(display_width * aspect_ratio)
        image_resized = image.resize((display_width, display_height))

        # Mostrar la imagen al usuario
        st.image(image_resized, caption="Selecciona la zona de interés (ROI)", use_container_width=True)

        # Controles deslizantes para seleccionar las coordenadas de la ROI
        st.write("Usa los deslizantes para seleccionar el centro de la ROI:")
        x = st.slider("Coordenada X (horizontal)", 0, display_width, display_width // 2)
        y = st.slider("Coordenada Y (vertical)", 0, display_height, display_height // 2)

        # Botón para confirmar la selección
        if st.button("Confirmar Selección"):
            st.success(f"Punto seleccionado: ({x}, {y})")

            # Calcular la ROI alrededor del punto seleccionado
            half_size = 150  # Mitad de 300x300
            x1 = max(0, x - half_size)
            y1 = max(0, y - half_size)
            x2 = min(display_width, x + half_size)
            y2 = min(display_height, y + half_size)

            # Recortar la ROI original a partir de las coordenadas
            x_ratio = frame.shape[1] / display_width
            y_ratio = frame.shape[0] / display_height
            roi = frame[int(y1 * y_ratio):int(y2 * y_ratio), int(x1 * x_ratio):int(x2 * x_ratio)]

            # Mostrar la ROI seleccionada
            st.image(roi, caption="ROI Seleccionada (300x300)")
            return (int(x1 * x_ratio), int(y1 * y_ratio), int(x2 * x_ratio), int(y2 * y_ratio))

        st.info("Ajusta los deslizantes y haz clic en 'Confirmar Selección' para continuar.")
        return None
    except Exception as e:
        st.error(f"Error al seleccionar la ROI: {e}")
        return None
