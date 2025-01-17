import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from data_processing import extract_first_frame
import cv2

st.title("Sistema de Identificación de Leptospira Interrogans")

st.header("Carga de Video y Selección de ROI")

uploaded_file = st.file_uploader("Sube un video para análisis", type=["mp4", "avi"])

if uploaded_file:
    try:
        # Extraer el primer fotograma del video
        frame = extract_first_frame(uploaded_file)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convertir a RGB
        image = Image.fromarray(frame_rgb)

        # Redimensionar imagen
        image.thumbnail((800, 800), Image.ANTIALIAS)

        # Mostrar lienzo interactivo
        st.write("Selecciona el punto central de la ROI haciendo clic en el fotograma:")
        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.3)",
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
                break

            st.write(f"Punto seleccionado: ({x}, {y})")
    except Exception as e:
        st.error(f"Error al procesar el video o el lienzo: {e}")
