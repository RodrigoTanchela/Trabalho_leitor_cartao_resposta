import PySimpleGUI as sg
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
        self.janela = sg.Window("Dados do Usuário").layout(layout)
        self.button, self.values = self.janela.Read()

    def setVisible(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == 'Mostrar Segunda View':
                self.mostrar_segunda_view()
        self.window.close()

    def atualizar_label(self, texto):
        self.janela['arquivo'].update(texto)