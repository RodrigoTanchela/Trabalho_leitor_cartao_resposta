import PySimpleGUI as sg
import cv2
import fitz
from io import BytesIO
from PIL import Image
import json


class TelaLeitorCartao:
    def __init__(self, controlador):
        self.controlador = controlador
        self.telaGeracaoCartaoResposta = None

        layoutBuscarArquivo = [
            [sg.Text('Arquivo'), sg.Input(size=(51, 1), key='arquivo'), sg.Button('Buscar', key='buscar')],
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

        layoutCampoTeste = [
            [sg.Text('Teste:', size=(7)), sg.Input(size=(7, 0), pad=((0, 200), (0, 0)), key='teste')]
        ]

        # layoutAlunos = [
        #     [sg.Text('Quantidade:', size=(10)), sg.Input(size=(7, 0), pad=((0, 200), (0, 0)), key='qtdAlunos')]
        # ]

        layoutBotoes = [
            [sg.Button('Preview'), sg.Button('Definir Configuracao'), sg.Button('Salvar Configuracao'), sg.Button('Importar cartao resposta'), sg.Button('Carregar Dados')]
        ]

        layout = [
            [sg.Frame('Importar', layoutBuscarArquivo, border_width=2, size=(600, 50))],
            [sg.Frame('Número', layoutNumeroPerguntas, border_width=2, size=(600, 50))],
            [sg.Frame('Medidas do campo', layoutEspacamentoMarcador, border_width=2, size=(600, 50))],
            [sg.Frame('Espaçamento', layoutEspacamentoPerguntas, border_width=2, size=(600, 50))],
            [sg.Frame('Margem', loyuotMarginPagina, border_width=2, size=(600, 50))],
            [sg.Frame('Teste', layoutCampoTeste, border_width=2, size=(600, 50))],
            # [sg.Frame('Alunos', layoutCampoTeste, border_width=2, size=(600, 50))],
            [sg.Frame('', layoutBotoes, border_width=2, size=(600, 50))],

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

    def getTeste(self):
        return int(self.janela['teste'].get())

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

    # def getQuantidadeAlunos(self):
    #     return int(self.janela['qtdAlunos'].get())

    def getImage(self):
        pdf_document = fitz.open(self.getCaminho())
        page = pdf_document[int(self.getTeste())]
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

    def trataDadosTela(self):
        dados = self.getDadosTela()
        numeroPerguntas = int(dados['numeroPerguntas'])
        numeroOpcoes = int(dados['numeroOpcoes'])
        margemLateral = int(dados['margemLateral'])
        margemSuperior = int(dados['margemSuperior'])
        larguraMarcador = int(dados['larguraMarcador'])
        alturaMarcador = int(dados['alturaMarcador'])
        espacamentoPerguntas = int(dados['espacamentoPerguntas'])
        espacamentoResposta = int(dados['espacamentoResposta'])
        # qtdAlunos = int(dados['qtdAlunos'])
        return {
            'numeroPerguntas': numeroPerguntas,
            'numeroOpcoes': numeroOpcoes,
            'margemLateral': margemLateral,
            'margemSuperior': margemSuperior,
            'larguraMarcador': larguraMarcador,
            'alturaMarcador': alturaMarcador,
            'espacamentoPerguntas': espacamentoPerguntas,
            'espacamentoResposta': espacamentoResposta,
            # 'qtdAlunos': qtdAlunos,
        }

    def getDadosTela(self):
        numeroPerguntas = int(self.janela['numeroPerguntas'].get())
        numeroOpcoes = int(self.janela['numeroOpcoes'].get())
        margemLateral = int(self.janela['margemLateral'].get())
        margemSuperior = int(self.janela['margemSuperior'].get())
        larguraMarcador = int(self.janela['larguraMarcador'].get())
        alturaMarcador = int(self.janela['alturaMarcador'].get())
        espacamentoPerguntas = int(self.janela['espacamentoPerguntas'].get())
        espacamentoResposta = int(self.janela['espacamentoResposta'].get())
        # qtdAlunos = int(self.janela['qtdAlunos'].get())
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
            # 'qtdAlunos': qtdAlunos,
            'imagem': imagem,
            'keypoints': keypoints,
            'img_cinza': img_cinza
        }

    def actiondefiniConfiguracaoLeitura(self):
        try:
            dados_tela = self.getDadosTela()
            self.controlador.definirConfiguracao(dados_tela)
        except Exception as e:
            self.popupErro('Erro ao executar a ação de definir configuração verifique os campos e tente novamente')


    def ActionGeraTxt(self):
        try:
            dados_tela = self.getDadosTela()
            dados_para_salvar = {chave: valor for chave, valor in dados_tela.items() if chave not in ["imagem", "keypoints", "img_cinza"]}
            caminho_arquivo = sg.popup_get_file('Salve o arquivo como:', save_as=True, file_types=(("Arquivos de Texto", "*.txt"),))
            if caminho_arquivo:
                self.controlador.salvandoDadosTela(dados_para_salvar, caminho_arquivo)
                self.popupInformativo(f'Dados salvos em {caminho_arquivo}')
        except Exception as e:
            self.popupErro('Erro ao executar a ação geracao txt verifique os campos e tente novamente')


    def actionPreview(self):
        try:
            self.controlador.actionPreview()
        except Exception as e:
            self.popupErro('Erro ao executar a ação preview verifique os campos e tente novamente')

    def popupInformativo(self, msg):
        sg.popup(msg, title='Popup de Informação')

    def popupErro(self, msg):
        sg.popup_error(msg, title='Erro')

    def actionBuscarArquivo(self):
        arquivo_selecionado = sg.popup_get_file("Selecione um arquivo")
        if arquivo_selecionado:
            self.controlador.abrir_explorador_de_arquivos(arquivo_selecionado)

    def carregar_dados(self):
        # Solicite ao usuário que selecione o arquivo JSON
        caminho_arquivo = sg.popup_get_file('Selecione o arquivo JSON', file_types=(("Arquivos TXT", "*.txt"),))

        if caminho_arquivo:
            try:
                with open(caminho_arquivo, 'r') as arquivo_json:
                    dados = json.load(arquivo_json)
                    for chave, valor in dados.items():
                        if chave in self.janela.AllKeysDict:
                            self.janela[chave].update(valor)
            except Exception as e:
                sg.popup_error(f"Erro ao carregar os dados do txt: {str(e)}")

    def eventListner(self):
        while True:
            evento, valores = self.janela.Read()
            if evento == sg.WINDOW_CLOSED:
                break
            elif evento == 'buscar':
                self.actionBuscarArquivo()
            elif evento == 'buscartxt':
                self.actionBuscarArquivo()
            elif evento == 'Preview':
                self.actionPreview()
            elif evento == 'Importar cartao resposta':
                self.controlador.actionImportacao()
            elif evento == 'Definir Configuracao':
                self.actiondefiniConfiguracaoLeitura()
            elif evento == 'Salvar Configuracao':
                self.ActionGeraTxt()
            elif evento == 'Carregar Dados':
                self.carregar_dados()

