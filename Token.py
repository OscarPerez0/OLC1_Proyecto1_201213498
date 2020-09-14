
class Token:
    def __init__(self, token, lexema, linea, columna):
        self.token = token
        self.lexema = lexema
        self.linea = linea
        self.columna = columna


    def print(self):
        print(self.token + ' ' + self.lexema)
