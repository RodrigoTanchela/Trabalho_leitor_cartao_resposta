from ProjetoPin3.model.Configuracoes import Configuracoes

class ConfiguracoesOpcoes(Configuracoes):
    def __init__(self, espacamento, numero, largura, altura):
        super().__init__(espacamento, numero)
        self._largura = largura
        self._altura  = altura

        # Getter para o atributo 'espacamento'
        def get_largura(self):
            return self._largura

        # Setter para o atributo 'largura'
        def set_largura(self, largura):
            self._largura = largura

        # Getter para o atributo 'espacamento'
        def get_altura(self):
            return self._altura

        # Setter para o atributo 'largura'
        def set_altura(self, altura):
            self._altura = altura