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
        for i in range(3):
            page = pdf_document[i]
            pix = page.get_pixmap(matrix=fitz.Matrix(100 / 100, 100 / 100))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img_byte_array = BytesIO()
            img.save(img_byte_array, format="PNG")
            img_cinza = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
            img_cinzas.append(img_cinza)
            imagens.append(img)
        return img_cinzas, imagens

    def atualizar_label(self, texto):
        self.janela['arquivo'].update(texto)

    def popupInformativo(self, msg):
        sg.popup(msg, title='Popup de Informação')

    # def popupSelecao(self):
    #     opcoes = ['A', 'B', 'C', 'D']
    #
    #     # Exibe um popup de escolha de opção
    #     escolha = sg.popup_get_choice('Escolha uma opção:', title='Opções', values=opcoes)
    #
    #     # Verifica a escolha do usuário
    #     if escolha:
    #         print(f'O usuário escolheu: {escolha}')
    #     else:
    #         print('Nenhuma opção selecionada.')

    def actionGeracaoPlanilha(self, img):
        caminho_arquivo = sg.popup_get_file('Salve o arquivo como:', save_as=True, file_types=(("Arquivos Excel", "*.xlsx"),))
        self.controlador.leituraRespostas(img, caminho_arquivo)

    def setVisible(self):
        while True:
            evento, values = self.janela.Read()
            if evento == sg.WIN_CLOSED:
                pass
            elif evento == 'buscar':
                arquivo_selecionado = sg.popup_get_file("Selecione um arquivo")
                if arquivo_selecionado:
                    self.controlador.importar_cartao_resposta(arquivo_selecionado)
            if evento == 'Geracao Planilha':
                img_cinza, img = self.getImage()
                self.actionGeracaoPlanilha(img_cinza)
        self.window.close()



    def atualizar_label(self, texto):
        self.janela['arquivo'].update(texto)