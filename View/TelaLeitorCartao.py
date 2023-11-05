import PySimpleGUI as sg
import cv2
import fitz
from io import BytesIO
from PIL import Image
import numpy as np


class TelaLeitorCartao:
    def __init__(self, controlador):
        self.controlador = controlador
        self.telaGeracaoCartaoResposta = None

        layoutBuscarArquivo = [
            [sg.Text('Caminho', size=(7, 0)), sg.Input(size=(51, 8), key='arquivo'), sg.Button('Buscar', key='buscar')]
        ]

        layoutNumeroPerguntas = [
            [sg.Text('Perguntas:', size=(7)), sg.Input(size=(7, 0), pad=((0, 200), (0, 0)), key='numeroPerguntas'),
             sg.Text('Opções:', size=(7, 0), ), sg.Input(size=(7, 0), key='numeroOpcoes')]
        ]

        layoutEspacamentoMarcador = [
            [sg.Text('Largura:', size=(7)), sg.Input(size=(7, 0), pad=((0, 200), (0, 0)), key='larguraMarcador'),
             sg.Text('Altura:', size=(7, 0), ), sg.Input(size=(7, 0), key='alturaMarcador')]
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

    def Iniciar(self):
        self.eventListner()

    def getCaminho(self):
        return self.janela['arquivo'].get()

    def getLarguraMarcador(self):
        return int(self.janela['larguraMarcador'].get())

    def getAlturaMarcador(self):
        return int(self.janela['alturaMarcador'].get())

    def getEspacamentoResposta(self):
        return int(self.janela['espacamentoResposta'].get())

    def getEspacamentoPergunta(self):
        return int(self.janela['espacamentoPerguntas'].get())

    def getMargemLateral(self):
        return int(self.janela['margemLateral'].get())

    def getMargemSuperior(self):
        return int(self.janela['margemSuperior'].get())

    def getNumeroOpcoes(self):
        return int(self.janela['numeroOpcoes'].get())

    def getNumeroPerguntas(self):
        return int(self.janela['numeroPerguntas'].get())

    def getQuantidadeAlunos(self):
        return int(self.janela['qtdAlunos'].get())

    def getImage(self):
        pdf_document = fitz.open(self.getCaminho())
        page = pdf_document[0]
        pix = page.get_pixmap(matrix=fitz.Matrix(100 / 100, 100 / 100))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img_byte_array = BytesIO()
        img.save(img_byte_array, format="PNG")
        return img

    def atualizar_label(self, texto):
        self.janela['arquivo'].update(texto)

    def previewConfiguracoes(self, image):
        cv2.imshow('Retângulos', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def abrirTelaImportacaoCartaoResposta(self):
        pass

    def getDadosTela(self):
        numeroPerguntas = int(self.janela['numeroPerguntas'].get())
        numeroOpcoes = int(self.janela['numeroOpcoes'].get())
        margemLateral = float(self.janela['margemLateral'].get())
        margemSuperior = float(self.janela['margemSuperior'].get())
        larguraMarcador = int(self.janela['larguraMarcador'].get())
        alturaMarcador = int(self.janela['alturaMarcador'].get())
        espacamentoPerguntas = int(self.janela['espacamentoPerguntas'].get())
        espacamentoResposta = int(self.janela['espacamentoResposta'].get())
        qtdAlunos = int(self.janela['qtdAlunos'].get())
        imagem = self.getImage()
        keypoints, img_cinza = self.controlador.identificandoPontos(imagem)
        return {
            'numeroPerguntas': numeroPerguntas,
            'numeroOpcoes': numeroOpcoes,
            'margemLateral': margemLateral,
            'margemSuperior': margemSuperior,
            'larguraMarcador': larguraMarcador,
            'alturaMarcador': alturaMarcador,
            'espacamentoPerguntas': espacamentoPerguntas,
            'espacamentoResposta': espacamentoResposta,
            'qtdAlunos': qtdAlunos,
            'imagem': imagem,
            'keypoints': keypoints,
            'img_cinza': img_cinza
        }

    def ActiondefiniConfiguracaoLeitura(self):
        dados_tela = self.getDadosTela()
        self.controlador.definirConfiguracao(dados_tela)

    def ActiongeraTxt(self):
        dados_tela = self.getDadosTela()
        dados_para_salvar = {chave: valor for chave, valor in dados_tela.items() if chave not in ["imagem", "keypoints", "img_cinza"]}
        caminho_arquivo = sg.popup_get_file('Salve o arquivo como:', save_as=True, file_types=(("Arquivos de Texto", "*.txt"),))
        if caminho_arquivo:
            self.controlador.salvandoDadosTela(dados_para_salvar, caminho_arquivo)

    def actionPreview(self):
        self.controlador.actionPreview()

    def popupInformativo(self):
        sg.popup('Esta é uma mensagem de informação.', title='Popup de Informação')

    def actionBuscarArquivo(self):
        arquivo_selecionado = sg.popup_get_file("Selecione um arquivo")
        if arquivo_selecionado:
            self.controlador.abrir_explorador_de_arquivos(arquivo_selecionado)

    def eventListner(self):
        while True:
            evento, valores = self.janela.Read()
            if evento == sg.WINDOW_CLOSED:
                break
            elif evento == 'buscar':
                self.actionBuscarArquivo()
            elif evento == 'Preview':
                self.actionPreview()
            elif evento == 'Importar cartao resposta':
                self.controlador.actionImportacao()
            elif evento == 'Definir Configuracao':
                self.ActiondefiniConfiguracaoLeitura()
            elif evento == 'Salvar Configuracao':
                self.ActiongeraTxt()

