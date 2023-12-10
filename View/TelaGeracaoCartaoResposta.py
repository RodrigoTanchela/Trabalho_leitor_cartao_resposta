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
        self.janela = sg.Window("Leitura Cartao Resposta").layout(layout)
        self.button, self.values = self.janela.Read()

    def getImage(self):
        pdf_document = fitz.open(self.janela['arquivo'].get())
        img_cinzas = []
        imagens = []
        for i in range(pdf_document.page_count):
            page = pdf_document[i]
            pix = page.get_pixmap(matrix=fitz.Matrix(100 / 100, 100 / 100))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img = self.ajustar_saturacao(np.array(img), 100)
            img_cinza = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
            img_cinzas.append(img_cinza)
            img = np.array(img)
            imagens.append(img)
        return img_cinzas, imagens

    def ajustar_saturacao(self, imagem, fator_saturacao):
        # Converter a imagem de RGB para HLS
        imagem_hls = cv2.cvtColor(imagem, cv2.COLOR_BGR2HLS)

        # Ajustar a saturação
        imagem_hls[:, :, 2] = np.clip(imagem_hls[:, :, 2] * fator_saturacao, 0, 255)

        # Converter a imagem de volta para RGB
        imagem_rgb = cv2.cvtColor(imagem_hls, cv2.COLOR_HLS2BGR)

        return imagem_rgb

    def atualizar_label(self, texto):
        self.janela['arquivo'].update(texto)

    def popupInformativo(self, msg):
        sg.popup(msg, title='Popup de Informação')

    def actionGeracaoPlanilha(self, img, img_cinza):
        try:
            caminho_arquivo = sg.popup_get_file('Salve o arquivo como:', save_as=True, file_types=(("Arquivos Excel", "*.xlsx"),))
            self.controlador.leituraRespostas(img, img_cinza, caminho_arquivo)
        except Exception as e:
            sg.popup_error(f"Erro ao salva o  arquivo")


    def popupCaixaTesto(self, texto):
        return sg.popup_get_text(texto)

    def popupErro(self, msg):
        sg.popup_error(msg, title='Erro')

    def iniciar(self):
        self.eventListner()

    def actionBuscarArquivo(self):
        try:
            arquivo_selecionado = sg.popup_get_file("Selecione um arquivo")
            if arquivo_selecionado:
                self.controlador.importar_cartao_resposta(arquivo_selecionado)
        except Exception as e:
            sg.popup_error(f"Selecione um arquivo valido")

    def eventListner(self):
        while True:
            evento, values = self.janela.Read()
            if evento == sg.WIN_CLOSED:
                break
            elif evento == 'buscar':
                self.actionBuscarArquivo()
            if evento == 'Geracao Planilha':
                img_cinza, img = self.getImage()
                self.actionGeracaoPlanilha(img, img_cinza)
        self.janela.close()



    def atualizar_label(self, texto):
        self.janela['arquivo'].update(texto)