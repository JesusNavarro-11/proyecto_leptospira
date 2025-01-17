import cv2
import numpy as np
import tempfile

def extract_first_frame(video_file):
    """
    Extrae el primer fotograma de un archivo de video cargado.
    
    Args:
        video_file: Objeto subido (BytesIO) desde Streamlit.

    Returns:
        numpy array: Primer fotograma del video.
    """
    try:
        # Guardar el archivo en un directorio temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(video_file.read())
            temp_path = temp_file.name

        # Leer el video desde el archivo temporal
        cap = cv2.VideoCapture(temp_path)
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
