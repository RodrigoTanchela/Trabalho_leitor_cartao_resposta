import PySimpleGUI as sg
from ProjetoPin3.model.Aluno import Aluno
from ProjetoPin3.model.CartaoResposta import CartaoResposta
from ProjetoPin3.model.ConfiguracaoQuestao import ConfiguracaoQuestao
from ProjetoPin3.model.ConfiguracaoOpcoes import ConfiguracoesOpcoes
from ProjetoPin3.model.GeracaoPlanilha import GeracaoPlanilha

class ControladorLeitorCartao:
    def __init__(self):
        self.visao = None
        self.aluno = None
        self.cartaoResposta = None
        self.configuracaoOpcoes = None
        self.configuracaoQuestao = None
        self.geracaoPlanilha = None
        self.questoes = None

    def abrir_explorador_de_arquivos(self, arquivo_selecionado):
        # self.modelo.arquivo_selecionado = arquivo_selecionado
        self.visao.atualizar_label(arquivo_selecionado)
