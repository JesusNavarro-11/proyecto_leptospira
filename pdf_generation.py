from fpdf import FPDF
import os


class PDFReport(FPDF):
    def header(self):
        # Título del PDF
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Reporte de Resultados - Sistema de Identificación de Leptospira", ln=True, align="C")
        self.ln(10)

    def footer(self):
        # Pie de página
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")


def generate_pdf_with_info(output_path, patient_info, metrics, morphological_info, grad_cam_path):
    """
    Genera un PDF con información del paciente y resultados.

    Args:
        output_path (str): Ruta donde guardar el PDF generado.
        patient_info (dict): Información del paciente.
        metrics (dict): Métricas del modelo.
        morphological_info (dict): Información morfológica de la bacteria.
        grad_cam_path (str): Ruta de la imagen Grad-CAM.
    """
    pdf = PDFReport()
    pdf.add_page()

    # Información del paciente
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "Información del Paciente:", ln=True)
    for key, value in patient_info.items():
        pdf.cell(0, 10, f"{key}: {value}", ln=True)
    pdf.ln(10)

    # Métricas
    pdf.cell(0, 10, "Métricas del Modelo:", ln=True)
    for key, value in metrics.items():
        pdf.cell(0, 10, f"{key}: {value}", ln=True)
    pdf.ln(10)

    # Información morfológica
    pdf.cell(0, 10, "Información Morfológica de la Bacteria:", ln=True)
    for key, value in morphological_info.items():
        pdf.cell(0, 10, f"{key}: {value}", ln=True)
    pdf.ln(10)

    # Imagen Grad-CAM
    if os.path.exists(grad_cam_path):
        pdf.cell(0, 10, "Fotograma con Grad-CAM aplicado:", ln=True)
        pdf.image(grad_cam_path, x=10, y=None, w=180)

    # Guardar PDF
    pdf.output(output_path)


def generate_pdf_without_info(output_path, metrics, morphological_info, grad_cam_path):
    """
    Genera un PDF solo con resultados.

    Args:
        output_path (str): Ruta donde guardar el PDF generado.
        metrics (dict): Métricas del modelo.
        morphological_info (dict): Información morfológica de la bacteria.
        grad_cam_path (str): Ruta de la imagen Grad-CAM.
    """
    pdf = PDFReport()
    pdf.add_page()

    # Métricas
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "Métricas del Modelo:", ln=True)
    for key, value in metrics.items():
        pdf.cell(0, 10, f"{key}: {value}", ln=True)
    pdf.ln(10)

    # Información morfológica
    pdf.cell(0, 10, "Información Morfológica de la Bacteria:", ln=True)
    for key, value in morphological_info.items():
        pdf.cell(0, 10, f"{key}: {value}", ln=True)
    pdf.ln(10)

    # Imagen Grad-CAM
    if os.path.exists(grad_cam_path):
        pdf.cell(0, 10, "Fotograma con Grad-CAM aplicado:", ln=True)
        pdf.image(grad_cam_path, x=10, y=None, w=180)

    # Guardar PDF
    pdf.output(output_path)
