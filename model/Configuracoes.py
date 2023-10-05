from abc import ABC, abstractmethod

class Configuracoes(ABC):
    def __init__(self, espacamento, tipo, numero):
        self._espacamento = espacamento
        self._tipo = tipo
        self._numero = numero

    # Getter para o atributo 'espacamento'
    def get_espacamento(self):
        return self._espacamento

    # Setter para o atributo 'espacamento'
    def set_espacamento(self, espacamento):
        self._espacamento = espacamento

    # Getter para o atributo 'tipo'
    def get_tipo(self):
        return self._tipo

    # Setter para o atributo 'tipo'
    def set_tipo(self, novo_tipo):
        self._tipo = novo_tipo

    # Getter para o atributo 'numero'
    def get_numero(self):
        return self._numero

    # Setter para o atributo 'numero'
    def set_numero(self, novo_numero):
        self._numero = novo_numero