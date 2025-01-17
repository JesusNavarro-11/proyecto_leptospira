import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import cv2

def select_roi(frame):
    """
    Muestra un lienzo interactivo para seleccionar el punto central de la ROI.
    
    Args:
        frame (numpy array): Fotograma del video.

    Returns:
        tuple: Coordenadas de la ROI (x1, y1, x2, y2) o None si no se seleccionó un punto.
    """
    try:
        # Convertir el fotograma a formato PIL
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)

        # Redimensionar la imagen para evitar problemas de tamaño
        image.thumbnail((800, 800), Image.ANTIALIAS)

        # Mostrar lienzo interactivo
        st.write("Selecciona el punto central de la ROI haciendo clic en el fotograma:")
        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.3)",  # Color del punto seleccionado
            stroke_width=1,
            background_image=image,
            update_streamlit=True,
            height=image.height,
            width=image.width,
            drawing_mode="point",
            key="canvas",
        )

        # Procesar selección del usuario
        if canvas_result.json_data is not None:
            for obj in canvas_result.json_data["objects"]:
                x = int(obj["left"])
                y = int(obj["top"])
                st.write(f"Punto seleccionado: ({x}, {y})")

                # Calcular ROI alrededor del punto seleccionado
                half_size = 150  # Mitad de 300x300
                x1, y1 = max(0, x - half_size), max(0, y - half_size)
                x2, y2 = min(frame.shape[1], x + half_size), min(frame.shape[0], y + half_size)

                # Mostrar vista previa de la ROI
                roi = frame[y1:y2, x1:x2]
                st.write("Vista previa de la región seleccionada:")
                st.image(roi, caption="ROI Seleccionada")

                # Confirmar selección
                if st.button("Confirmar selección"):
                    return (x1, y1, x2, y2)
                else:
                    st.warning("Haz clic nuevamente en la zona de interés si deseas cambiar la selección.")
                    return None
    except Exception as e:
        st.error(f"Error al seleccionar la ROI: {e}")
        return None
