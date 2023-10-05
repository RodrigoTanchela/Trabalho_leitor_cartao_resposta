import PySimpleGUI as sg

class TelaLeitorCartao:
    def __init__(self, controlador):
        self.controlador = controlador

        layoutBuscarArquivo = [
            [sg.Text('Caminho',size=(7,0)),sg.Input(size=(51,8), key='arquivo'), sg.Button('Buscar', key='buscar')]
        ]

        layoutNumeroPerguntas = [
            [sg.Text('Perguntas:',size=(7)), sg.Input(size=(7,0), pad=((0, 200), (0, 0)), key='numeroperguntas'), 
            sg.Text('Opções:',size=(7,0),), sg.Input(size=(7,0),  key='numeroopcoes')]
        ]
        
        layoutEspacamentoMarcador = [
            [sg.Text('Largura:',size=(7)), sg.Input(size=(7,0), pad=((0, 200), (0, 0)), key='numeroperguntas'), 
            sg.Text('Altura:',size=(7,0),), sg.Input(size=(7,0),  key='numeroopcoes')]   
        ]

        layoutEspacamentoPerguntas = [
            [sg.Text('Perguntas:',size=(7)), sg.Input(size=(7,0), pad=((0, 200), (0, 0)), key='numeroperguntas'), 
            sg.Text('Respostas:',size=(7,0),), sg.Input(size=(7,0),  key='numeroopcoes')] 
        ]

        layoutTipoMarcadores = [
            [sg.Text('Folha de respostas:',size=(15)), sg.Input(size=(7,0), key='numeroperguntas'), 
            sg.Text('Perguntas:',size=(7,0),), sg.Input(size=(7,0),  key='numeroopcoes'),
            sg.Text('Respostas:',size=(7,0),), sg.Input(size=(7,0),  key='numeroopcoes')] 
        ]

        layoutBotoes = [
            [sg.Button('Preview'), sg.Button('Gerar planilha')]
        ]

        layout = [
            [sg.Frame('', layoutBuscarArquivo, border_width=2, size=(500, 50))],
            [sg.Frame('Número', layoutNumeroPerguntas, border_width=2, size=(500, 50))],
            [sg.Frame('Espaçamento Marcador', layoutEspacamentoMarcador, border_width=2, size=(500, 50))],
            [sg.Frame('Espaçamento Respostas', layoutEspacamentoPerguntas, border_width=2, size=(500, 50))],
            [sg.Frame('Marcadores Respostas', layoutTipoMarcadores, border_width=2, size=(500, 50))],            
            [sg.Frame('', layoutBotoes, border_width=2, size=(500, 50))],
            # [sg.Output(size=(30,20))]
        ]

        # Janela
        self.janela = sg.Window("Dados do Usuário").layout(layout)
        # Extrair os dados da tela
        self.button, self.values = self.janela.Read()
    
    def atualizar_label(self, texto):
        self.janela['arquivo'].update(texto)

    # def Iniciar(self):
    #    print(self.values)
    def Iniciar(self):
        while True:
            evento, valores = self.janela.read()
            if evento == sg.WINDOW_CLOSED:
                break
            elif evento == 'buscar':
                arquivo_selecionado = sg.popup_get_file("Selecione um arquivo")
                if arquivo_selecionado:
                    self.controlador.abrir_explorador_de_arquivos(arquivo_selecionado)


