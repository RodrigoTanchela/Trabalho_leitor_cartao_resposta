from ProjetoPin3.model.Configuracoes import Configuracoes

class ConfiguracaoQuestao(Configuracoes):
    def __init__(self, espacamento, numero, margemSuperior, margemLateral, qtdAlunos, posicaoHorizontal, posicaoVertical):
        super().__init__(espacamento, numero)
        self._margemSuperior = margemSuperior
        self._margemLateral = margemLateral
        self._qtdAlunos = qtdAlunos
        self._posicaoHorizontal = posicaoHorizontal
        self._posicaoVertical = posicaoVertical

        # Getter para o atributo 'espacamento'
        def get_margemSuperior(self):
            return self._margemSuperior

        # Setter para o atributo 'margemSuperior'
        def set_margemSuperior(self, margemSuperior):
            self._margemSuperior = margemSuperior

        # Getter para o atributo 'espacamento'
        def get_margemLateral(self):
            return self._margemLateral

        # Setter para o atributo 'margemSuperior'
        def set_margemLateral(self, margemLateral):
            self._margemLateral = margemLateral

            # Getter para o atributo 'espacamento'

        def get_qtdAlunos(self):
            return self._qtdAlunos

        def set_qtdAlunos(self, qtdAlunos):
            self._qtdAlunos = qtdAlunos

        def get_posicaoVertical(self):
            return self._posicaoVertical

        def set_posicaoVertical(self, posicaoVertical):
            self._posicaoVertical = posicaoVertical

        def get_posicaoHorizontal(self):
            return self._posicaoHorizontal

        def set_posicaoHorizontal(self, _posicaoHorizontal):
            self._posicaoHorizontal = posicaoHorizontal