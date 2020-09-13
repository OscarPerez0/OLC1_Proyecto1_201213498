from Compi.Token import Token
from Compi.Error import Error


class HtmlScanner:

    def __init__(self, texto):
        self.tokens = []
        self.errores = []
        self.text = texto.lower() + ' '


    def scanner(self):
        lexema = ''
        linea = 1
        columna = 1
        estado = 0

        index = 0

        while index < len(self.text):
            lexema = ''
            estado = 0
            tag = False
            linea = 1
            columna = 1

            if estado == 0:
                lexema = ''

                if self.text[index].isalpha():
                    estado = 1
                    columna += 1
                    lexema += self.text[index]
                elif ord(self.text[index]) == 34:
                    estado = 2
                    columna += 1
                    lexema += self.text[index]



            elif estado == 1:
                if self.text[index].isalpha() or self.text[index].isdigit() or ord(self.text[index]) == 95:
                    columna += 1
                    lexema += self.text[index]
                else:
                    #aceptacion de ids
                    estado = 0
                    index -= 1 #esto se podria quitar?
                    self.tokens.append(Token(self.reservadas(lexema), lexema, linea, columna))

            elif estado == 2:
                if ord(self.text[index]) != 34:
                    if ord(self.text[index]) == 10:
                        self.errores.append(Error(lexema, linea, columna, 'Las cadenas no aceptan saltos de linea', 'Error Lexico'))
                        estado = 0
                        continue

                    lexema += self.text[index]
                    columna += 1
                else:
                    lexema += self.text[index]
                    self.tokens.append(Token('tk_cadena', lexema, linea, columna))
                    estado = 0

            index += 1




    def reservadas(self, word):
        return None


    def simbolos(self, simbol):
        switcher = {

        }

        return switcher.get(simbol, 404)


