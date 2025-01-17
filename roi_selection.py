import streamlit as st
from PIL import Image
import base64
from io import BytesIO
import cv2

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
    """
    Permite seleccionar un punto en la imagen y calcula la ROI.

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
        image.thumbnail((800, 800), Image.Resampling.LANCZOS)

        # Convertir la imagen a base64
        image_base64 = image_to_base64(image)
        st.write("Haz clic en la zona de interés:")
        click_url = f'<img src="{image_base64}" style="cursor: crosshair;" usemap="#image-map">'
        st.markdown(click_url, unsafe_allow_html=True)

        # Crear un mapa de clics
        map_html = """
        <map name="image-map">
            <area shape="rect" coords="0,0,{width},{height}" href="?x=50&y=50">
        </map>
        """.format(width=image.width, height=image.height)

        st.markdown(map_html, unsafe_allow_html=True)

        # Procesar coordenadas desde la URL
        query_params = st.experimental_get_query_params()
        if "x" in query_params and "y" in query_params:
            x = int(query_params["x"][0])
            y = int(query_params["y"][0])
            st.write(f"Punto seleccionado: ({x}, {y})")

            # Calcular ROI alrededor del punto seleccionado
            half_size = 150
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
