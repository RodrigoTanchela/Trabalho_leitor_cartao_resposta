from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

class Formulario:
    def __init__(self):
        self.nome = ""
        self.email = ""

    def preencher_formulario(self, nome, email):
        self.nome = nome
        self.email = email

    def gerar_pdf(self, nome_arquivo):
        doc = SimpleDocTemplate(nome_arquivo, pagesize=letter)
        story = []

        styles = getSampleStyleSheet()
        story.append(Paragraph(f'Nome: {self.nome}', styles['Normal']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f'Email: {self.email}', styles['Normal']))

        doc.build(story)
        # Abra o arquivo PDF após a criação
        os.startfile(nome_arquivo)
