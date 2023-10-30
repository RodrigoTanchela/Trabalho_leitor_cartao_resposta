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
            [sg.Text('Perguntas:', size=(7)), sg.Input(size=(7, 0), pad=((0, 200), (0, 0)), key='numeroPerguntas'),
             sg.Text('Opções:', size=(7, 0), ), sg.Input(size=(7, 0), key='numeroOpcoes')]
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
        params.minRepeatability = 12
        # params.minArea = 300
        params.maxArea = 350

        img_cinza = cv2.cvtColor(np.array(imagem), cv2.COLOR_BGR2GRAY)

        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(img_cinza)

        imagem_com_keypoints = cv2.drawKeypoints(img_cinza, keypoints, None)

        # cv2.imshow("Imagem com Keypoints", imagem_com_keypoints)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        self.construcaoFormularioRetangular(keypoints, img_cinza)

    def construcaoFormularioCircular(self, keypoints, image):
        indice = 2
        keypoint = keypoints[indice]
        x = keypoint.pt[0]
        y = keypoint.pt[1]
        # Especifica o centro e o raio do círculo
        center = (int(x+float(self.values['margemSuperior'])), int(y+float(self.values['margemLateral'])))
        radius = 4
        color = (0, 0, 255)
        thickness = 2

        # Desenhe o círculo na imagem
        cv2.circle(image, center, radius, color, thickness)

        # Exiba a imagem
        cv2.imshow('Círculo', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def construcaoFormularioRetangular(self, keypoints, image):
        self.atualizar_interface()
        indice = 2
        keypoint = keypoints[indice]
        x = int(keypoint.pt[0])
        y = int(keypoint.pt[1])

        # Tamanho dos retângulos
        retangulo_width = int(self.values['larguraMarcador'])
        retangulo_height = int(self.values['AlturaMarcador'])


        distancia_horizontal = int(self.values['espacamentoResposta'])
        distancia_vertical = int(self.values['espacamentoPerguntas'])

        # Posição inicial a partir da qual começar a desenhar
        start_x = int(x+float(self.values['margemSuperior']))
        #start_y = int(y+float(self.values['margemLateral']))

        # Cor dos retângulos (em BGR)
        color = (0, 255, 0)  # Verde

        # Espessura da linha do retângulo (pode ser -1 para preencher os retângulos)
        thickness = 1
        linhas_limite = int(self.values['numeroPerguntas'])
        linha_atual = 1
        retangulos_desenhados = 0
        retangulos_por_linha = int(self.values['numeroOpcoes'])

        # Desenhe os retângulos na imagem com a posição inicial
        x = start_x
        for _ in range(linhas_limite):
            for _ in range(retangulos_por_linha):
                x1, y1 = x, y
                x2, y2 = x + retangulo_width, y + retangulo_height
                cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
                x += retangulo_width + distancia_horizontal

            # Mover para a próxima linha
            x = start_x
            y += retangulo_height + distancia_vertical

        cv2.imshow('Retângulos', image)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def Iniciar(self):
        self.eventListner()

    def eventListner(self):
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

