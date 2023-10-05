class Questoes:
    def __init__(self, numero, assinaladas):
        self._numero = numero
        self._assinaladas = assinaladas

    def get_numero(self):
        return self._numero

    def set_numero(self, numero):
        self._numero = numero

    def get_assinaladas(self):
        return self._assinaladas

    def set_assinaladas(self, _assinaladas):
        self._assinaladas = _assinaladas