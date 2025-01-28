import streamlit as st
from PIL import Image, ImageDraw
import cv2
import numpy as np
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg

# Configuración del modelo Detectron2
@st.cache_resource
def load_detectron2_model():
    """
    Carga el modelo Detectron2 con la configuración y pesos preentrenados.

    Returns:
        DefaultPredictor: Modelo listo para realizar inferencias.
    """
    cfg = get_cfg()
    cfg.merge_from_file("configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")  # Cambia si es necesario
    cfg.MODEL.WEIGHTS = "model_final.pth"  # Ruta a tu modelo entrenado
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1  # Número de clases personalizadas
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7  # Umbral de confianza
    cfg.MODEL.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"  # Usar GPU si está disponible
    return DefaultPredictor(cfg)

# Cargar el modelo Detectron2
predictor = load_detectron2_model()

def select_roi_and_detect(frame):
    """
    Permite seleccionar una ROI en la imagen y realiza inferencia con Detectron2.

    Args:
        frame (numpy array): Fotograma del video.

    Returns:
        tuple: Coordenadas de la ROI seleccionada.
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

        # Controles deslizantes para seleccionar las coordenadas
        st.write("Usa los deslizantes para seleccionar el centro de la ROI:")
        x = st.slider("Coordenada X (horizontal)", 0, display_width, display_width // 2)
        y = st.slider("Coordenada Y (vertical)", 0, display_height, display_height // 2)

        # Dibujar los ejes sobre la imagen
        image_with_axes = image_resized.copy()
        draw = ImageDraw.Draw(image_with_axes)
        draw.line([(0, y), (display_width, y)], fill="red", width=2)
        draw.line([(x, 0), (x, display_height)], fill="red", width=2)

        # Mostrar la imagen con los ejes
        st.image(image_with_axes, caption="Vista previa con ejes", use_container_width=True)

        # Botón para confirmar la selección
        if st.button("Confirmar Selección"):
            st.success(f"Punto seleccionado: ({x}, {y})")

            # Calcular la ROI alrededor del punto seleccionado
            half_size = 150  # Mitad de 300x300
            x1 = max(0, x - half_size)
            y1 = max(0, y - half_size)
            x2 = min(display_width, x + half_size)
            y2 = min(display_height, y + half_size)

            # Escalar las coordenadas a la resolución original
            x_ratio = frame.shape[1] / display_width
            y_ratio = frame.shape[0] / display_height
            roi = frame[int(y1 * y_ratio):int(y2 * y_ratio), int(x1 * x_ratio):int(x2 * x_ratio)]

            # Realizar inferencias con Detectron2 en la ROI
            st.info("Procesando la ROI con el modelo...")
            outputs = predictor(roi)

            # Dibujar bounding boxes sobre la ROI
            v = Visualizer(roi[:, :, ::-1], scale=0.8)
            v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
            detected_image = v.get_image()[:, :, ::-1]

            # Mostrar resultados
            st.image(detected_image, caption="Detecciones en la ROI", use_container_width=True)
            return (int(x1 * x_ratio), int(y1 * y_ratio), int(x2 * x_ratio), int(y2 * y_ratio))

        st.info("Ajusta los deslizantes y haz clic en 'Confirmar Selección' para continuar.")
        return None
    except Exception as e:
        st.error(f"Error al seleccionar la ROI: {e}")
        return None
