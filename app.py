import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from data_processing import extract_first_frame, preprocess_roi
import cv2

st.title("Sistema de Identificación de Leptospira Interrogans")

st.header("Carga de Video y Selección de ROI")

# Cargar video
uploaded_file = st.file_uploader("Sube un video para análisis", type=["mp4", "avi"])

if uploaded_file:
    try:
        # Extraer el primer fotograma del video
        frame = extract_first_frame(uploaded_file)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convertir a RGB para PIL
        image = Image.fromarray(frame_rgb)

        # Mostrar lienzo interactivo
        st.write("Selecciona el punto central de la ROI haciendo clic en el fotograma:")
        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.3)",  # Color de relleno (no se usa aquí)
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
            # Obtener el punto seleccionado por el usuario
            for obj in canvas_result.json_data["objects"]:
                x = int(obj["left"])
                y = int(obj["top"])
                break  # Tomar el primer punto seleccionado

            st.write(f"Punto seleccionado: ({x}, {y})")

            # Generar ROI automáticamente
            half_size = 150  # Mitad de 300x300
            x1, y1 = max(0, x - half_size), max(0, y - half_size)
            x2, y2 = min(frame.shape[1], x + half_size), min(frame.shape[0], y + half_size)
            roi = frame[y1:y2, x1:x2]

            # Mostrar vista previa de la ROI
            st.write("Vista previa de la región seleccionada:")
            st.image(roi, caption="ROI Seleccionada")

            # Confirmación del usuario
            if st.button("Confirmar selección"):
                roi_preprocessed = preprocess_roi(frame, (x1, y1, x2, y2))
                st.success("ROI confirmada y lista para el modelo.")
                st.image(roi_preprocessed[0], caption="ROI Redimensionada (300x300)")
            else:
                st.warning("Haz clic nuevamente en la zona de interés si deseas cambiar la selección.")

    except ValueError as e:
        st.error(f"Error al procesar el video: {e}")
