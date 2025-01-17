import streamlit as st
from PIL import Image
import cv2

def select_roi(frame):
    """
    Permite seleccionar un punto en la imagen para calcular la ROI sin recargar la página.

    Args:
        frame (numpy array): Fotograma del video.

    Returns:
        tuple: Coordenadas de la ROI (x1, y1, x2, y2) o None si no se seleccionó un punto.
    """
    try:
        # Convertir el fotograma a formato PIL
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)

        # Redimensionar la imagen para mostrarla de forma manejable
        display_width = 800
        aspect_ratio = image.height / image.width
        display_height = int(display_width * aspect_ratio)
        image = image.resize((display_width, display_height))

        # Mostrar la imagen
        st.write("Haz clic en el botón para seleccionar el punto central de la ROI:")
        st.image(image, use_column_width=False, caption="Haz clic en la imagen para seleccionar la ROI")

        # Crear inputs para capturar clics
        if "roi_coords" not in st.session_state:
            st.session_state.roi_coords = None

        # Botón para simular la selección interactiva
        x = st.slider("Selecciona X (horizontal)", min_value=0, max_value=display_width, value=display_width // 2)
        y = st.slider("Selecciona Y (vertical)", min_value=0, max_value=display_height, value=display_height // 2)

        if st.button("Confirmar Selección"):
            st.session_state.roi_coords = (x, y)
            st.success(f"ROI seleccionada en ({x}, {y})")

        # Mostrar coordenadas seleccionadas y calcular ROI
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

        st.info("Selecciona un punto en la imagen usando los controles deslizantes.")
        return None
    except Exception as e:
        st.error(f"Error al seleccionar la ROI: {e}")
        return None
