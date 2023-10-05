import PySimpleGUI as sg

class ControladorLeitorCartao():
    def __init__(self):
        pass

    def abrir_explorador_de_arquivos(self):
        arquivo_selecionado = sg.popup_get_file("Selecione um arquivo")
        if arquivo_selecionado:
            self.modelo.arquivo_selecionado = arquivo_selecionado
            self.visao.atualizar_label(arquivo_selecionado)
