
class Error():
    def __init__(self, lexema, linea, columna, descripcion, tipo):
        self.lexema = lexema
        self.linea = linea
        self.columna = columna
        self.descripcion = descripcion
        self.tipo = tipo