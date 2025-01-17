from moviepy.editor import VideoFileClip
import tempfile
import os

def convert_to_mp4(video_file, original_format="mp4"):
    """
    Convierte un video cargado a formato MP4 si no lo está.

    Args:
        video_file: Objeto subido (BytesIO) desde Streamlit.
        original_format (str): Extensión del archivo original (sin punto, por ejemplo, 'mp4').

    Returns:
        str: Ruta del archivo MP4 (convertido o original si ya es MP4).
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
