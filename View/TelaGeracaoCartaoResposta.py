import PySimpleGUI as sg
import cv2
import fitz
from io import BytesIO
from PIL import Image
import numpy as np
class TelaGeracaoCartaoResposta:
    def __init__(self, controlador):
        self.controlador = controlador

        layoutBuscarArquivo = [
            [sg.Text('Caminho', size=(7, 0)), sg.Input(size=(51, 8), key='arquivo'), sg.Button('Buscar', key='buscar')]
        ]
        layoutBotoes = [
            [sg.Button('Geracao Planilha')]
        ]
        layout = [
            [sg.Frame('', layoutBuscarArquivo, border_width=2, size=(500, 50))],
            [sg.Frame('', layoutBotoes, border_width=2, size=(500, 50))],
        ]

        # Janela
        self.janela = sg.Window("Dados do Usuário").layout(layout)
        self.button, self.values = self.janela.Read()

    def setVisible(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == 'Mostrar Segunda View':
                self.mostrar_segunda_view()
        self.window.close()

    def leituraRespostas(self, imagem_cinza, imagem_cartao):
        # Aplicar uma limiarização para binarizar a imagem
        _, imagem_binarizada = cv2.threshold(imagem_cinza, 128, 255, cv2.THRESH_BINARY)

        # Encontrar contornos na imagem binarizada
        contornos, _ = cv2.findContours(imagem_binarizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Definir uma lista para armazenar as marcações preenchidas
        marcacoes_preenchidas = []

        # Iterar sobre os contornos
        for contorno in contornos:
            # Calcular a área do contorno
            area = cv2.contourArea(contorno)

            # Se a área do contorno for maior que um limite (marcação preenchida), adicione à lista
            if area > 100:  # Ajuste este limite de acordo com suas necessidades
                marcacoes_preenchidas.append(contorno)

        # Desenhe os contornos das marcações preenchidas na imagem original
        cv2.drawContours(imagem_cartao, marcacoes_preenchidas, -1, (0, 0, 255), 2)

        # Exibir a imagem com as marcações destacadas
        cv2.imshow('Cartão de Respostas', imagem_cartao)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Agora você pode processar as marcações preenchidas (por exemplo, contando o número de marcações).
        print(f"Número de marcações preenchidas: {len(marcacoes_preenchidas)}")

    def atualizar_label(self, texto):
        self.janela['arquivo'].update(texto)