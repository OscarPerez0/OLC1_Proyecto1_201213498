from Compi.Error import Error
from Compi.Token import Token

class AritmeticScanner:

    def __init__(self, data):
        self.text = data + ' '
        self.errores = []
        self.tokens = []


    def scanner(self):
        estado = 0
        lexema = ''
        linea = 1
        columna = 1

        i = 0

        while i < len(self.text):
            if estado == 0:
                lexema = ''
                if self.text[i].isalpha():
                    estado = 1
                    columna += 1
                    lexema += self.text[i]
                elif self.text[i].isdigit():
                    estado = 2
                    columna += 1
                    lexema += self.text[i]
                elif self.simbolos(self.text[i]) != 404:
                    estado = 3
                    columna += 1
                    lexema += self.text[i]
                elif ord(self.text[i]) == 45:
                    estado = 5
                    columna += 1
                    lexema += self.text[i]
                elif 0 <= ord(self.text[i]) <= 32:
                    #tokens que se ignoran
                    columna += 1

                    if ord(self.text[i]) == 10:
                        linea += 1
                        columna = 1

                else:
                    lexema += self.text[i]
                    self.errores.append(Error(lexema, linea, columna, 'Caracter Desconocido', 'Error Lexico'))

            elif estado == 1:
                if self.text[i].isalpha() or self.text[i].isdigit() or ord(self.text[i]) == 95:
                    columna += 1
                    lexema += self.text[i]
                else:
                    estado = 0
                    i -= 1
                    self.tokens.append(Token('tk_id', lexema, linea, columna))

            elif estado == 2:
                if self.text[i].isdigit():
                    estado = 2
                    columna += 1
                    lexema += self.text[i]
                elif ord(self.text[i]) == 46:
                    estado = 4
                    columna += 1
                    lexema += self.text[i]
                else:
                    #aceptacion para enteros
                    estado = 0
                    i -= 1
                    self.tokens.append(Token('tk_numero', lexema, linea, columna))

            elif estado == 3:
                estado = 0
                i -= 1
                self.tokens.append(Token(self.simbolos(lexema), lexema, linea, columna))

            elif estado == 4:
                if self.text[i].sidigit():
                    columna += 1
                    lexema += self.text[i]
                else:
                    #aceptacion para decimales
                    estado = 0
                    self.tokens.append(Token('tk_numero', lexema, linea, columna))

            elif estado == 5:
                if self.text[i].isdigit():
                    estado = 2
                    columna += 1
                    lexema += self.text[i]
                else:
                    #error
                    estado = 0
                    self.errores.append(Error(lexema, linea, columna, 'Error en el patron decimal', 'Error lexico'))

            i += 1



    def simbolos(self, simbol):
        s = {
            '(': 'tk_(',
            ')': 'tk_)',
            '+': 'tk_+',
            '-': 'tk_-',
            '*': 'tk_*',
            '/': 'tk_/'
        }
        return s.get(simbol, 404)
