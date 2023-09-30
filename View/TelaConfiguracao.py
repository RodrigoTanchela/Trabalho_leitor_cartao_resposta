import PySimpleGUI as sg

class TelaConfiguracao:
    def __init__(self):

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

        layout = [
            [sg.Text('Buscar Arquivo',size=(7,0)),sg.Input(size=(51,8), key='caminho')],
            [sg.Frame('Número', layoutNumeroPerguntas, border_width=2, size=(500, 50))],
            [sg.Frame('Espaçamento Marcador', layoutEspacamentoMarcador, border_width=2, size=(500, 50))],
            [sg.Frame('Espaçamento Respostas', layoutEspacamentoPerguntas, border_width=2, size=(500, 50))],
            [sg.Frame('Marcadores Respostas', layoutTipoMarcadores, border_width=2, size=(500, 50))],            
            [sg.Button('Salvar os dados')],
            # [sg.Output(size=(30,20))]
        ]

        # Janela
        self.janela = sg.Window("Dados do Usuário").layout(layout)
        # Extrair os dados da tela
        self.button, self.values = self.janela.Read()
    def Iniciar(self):
       print(self.values)

tela = TelaConfiguracao()
tela.Iniciar()