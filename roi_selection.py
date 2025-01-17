import streamlit as st
from PIL import Image
import cv2

def select_roi(frame):
    """
    Permite seleccionar un punto en la imagen para calcular la ROI usando controles en Streamlit.

    Args:
        frame (numpy array): Fotograma del video.

    Returns:
        tuple: Coordenadas de la ROI (x1, y1, x2, y2) o None si no se seleccionó un punto.
    """
    try:
        # Convertir el fotograma a formato PIL
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)

        # Mostrar la imagen
        st.image(image, caption="Selecciona la zona de interés (ROI)", use_column_width=True)

        # Inicializar el estado de las coordenadas si no existe
        if "roi_coords" not in st.session_state:
            st.session_state.roi_coords = {"x": None, "y": None}

        # Controles deslizantes para seleccionar el punto
        st.write("Selecciona el centro de la ROI:")
        x = st.slider("Coordenada X (horizontal)", 0, image.width, image.width // 2)
        y = st.slider("Coordenada Y (vertical)", 0, image.height, image.height // 2)

        # Botón para confirmar la selección
        if st.button("Confirmar Selección"):
            st.session_state.roi_coords = {"x": x, "y": y}
            st.success(f"Punto seleccionado: ({x}, {y})")

        # Procesar y mostrar la ROI seleccionada si el usuario confirma
        if st.session_state.roi_coords["x"] is not None and st.session_state.roi_coords["y"] is not None:
            x = st.session_state.roi_coords["x"]
            y = st.session_state.roi_coords["y"]

            # Calcular la ROI de 300x300 alrededor del punto seleccionado
            half_size = 150
            x1 = max(0, x - half_size)
            y1 = max(0, y - half_size)
            x2 = min(image.width, x + half_size)
            y2 = min(image.height, y + half_size)

            # Mostrar la ROI
            roi = frame[y1:y2, x1:x2]
            st.image(roi, caption="ROI Seleccionada (300x300)")
            return x1, y1, x2, y2

        st.info("Usa los controles deslizantes para seleccionar el centro de la ROI y confirma tu selección.")
        return None
    except Exception as e:
        st.error(f"Error al seleccionar la ROI: {e}")
        return None
