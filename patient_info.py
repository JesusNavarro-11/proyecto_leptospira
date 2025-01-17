import streamlit as st

def collect_patient_info():
    """
    Despliega un formulario para registrar información del paciente.

    Returns:
        dict: Información ingresada por el usuario.
    """
    st.header("Registro de Información del Paciente")
    patient_info = {}
    
    # Campos del formulario
    patient_info["name"] = st.text_input("Nombre del paciente:")
    patient_info["address"] = st.text_area("Domicilio:")
    patient_info["symptoms"] = st.text_area("Síntomas (separe por comas):")
    patient_info["sample_date"] = st.date_input("Fecha de la muestra:")
    patient_info["notes"] = st.text_area("Notas adicionales:")
    
    if st.button("Guardar Información"):
        st.success("Información guardada correctamente.")
        return patient_info

    return None
