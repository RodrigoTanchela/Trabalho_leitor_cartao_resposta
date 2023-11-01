import PySimpleGUI as sg
from ProjetoPin3.model.Aluno import Aluno
from ProjetoPin3.model.CartaoResposta import CartaoResposta
from ProjetoPin3.model.ConfiguracaoQuestao import ConfiguracaoQuestao
from ProjetoPin3.model.ConfiguracaoOpcoes import ConfiguracoesOpcoes
from ProjetoPin3.model.GeracaoPlanilha import GeracaoPlanilha

class ControladorLeitorCartao:
    def __init__(self):
        self.visaoLeitorCartaoResposta = None
        self.visaoGeracaoCartaoResposta = None
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
        kaypoints, img_cinza = self.visaoLeitorCartaoResposta.identificandoPontos(img)
        image = self.visaoLeitorCartaoResposta.construcaoFormularioRetangular(kaypoints, img_cinza)
        self.visaoLeitorCartaoResposta.previewConfiguracoes(image)

    def importar_cartao_resposta(self,  arquivo_selecionado):
        self.visaoGeracaoCartaoResposta.atualizar_label(arquivo_selecionado)

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

        self.configuracaoQuestao = ConfiguracaoQuestao(numeroPerguntas, espacamentoPerguntas, margemSuperior, margemLateral, qtdAlunos)
        self.configuracaoResposta = ConfiguracaoQuestao(numeroOpcoes, espacamentoResposta, larguraMarcador, alturaMarcador)


    def actionImportacao(self):
        self.visaoLeitorCartaoResposta.abrirTelaImportacaoCartaoResposta()
