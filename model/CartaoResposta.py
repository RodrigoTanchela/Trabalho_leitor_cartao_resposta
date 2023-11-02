class CartaoResposta:
    
    def __init__(self, identificador, aluno, questao) :
        self._identificador = identificador
        self._aluno = aluno
        self._questao = questao


    def get_identificador(self):
        return self._identificador

    def set_identificador(self, identificador):
        self._identificador = identificador
    
    def get_aluno(self):
        return self._aluno

    def set_aluno(self, aluno):
        self._aluno = aluno
    
    def get_questao(self):
        return self.questao

    def set_questao(self, questao):
        self.questao = questao
