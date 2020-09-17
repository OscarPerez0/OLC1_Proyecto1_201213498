
class Nodo:
    def __init__(self):
        self.indice = -1
        self.valor = None
        self.hijos = None
        self.anulable = False


    def set_id(self, id):
        self.id = id

    def set_valor(self, valor):
        self.valor = valor

    def create_hijos(self):
        self.hijos = []

    def agregar_hijo(self, valor):
        self.hijos.append(valor)

    def hijos_null(self):
        if self.hijos == None:
            return True
        return False
