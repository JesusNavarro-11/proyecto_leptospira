import streamlit as st
from PIL import Image
import cv2

def select_roi(frame):
    """
    Permite seleccionar un punto en la imagen para calcular la ROI mediante clics reales.

    Args:
        frame (numpy array): Fotograma del video.

    Returns:
        tuple: Coordenadas de la ROI (x1, y1, x2, y2) o None si no se seleccionó un punto.
    """
    try:
        # Convertir el fotograma a formato PIL
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)

        # Redimensionar la imagen para mostrarla de forma más manejable
        display_width = 800
        aspect_ratio = image.height / image.width
        display_height = int(display_width * aspect_ratio)
        image = image.resize((display_width, display_height))

        # Mostrar la imagen y capturar clics mediante HTML/JS
        st.write("Haz clic en la imagen para seleccionar el punto central de la ROI:")
        html_code = f"""
            <div>
                <img src="data:image/png;base64,{image_to_base64(image)}" 
                     style="width:{display_width}px;height:{display_height}px;cursor:crosshair;" 
                     onclick="getClickPosition(event)">
            </div>
            <script>
                function getClickPosition(event) {{
                    var rect = event.target.getBoundingClientRect();
                    var x = Math.round(event.clientX - rect.left);
                    var y = Math.round(event.clientY - rect.top);
                    document.getElementById("coords").value = x + "," + y;
                    document.getElementById("submit-coords").click();
                }}
            </script>
            <form action="" method="GET">
                <input type="hidden" id="coords" name="coords" value="">
                <button id="submit-coords" style="display:none;">Submit</button>
            </form>
        """
        st.markdown(html_code, unsafe_allow_html=True)

        # Leer coordenadas del clic desde la URL
        query_params = st.experimental_get_query_params()
        if "coords" in query_params:
            x, y = map(int, query_params["coords"][0].split(","))
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

def image_to_base64(image):
    """
    Convierte una imagen PIL a base64.

    Args:
        image (PIL.Image): Imagen a convertir.

    Returns:
        str: Representación base64 de la imagen.
    """
    import base64
    from io import BytesIO

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode()
