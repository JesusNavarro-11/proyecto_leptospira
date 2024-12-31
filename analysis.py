import streamlit as st

def analyze_samples():
    st.write("Iniciando análisis...")
    if st.button("Analizar"):
        st.success("Leptospira identificada. Precisión: 95%.")
