import streamlit as st
import json
import os


def save_anonymized_data(patient_data, metrics, morphological_info, output_path="shared_data.json"):
    """
    Guarda información anonimizada en un archivo JSON.

    Args:
        patient_data (dict): Información del paciente (se anonimiza eliminando datos personales).
        metrics (dict): Métricas del modelo.
        morphological_info (dict): Información morfológica de la bacteria.
        output_path (str): Ruta del archivo donde guardar los datos compartidos.

    Returns:
        str: Mensaje de éxito con la ruta del archivo.
    """
    # Eliminar datos personales (nombre, dirección, etc.)
    anonymized_data = {k: v for k, v in patient_data.items() if k not in ["Nombre", "Dirección"]}

    # Incluir métricas y datos morfológicos
    anonymized_data["metrics"] = metrics
    anonymized_data["morphological_info"] = morphological_info

    # Guardar en un archivo JSON
    with open(output_path, "w") as f:
        json.dump(anonymized_data, f, indent=4)

    return f"Información compartida guardada en: {output_path}"


def ask_to_share(patient_data, metrics, morphological_info):
    """
    Pregunta al usuario si desea compartir la información y actúa según la respuesta.

    Args:
        patient_data (dict): Información del paciente.
        metrics (dict): Métricas del modelo.
        morphological_info (dict): Información morfológica de la bacteria.
    """
    st.header("Compartir Información de Forma Anónima")

    # Pregunta al usuario
    share_data = st.radio(
        "¿Desea compartir esta información de forma anónima para mejorar el modelo y realizar análisis estadísticos?",
        ("Sí", "No"),
        index=1,  # Por defecto "No"
    )

    if share_data == "Sí":
        try:
            output_path = "shared_data.json"
            message = save_anonymized_data(patient_data, metrics, morphological_info, output_path)
            st.success(message)
            st.info("¡Gracias por contribuir a mejorar el modelo!")
        except Exception as e:
            st.error(f"Ocurrió un error al guardar los datos compartidos: {e}")
    else:
        st.info("No se compartirá la información. Puedes continuar con otras acciones.")
