from moviepy.editor import VideoFileClip
import os

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
    if not os.path.exists(video_file_path):
        raise ValueError(f"El archivo de video no existe: {video_file_path}")

    x1, y1, x2, y2 = roi_coords

    try:
        clip = VideoFileClip(video_file_path)

        # Validar dimensiones del video
        video_width, video_height = clip.size

        # Ajustar coordenadas si están fuera de los límites
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(video_width, x2)
        y2 = min(video_height, y2)

        cropped_clip = clip.crop(x1=x1, y1=y1, x2=x2, y2=y2)
        cropped_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)
        cropped_clip.close()
        return output_path
    except Exception as e:
        print(f"Error detallado: {e}")
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
