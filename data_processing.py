import cv2
import numpy as np
import tempfile
from moviepy.editor import VideoFileClip
import os

def convert_to_mp4(video_file, original_format="mp4"):
    """
    Convierte un video cargado a formato MP4 si no lo está.

    Args:
        video_file: Objeto subido (BytesIO) desde Streamlit.
        original_format (str): Extensión del archivo original (sin punto, por ejemplo, 'mp4').

    Returns:
        str: Ruta del archivo MP4 convertido.
    """
    # Si el archivo ya es MP4, guárdalo directamente y devuélvelo
    if original_format.lower() == "mp4":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(video_file.read())
            return temp_file.name

    # Guardar el archivo en un directorio temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_mp4:
        temp_mp4_path = temp_mp4.name

    try:
        # Cargar el video con moviepy
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{original_format}") as temp_input:
            temp_input.write(video_file.read())
            temp_input_path = temp_input.name

        clip = VideoFileClip(temp_input_path)

        # Escribir el archivo en formato MP4
        clip.write_videofile(temp_mp4_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)
        clip.close()

        # Limpiar archivo temporal original
        os.remove(temp_input_path)

        return temp_mp4_path
    except Exception as e:
        raise ValueError(f"Error al convertir el video a MP4: {e}")


def extract_first_frame(video_file_path):
    """
    Extrae el primer fotograma de un archivo de video cargado.

    Args:
        video_file_path: Ruta al archivo de video (MP4).

    Returns:
        numpy array: Primer fotograma del video.
    """
    try:
        # Leer el video desde la ruta proporcionada
        cap = cv2.VideoCapture(video_file_path)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            raise ValueError("No se pudo leer el primer fotograma del video. Verifica el formato del archivo.")
        
        return frame
    except Exception as e:
        raise ValueError(f"Error al procesar el video: {e}")


def preprocess_roi(frame, roi_coords, target_size=(300, 300)):
    """
    Recorta y redimensiona la ROI seleccionada a las dimensiones del modelo.
    
    Args:
        frame (numpy array): Fotograma del video.
        roi_coords (tuple): Coordenadas de la ROI (x1, y1, x2, y2).
        target_size (tuple): Dimensiones a las que se redimensionará la ROI.

    Returns:
        numpy array: ROI preprocesada lista para el modelo.
    """
    x1, y1, x2, y2 = roi_coords
    # Validar coordenadas de ROI
    if x1 >= x2 or y1 >= y2:
        raise ValueError("Las coordenadas de la ROI son inválidas. Asegúrate de que x2 > x1 y y2 > y1.")
    
    try:
        # Recortar la ROI
        roi = frame[int(y1):int(y2), int(x1):int(x2)]
        # Redimensionar la ROI a 300x300
        roi_resized = cv2.resize(roi, target_size)
        # Normalización
        roi_normalized = roi_resized / 255.0
        return np.expand_dims(roi_normalized, axis=0)  # Agregar dimensión batch
    except Exception as e:
        raise ValueError(f"Error al procesar la ROI: {e}")



def crop_video_to_roi(video_file_path, roi_coords, output_path="cropped_video.mp4"):
    """
    Recorta un video a la ROI especificada.

    Args:
        video_file_path (str): Ruta al archivo de video original.
        roi_coords (tuple): Coordenadas de la ROI (x1, y1, x2, y2).
        output_path (str): Ruta para guardar el video recortado.

    Returns:
        str: Ruta del video recortado.
    """
    x1, y1, x2, y2 = roi_coords

    try:
        clip = VideoFileClip(video_file_path)
        cropped_clip = clip.crop(x1=x1, y1=y1, x2=x2, y2=y2)
        cropped_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)
        cropped_clip.close()
        return output_path
    except Exception as e:
        raise ValueError(f"Error al recortar el video: {e}")


def process_frames_with_clahe(video_file_path, roi_coords, fps=6):
    """
    Simula el procesamiento del video: recorta, extrae fotogramas y aplica CLAHE.

    Args:
        video_file_path (str): Ruta al archivo original del video.
        roi_coords (tuple): Coordenadas de la ROI (x1, y1, x2, y2).
        fps (int): Tasa de fotogramas por segundo para extraer.

    Returns:
        list: Lista de rutas de fotogramas procesados.
    """
    cropped_video = crop_video_to_roi(video_file_path, roi_coords)
    # Aquí simulamos el procesamiento sin implementar CLAHE y modelo real.
    return f"Simulación de procesamiento completo para {cropped_video}"
