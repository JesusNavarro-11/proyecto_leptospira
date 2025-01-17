from PIL import Image
from io import BytesIO
import base64
from streamlit_drawable_canvas import st_canvas
import cv2
import streamlit as st

def image_to_base64(image):
    """
    Convierte una imagen PIL a una cadena base64.

    Args:
        image (PIL.Image): Imagen a convertir.

    Returns:
        str: Representación base64 de la imagen.
    """
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

def select_roi(frame):
    try:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)
        image.thumbnail((800, 800), Image.Resampling.LANCZOS)

        # Convertir imagen a base64
        image_base64 = image_to_base64(image)

        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.3)",
            stroke_width=1,
            background_image_url=image_base64,  # Usar base64 aquí
            update_streamlit=True,
            height=image.height,
            width=image.width,
            drawing_mode="point",
            key="canvas",
        )

        # Procesar la selección del usuario
        if canvas_result.json_data is not None:
            for obj in canvas_result.json_data["objects"]:
                x = int(obj["left"])
                y = int(obj["top"])
                st.write(f"Punto seleccionado: ({x}, {y})")
                half_size = 150
                x1, y1 = max(0, x - half_size), max(0, y - half_size)
                x2, y2 = min(frame.shape[1], x + half_size), min(frame.shape[0], y + half_size)
                roi = frame[y1:y2, x1:x2]
                st.image(roi, caption="ROI Seleccionada")
                return (x1, y1, x2, y2)
    except Exception as e:
        st.error(f"Error al seleccionar la ROI: {e}")
        return None
