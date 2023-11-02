from ProjetoPin3.model.Configuracoes import Configuracoes

class ConfiguracaoQuestao(Configuracoes):
    def __init__(self, espacamento, numero, margemSuperior, margemLateral, qtdAlunos, posicaoHorizontal, posicaoVertical):
        super().__init__(espacamento, numero)
        self._margemSuperior = margemSuperior
        self._margemLateral = margemLateral
        self._qtdAlunos = qtdAlunos

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