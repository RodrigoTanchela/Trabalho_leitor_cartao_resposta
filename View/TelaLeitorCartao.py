import PySimpleGUI as sg
import cv2
import fitz
from io import BytesIO
from PIL import Image
import numpy as np
from ProjetoPin3.View.TelaGeracaoCartaoResposta import TelaGeracaoCartaoResposta

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

        layoutAlunos = [
            [sg.Text('Quantidade:', size=(10)), sg.Input(size=(7, 0), pad=((0, 200), (0, 0)), key='qtdAlunos')]
        ]

        layoutBotoes = [
            [sg.Button('Preview'), sg.Button('Definir Configuracao'), sg.Button('Salvar Configuracao'), sg.Button('Importar cartao resposta')]
        ]

        layout = [
            [sg.Frame('', layoutBuscarArquivo, border_width=2, size=(500, 50))],
            [sg.Frame('Número', layoutNumeroPerguntas, border_width=2, size=(500, 50))],
            [sg.Frame('Medidas do campo', layoutEspacamentoMarcador, border_width=2, size=(500, 50))],
            [sg.Frame('Espaçamento', layoutEspacamentoPerguntas, border_width=2, size=(500, 50))],
            [sg.Frame('Margem', loyuotMarginPagina, border_width=2, size=(500, 50))],
            [sg.Frame('Alunos', layoutAlunos, border_width=2, size=(500, 50))],
            [sg.Frame('', layoutBotoes, border_width=2, size=(500, 50))],
            # [sg.Output(size=(30,20))]
        ]

        # Janela
        self.janela = sg.Window("Dados do Usuário").layout(layout)
        self.button, self.values = self.janela.Read()

    def atualizar_label(self, texto):
        self.janela['arquivo'].update(texto)

    def extraindoImagem(self):
        pdf_document = fitz.open(self.janela['arquivo'].get())
        page = pdf_document[0]

        pix = page.get_pixmap(matrix=fitz.Matrix(100 / 100, 100 / 100))

        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        img_byte_array = BytesIO()
        img.save(img_byte_array, format="PNG")
        #img_bytes = img_byte_array.getvalue()
        return img

    def identificandoPontos(self, imagem):
        #imagem = self.extraindoImagem()

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
        return keypoints, img_cinza
        #self.construcaoFormularioRetangular(keypoints, img_cinza)

    def construcaoFormularioRetangular(self, keypoints, image):
        indice = 2
        keypoint = keypoints[indice]
        x = int(keypoint.pt[0])
        y = int(keypoint.pt[1])

        # Tamanho dos retângulos
        print(self.janela['larguraMarcador'].get())
        retangulo_width = int(self.janela['larguraMarcador'].get())
        retangulo_height = int(self.janela['AlturaMarcador'].get())

        distancia_horizontal = int(self.janela['espacamentoResposta'].get())
        distancia_vertical = int(self.janela['espacamentoPerguntas'].get())

        # Posição inicial a partir da qual começar a desenhar
        start_x = int(x + float(self.janela['margemLateral'].get()))
        start_y = int(y + float(self.janela['margemSuperior'].get()))

        # Cor dos retângulos (em BGR)
        color = (0, 255, 0)  # Verde

        thickness = 1
        linhas_limite = int(self.janela['numeroPerguntas'].get())
        linha_atual = 1
        retangulos_desenhados = 0
        retangulos_por_linha = int(self.janela['numeroOpcoes'].get())

        # Desenhe os retângulos na imagem com a posição inicial
        x = start_x
        y = start_y
        for _ in range(linhas_limite):
            for _ in range(retangulos_por_linha):
                x1, y1 = x, y
                x2, y2 = x + retangulo_width, y + retangulo_height
                cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
                x += retangulo_width + distancia_horizontal

            # Mover para a próxima linha
            x = start_x
            y += retangulo_height + distancia_vertical

        # cv2.imshow('Retângulos', image)
        #
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return image

    def previewConfiguracoes(self, image):
        cv2.imshow('Retângulos', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

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

    def Iniciar(self):
        self.eventListner()

    def abrirTelaImportacaoCartaoResposta(self):
        telaGeracaoCartaoResposta = TelaGeracaoCartaoResposta(self.controlador)
        self.telaGeracaoCartaoResposta.setVisible()

    def eventListner(self):
        while True:
            evento, valores = self.janela.Read()
            if evento == sg.WINDOW_CLOSED:
                break
            elif evento == 'buscar':
                arquivo_selecionado = sg.popup_get_file("Selecione um arquivo")
                if arquivo_selecionado:
                    self.controlador.abrir_explorador_de_arquivos(arquivo_selecionado)
            elif evento == 'Preview':
                self.controlador.actionPreview()
            elif evento == 'Importar cartao resposta':
                self.controlador.actionImportacao()
            elif evento == 'Definir Configuracao':
                self.controlador.actionImportacao()

