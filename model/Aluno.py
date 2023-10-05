class Aluno:
    def __init__(self, id):
        self._id = id

    def get_id(self):
        return self._id

    # Setter para o atributo 'id'
    def set_id(self, id):
        self._id = id