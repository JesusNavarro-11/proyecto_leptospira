import streamlit as st
import matplotlib.pyplot as plt

def show_results():
    metrics = {"Precisión": 0.95, "Sensibilidad": 0.92, "Especificidad": 0.88}
    fig, ax = plt.subplots()
    ax.bar(metrics.keys(), metrics.values())
    st.pyplot(fig)
