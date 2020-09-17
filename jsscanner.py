from Token import Token
from Error import Error
from io import StringIO


class JsScanner:
    def __init__(self, data, t):
        self.tktext = t
        self.text = data + ' '
        self.tokens = []
        self.errores = []
        self.out_text = StringIO()
        self.index = -1
        self.er = {}
        self.out_er = {}

        self.expresiones_regulares()

    def expresiones_regulares(self):
        self.er['id'] = '.L*||LN_'
        self.er['entero'] = '+N'
        self.er['decimal'] = '.+N?.p+N' # p representa el . como lexema no como simbolo
        self.er['cadena'] = '.."*C"'
        self.er['cadena_s'] = "..'*C'"
        self.er['comentario_m'] = '..../@*C@/' # @ representa el * como lexema no como simbolo
        self.er['comentario_s'] = '..//*C'

    def add_er(self, er):
        if not er in self.out_er:
            self.out_er[er] = self.er[er]


    def scanner(self):
        estado = 0
        lexema = ""
        linea = 1
        columna = 1

        length = len(self.text)
        index = 0
        found_error = False
        index_auxiliar = 0
        aux_text = self.text
        self.text = self.text.lower()



        while(index < length):
            if estado == 0:
                lexema = ""
                found_error = False
                if self.text[index].isalpha(): #Identificador
                    estado = 1
                    lexema+= self.text[index]
                    columna+= 1
                    start_i = index
                elif ord(self.text[index]) == 47: #Comentarios
                    estado = 2
                    lexema+= self.text[index]
                    columna+= 1
                elif ord(self.text[index]) == 34: #Cadena
                    estado = 3
                    lexema += self.text[index]
                    columna += 1
                elif ord(self.text[index]) == 39: # ' char
                    estado = 4
                    lexema += self.text[index]
                    columna += 1
                elif self.text[index].isdigit():
                    estado = 5
                    lexema += self.text[index]
                    columna += 1
                elif self.simbols(self.text[index]) != 404:
                    estado = 6
                    lexema += self.text[index]
                    columna += 1
                elif ord(self.text[index]) >= 0 and ord(self.text[index]) <= 32:
                    #ignore all
                    columna += 1

                    if ord(self.text[index]) == 10:
                        linea += 1
                        columna = 1

                else:
                    #lexical error
                    lexema+= self.text[index]
                    columna += 1
                    self.errores.append(Error(lexema, linea, columna, 'Caracter no reconocido', 'Error Lexico'))
                    found_error = True

            elif estado == 1:
                if self.text[index].isalpha() or self.text[index].isdigit() or ord(self.text[index]) == 95:
                    lexema += self.text[index]
                    columna += 1
                else:
                    #aceptacion para los identificadores y palabras reservadas
                    estado = 0
                    index -= 1
                    self.tokens.append(Token(self.reservadas(lexema), lexema, linea, columna))
                    self.add_er('id')

                    # self.tktext.tag_add("test", start_i, columna)
                    # self.tktext.tag_config("test", background="red")


            elif estado == 2: #comentarios
                lexema += self.text[index]
                columna += 1

                if ord(self.text[index]) == 47:
                    estado = 7
                elif ord(self.text[index]) == 42:
                    estado = 8
                else:
                    #simbolo de division
                    self.tokens.append(Token('tk_/', lexema, linea, columna))
                    estado = 0

            elif estado == 3:

                if ord(self.text[index]) != 34:
                    if ord(self.text[index]) == 10:
                        self.errores.append(Error(lexema, linea, columna, 'Las cadenas no aceptan saltos de linea', 'Error Lexico'))
                        found_error = True
                        estado = 0
                        self.out_text += aux_text[index]
                        continue

                    lexema += self.text[index]
                    columna += 1
                else:
                    lexema += self.text[index]
                    self.tokens.append(Token('tk_cadena', lexema, linea, columna))
                    self.add_er('cadena')
                    estado = 0

            elif estado == 4:
                if ord(self.text[index]) != 39:
                    if ord(self.text[index]) == 10:
                        self.errores.append(Error(lexema, linea, columna, 'Las cadenas no aceptan saltos de linea ', 'Error Lexico'))
                        found_error = True
                        estado = 0
                        self.out_text += aux_text[index]
                        continue

                    lexema += self.text[index]
                    columna += 1
                else:
                    lexema += self.text[index]
                    self.tokens.append(Token('tk_cadena_s', lexema, linea, columna))
                    self.add_er('cadena_s')
                    estado = 0

            elif estado == 5:
                if self.text[index].isdigit():
                    lexema += self.text[index]
                    columna += 1
                elif ord(self.text[index]) == 46:
                    estado = 12
                    lexema += self.text[index]
                    columna += 1
                else:
                    #aceptacion numeros
                    estado = 0
                    index -= 1
                    self.tokens.append(Token('tk_entero', lexema, linea, columna))
                    self.add_er('entero')

            elif estado == 6:
                if ord(lexema[0]) == 61:
                    if ord(self.text[index]) == 61:
                        lexema += self.text[index]
                        columna += 1
                        self.tokens.append(Token('tk_comparar',lexema, linea, columna))
                    else:
                        # index -= 1
                        self.tokens.append(Token('tk_igual', lexema, linea, columna))
                    estado = 0

                elif ord(lexema[0]) == 33:
                    if ord(self.text[index]) == 61:
                        lexema += self.text[index]
                        columna += 1
                        self.tokens.append(Token('tk_diferente', lexema, linea, columna))
                    else:
                        # index -= 1
                        self.tokens.append(Token('tk_negacion', lexema, linea, columna))

                    estado = 0

                elif ord(lexema[0]) == 60:
                    if ord(self.text[index]) == 61:
                        lexema += self.text[index]
                        columna += 1
                        self.tokens.append(Token('tk_menorI', lexema, linea, columna))
                    else:
                        # index -= 1
                        self.tokens.append(Token('tk_menor', lexema, linea, columna))

                    estado = 0

                elif ord(lexema[0]) == 62:
                    if ord(self.text[index]) == 61:
                        lexema += self.text[index]
                        columna += 1
                        self.tokens.append(Token('tk_mayorI', lexema, linea, columna))
                    else:
                        # index -= 1
                        self.tokens.append(Token('tk_mayor', lexema, linea, columna))

                    estado = 0

                elif ord(lexema[0]) == 38:
                    if ord(self.text[index]) == 38:
                        lexema += self.text[index]
                        columna += 1
                        self.tokens.append(Token('tk_and', lexema, linea, columna))
                    else:
                        #error lexico
                        self.errores.append(Error(lexema, linea, columna, 'Patron no reconocido', 'Error lexico'))
                        found_error = True


                    estado = 0

                elif ord(lexema[0]) == 124:
                    if ord(self.text[index]) == 124:
                        lexema += self.text[index]
                        columna += 1
                        self.tokens.append(Token('tk_or',lexema, linea, columna))
                    else:
                        #Error
                        self.errores.append(Error(lexema, linea, columna, 'Patron no reconocido', 'Error lexico'))
                        found_error = True

                    estado = 0

                else:
                    estado = 0
                    # index -= 1
                    self.tokens.append(Token(self.simbols(lexema), lexema, linea, columna))

                continue

            elif estado == 7:
                #comentario path
                if ord(self.text[index]) != 10:
                    lexema += self.text[index]
                    columna += 1
                else:
                    estado = 0
                    # index -= 1
                    self.tokens.append(Token('tk_comentario_s', lexema,linea, columna))
                    self.add_er('comentario_s')
                    linea += 1
                    columna = 1

            elif estado == 8:
                if ord(self.text[index]) == 42:
                    estado = 9

                lexema += self.text[index]
                columna += 1

                if ord(self.text[index]) == 10:
                    linea += 1
                    columna = 1

            elif estado == 9:
                if ord(self.text[index]) == 47:
                    lexema += self.text[index]
                    columna += 1
                    estado = 14

                else:
                    # print(self.text[index])
                    lexema += self.text[index]
                    estado = 8

            elif estado == 10:
                if ord(self.text[index]) == 39:
                    estado = 11
                    lexema += self.text[index]
                    columna += 1
                else:
                    self.errores.append(Error(lexema, linea, columna, 'No puede contener mas de un caracter', 'Error Lexico'))
                    estado = 0
                    found_error = True

            elif estado == 11:
                #estado de aceptacion para caracteres
                # index -= 1
                estado = 0
                self.tokens.append(Token('tk_cadena_s', lexema, linea, columna))
                self.add_er('cadena_s')
                continue

            elif estado == 12:
                if self.text[index].isdigit():
                    estado = 13
                    lexema += self.text[index]
                    columna += 1
                else:
                    estado = 0
                    lexema += self.text[index]
                    self.errores.append(Error(lexema, linea, columna, 'Patron decimal incorrecto', 'Error lexico'))
                    found_error = True

            elif estado == 13:
                if self.text[index].isdigit():
                    lexema += self.text[index]
                    columna += 1
                else:
                    estado = 0
                    # index -= 1
                    self.tokens.append(Token('tk_decimal', lexema, linea, columna))
                    self.add_er('decimal')
                    continue

            elif estado == 14:
                index -= 1
                estado = 0
                self.tokens.append(Token('tk_comentario_m', lexema, linea, columna))
                self.add_er('comentario_m')


            if not found_error and index_auxiliar == index:
                self.out_text.write(aux_text[index_auxiliar])
            else:
                index_auxiliar = index



            # print(self.out_text.getvalue())

            index += 1

            if index_auxiliar + 1 < len(self.text):
                index_auxiliar += 1

    def find_path(self):
        if len(self.tokens) == 0:
            return

        print('looking path')

        token = self.next_token()
        comment = ''
        index = 0
        estado = 0
        temp = ''
        while token != 404:

            if token.token == 'tk_comentario_s' or 'tk_comentario_m':
                comment = token.lexema

            while index < len(comment):
                if estado == 0:
                    if comment[index].isalpha():
                        temp += comment[index]
                    else:
                        if temp == 'pathl':
                            estado = 1
                            index -= 1
                            # if ord(comment[index]) == 32:


                        temp = ''

                elif estado == 1:
                    if ord(comment[index]) == 58 or ord(comment[index]) == 61:
                        estado = 3

                    elif ord(comment[index]) == 45:
                        estado = 2

                elif estado == 2:
                    if ord(comment[index]) == 62:
                        estado = 3
                    else:
                        estado = 3


                elif estado == 3:
                    if 0 <= ord(comment[index]) <= 32:
                        index += 1
                        continue
                        
                    if ord(comment[index]) == 47 or comment[index].isdigit() or comment[index].isalpha():
                        temp += comment[index]
                    else:
                        if ord(temp[len(temp) -1]) != 47:
                            temp += '/'
                        return temp

                index += 1


            token = self.next_token()


        print('exit while')
        return None


    def next_token(self):
        self.index += 1
        if self.index < len(self.tokens):
            return self.tokens[self.index]
        else:
            return 404



    def reservadas(self, index):
        switcher =  {
            'var': 'tk_var',
            'if': 'tk_if',
            'else': 'tk_else',
            'console': 'tk_console',
            'log': 'tk_log',
            'for': 'tk_for',
            'do': 'tk_do',
            'while': 'tk_while',
            'return': 'tk_return',
            "continue": 'tk_continue',
            'break': 'tk_break',
            'function': 'tk_function',
            'constructor': 'tk_constructor',
            'class': 'tk_class',
            'this': 'tk_this',
            'math': 'tk_math',
            'pow': 'tk_pow'
        }

        return switcher.get(index, 'tk_identificador')


    def simbols(self, index):
        switcher = {
            '(': 'tk_(',
            ')': 'tk_)',
            '{': 'tk_{',
            '}': 'tk_}',
            '.': 'tk_.',
            ';': 'tk_;',
            ',': 'tk_,',
            ':': 'tk_:',
            '+': 'tk_+',
            '-': 'tk_-',
            '*': 'tk_*',
            # '/': 'tk_/',
            '=': 'tk_=',
            '!': 'tk_!',
            '>': 'tk_>',
            '<': 'tk_<',
            '|': 'tk_|',
            '&': 'tk_&'
        }

        return switcher.get(index, 404)