import PySimpleGUI as sg
from ProjetoPin3.model.Aluno import Aluno
from ProjetoPin3.model.CartaoResposta import CartaoResposta
from ProjetoPin3.model.ConfiguracaoQuestao import ConfiguracaoQuestao
from ProjetoPin3.model.ConfiguracaoOpcoes import ConfiguracoesOpcoes
from ProjetoPin3.View.TelaGeracaoCartaoResposta import TelaGeracaoCartaoResposta
from ProjetoPin3.model.GeracaoPlanilha import GeracaoPlanilha
import PySimpleGUI as sg
import cv2
import fitz
from io import BytesIO
from PIL import Image
import numpy as np

class ControladorLeitorCartao:
    def __init__(self):
        self.visaoLeitorCartaoResposta = None
        self.aluno = None
        self.cartaoResposta = None
        self.configuracaoOpcoes = None
        self.configuracaoQuestao = None
        self.geracaoPlanilha = None
        self.questoes = None

    def abrir_explorador_de_arquivos(self, arquivo_selecionado):
        # self.modelo.arquivo_selecionado = arquivo_selecionado
        self.visaoLeitorCartaoResposta.atualizar_label(arquivo_selecionado)

    def actionPreview(self):
        img = self.visaoLeitorCartaoResposta.extraindoImagem()
        keypoints, img_cinza = self.visaoLeitorCartaoResposta.identificandoPontos(img)
        image = self.visaoLeitorCartaoResposta.construcaoFormularioRetangular(keypoints, img_cinza)
        self.visaoLeitorCartaoResposta.previewConfiguracoes(image)

    def importar_cartao_resposta(self,  arquivo_selecionado):
        self.telaGeracaoCartaoResposta.atualizar_label(arquivo_selecionado)

    def salvarKeypoints(self, keypoints):
        pass

    def definirConfiguracao(self, configuracao):
        numeroPerguntas = configuracao['numeroPerguntas']
        numeroOpcoes = configuracao['numeroOpcoes']
        margemLateral = configuracao['margemLateral']
        margemSuperior = configuracao['margemSuperior']
        larguraMarcador = configuracao['larguraMarcador']
        alturaMarcador = configuracao['alturaMarcador']
        espacamentoPerguntas = configuracao['espacamentoPerguntas']
        espacamentoResposta = configuracao['espacamentoResposta']
        qtdAlunos = configuracao['qtdAlunos']

        keypoints = configuracao['keypoints']
        keypoint = keypoints[2]
        posicaoHorizontal = int(keypoint.pt[0])
        posicaoVertical = int(keypoint.pt[1])

        self.configuracaoQuestao = ConfiguracaoQuestao(numeroPerguntas, espacamentoPerguntas, margemSuperior, margemLateral, qtdAlunos, posicaoHorizontal, posicaoVertical)
        self.configuracaoResposta = ConfiguracoesOpcoes(numeroOpcoes, espacamentoResposta, larguraMarcador, alturaMarcador)


    def actionImportacao(self):
        self.telaGeracaoCartaoResposta = TelaGeracaoCartaoResposta(self)
        self.visaoLeitorCartaoResposta.abrirTelaImportacaoCartaoResposta()
        self.telaGeracaoCartaoResposta.setVisible()

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

