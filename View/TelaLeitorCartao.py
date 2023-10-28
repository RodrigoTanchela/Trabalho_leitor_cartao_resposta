import PySimpleGUI as sg
import cv2
import fitz
from io import BytesIO
from PIL import Image
import numpy as np

class TelaLeitorCartao:
    def __init__(self, controlador):
        self.controlador = controlador

        layoutBuscarArquivo = [
            [sg.Text('Caminho', size=(7, 0)), sg.Input(size=(51, 8), key='arquivo'), sg.Button('Buscar', key='buscar')]
        ]

        layoutNumeroPerguntas = [
            [sg.Text('Perguntas:', size=(7)), sg.Input(size=(7, 0), pad=((0, 200), (0, 0)), key='numeroperguntas'),
             sg.Text('Opções:', size=(7, 0), ), sg.Input(size=(7, 0), key='numeroopcoes')]
        ]

        layoutEspacamentoMarcador = [
            [sg.Text('Largura:', size=(7)), sg.Input(size=(7, 0), pad=((0, 200), (0, 0)), key='larguraMarcador'),
             sg.Text('Altura:', size=(7, 0), ), sg.Input(size=(7, 0), key='AlturaMarcador')]
        ]

        layoutEspacamentoPerguntas = [
            [sg.Text('Perguntas:', size=(7)), sg.Input(size=(7, 0), pad=((0, 200), (0, 0)), key='espacamentoPerguntas'),
             sg.Text('Respostas:', size=(7, 0), ), sg.Input(size=(7, 0), key='espacamentoResposta')]
        ]

        loyuotMarginPagina = [
            [sg.Text('Superior:', size=(7)), sg.Input(size=(7, 0), pad=((0, 200), (0, 0)), key='margemSuperior'),
             sg.Text('Lateral:', size=(7, 0), ), sg.Input(size=(7, 0), key='margemLateral')]
        ]

        layoutBotoes = [
            [sg.Button('Preview'), sg.Button('Gerar planilha')]
        ]

        layout = [
            [sg.Frame('', layoutBuscarArquivo, border_width=2, size=(500, 50))],
            [sg.Frame('Número', layoutNumeroPerguntas, border_width=2, size=(500, 50))],
            [sg.Frame('Medidas do campo', layoutEspacamentoMarcador, border_width=2, size=(500, 50))],
            [sg.Frame('Espaçamento', layoutEspacamentoPerguntas, border_width=2, size=(500, 50))],
            [sg.Frame('Margem', loyuotMarginPagina, border_width=2, size=(500, 50))],
            [sg.Frame('', layoutBotoes, border_width=2, size=(500, 50))],
            # [sg.Output(size=(30,20))]
        ]

        # Janela
        self.janela = sg.Window("Dados do Usuário").layout(layout)
        # Extrair os dados da tela
        self.button, self.values = self.janela.Read()

    def atualizar_label(self, texto):
        self.janela['arquivo'].update(texto)

    def extraindoImagem(self):
        pdf_document = fitz.open(self.janela['arquivo'].get())
        page = pdf_document[0]  # Acesse a primeira página ou a página desejada

        # Renderize a página como uma imagem usando PyMuPDF (Fitz)
        pix = page.get_pixmap(matrix=fitz.Matrix(72 / 72, 72 / 72))  # Ajuste a resolução conforme necessário

        # Use Pillow para converter a imagem PyMuPDF em um formato compatível com PySimpleGUI
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Converta a imagem Pillow em bytes para exibição no PySimpleGUI
        img_byte_array = BytesIO()
        img.save(img_byte_array, format="PNG")
        img_bytes = img_byte_array.getvalue()
        return img

    def identificandoPontos(self):
        imagem = self.extraindoImagem()

        params = cv2.SimpleBlobDetector_Params()
        params.filterByColor = True
        params.blobColor = 0
        params.filterByArea = True
        params.minRepeatability = 10
        # params.minArea = 300
        params.maxArea = 350

        img_cinza = cv2.cvtColor(np.array(imagem), cv2.COLOR_BGR2GRAY)

        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(img_cinza)

        imagem_com_keypoints = cv2.drawKeypoints(img_cinza, keypoints, None)

        cv2.imshow("Imagem com Keypoints", imagem_com_keypoints)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def Iniciar(self):
        while True:
            evento, valores = self.janela.read()
            if evento == sg.WINDOW_CLOSED:
                break
            elif evento == 'buscar':
                arquivo_selecionado = sg.popup_get_file("Selecione um arquivo")
                if arquivo_selecionado:
                    self.controlador.abrir_explorador_de_arquivos(arquivo_selecionado)
            elif evento == 'Preview':
                self.identificandoPontos()
                # # Abra a classe Formulario
                # formulario = Formulario()
                # formulario.preencher_formulario("Nome do usuáriodasd", "Email do usuáriasdao")
                # formulario.gerar_pdf("arquivo.pdf")

