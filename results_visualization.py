import streamlit as st
from PIL import Image, ImageDraw
import numpy as np

def display_grad_cam_result(frame, grad_cam_overlay):
    """
    Muestra el fotograma con Grad-CAM aplicado.

    Args:
        frame (numpy array): Fotograma original como arreglo de NumPy.
        grad_cam_overlay (numpy array): Mapa Grad-CAM superpuesto.

    Returns:
        None
    """
    # Convertir a imágenes PIL
    frame_image = Image.fromarray(frame)
    grad_cam_image = Image.fromarray(grad_cam_overlay)

    # Combinar la imagen original con el overlay (simulación básica)
    combined = Image.blend(frame_image, grad_cam_image, alpha=0.5)

    # Mostrar en Streamlit
    st.image(combined, caption="Fotograma con Grad-CAM aplicado", use_container_width=True)


def display_metrics():
    """
    Muestra métricas simuladas como precisión, sensibilidad, y especificidad.

    Returns:
        None
    """
    st.subheader("Métricas del Modelo")
    metrics = {
        "Precisión": "90%",
        "Sensibilidad": "85%",
        "Especificidad": "88%",
    }
    for metric, value in metrics.items():
        st.write(f"- **{metric}:** {value}")


def display_morphological_info():
    """
    Muestra información morfológica simulada de la bacteria.

    Returns:
        None
    """
    st.subheader("Información Morfológica")
    st.write("- **Tamaño Promedio:** 15 µm")
    st.write("- **Forma:** Espiral")
    st.write("- **Patrón de Movimiento:** Helicoidal")
