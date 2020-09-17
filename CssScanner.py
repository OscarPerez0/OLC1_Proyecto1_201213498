from Token import Token
from Error import Error
from io import StringIO


class CssScanner:

    def __init__(self, texto, bitacora):
        self.tokens = []
        self.errores = []
        self.text = texto + ' '
        self.bitacora = bitacora
        self.out_text = StringIO()
        self.index = -1

    def scanner(self):
        lexema = ''
        estado = 0
        linea = 1
        columna = 1
        found_error = False
        aux_text = self.text
        self.text = self.text.lower()

        index = 0
        index_auxiliar = 0
        while index < len(self.text):
            if estado == 0:
                lexema = ''
                found_error = False
                self.bitacora.insert('end-1c', 'Estado 0\n')
                if self.text[index].isalpha():
                    estado = 1
                    columna += 1
                    lexema += self.text[index]
                    self.bitacora.insert('end-1c', 'Reconociendo ID / Reservada ===> Estado 1 \n')
                elif self.text[index].isdigit():
                    estado = 2
                    columna += 1
                    lexema += self.text[index]
                    self.bitacora.insert('end-1c', 'Reconociendo Enteros / Decimales ===> Estado 2 \n')
                elif ord(self.text[index]) == 34:
                    estado = 5
                    columna += 1
                    lexema += self.text[index]
                    self.bitacora.insert('end-1c', 'Reconociendo Cadenas ===> Estado 5 \n')
                elif ord(self.text[index]) == 39:
                    estado = 6
                    columna += 1
                    lexema += self.text[index]
                    self.bitacora.insert('end-1c', 'Reconociendo Cadenas ===> Estado 6 \n')
                elif ord(self.text[index]) == 47:
                    estado = 7
                    lexema += self.text[index]
                    columna += 1
                    self.bitacora.insert('end-1c', 'Reconociendo Comentarios ===> Estado 7 \n')
                elif self.simbolos(self.text[index]) != 404:
                    estado = 11
                    lexema += self.text[index]
                    columna += 1
                    self.bitacora.insert('end-1c', 'Reconociendo Simbolos ===> Estado 11 \n')
                elif 0 <= ord(self.text[index]) <= 32:
                    # se ignora
                    columna += 1

                    if ord(self.text[index]) == 10:
                        linea += 1
                        columna = 1

                    self.bitacora.insert('end-1c', 'Ignorando Caracteres \n ')

                else:
                    lexema += self.text[index]
                    self.errores.append(Error(lexema, linea, columna, 'Caracter desconocido', 'error lexico'))
                    self.bitacora.insert('end-1c', 'Error lexico encontrado. Caracter Desconocido: ' + lexema + '\n')
                    found_error = True



            elif estado == 1:  #ids
                if self.text[index].isalpha() or self.text[index].isdigit() or ord(self.text[index]) == 95 or ord(self.text[index]) == 45:
                    columna += 1
                    lexema += self.text[index]
                else:
                    #comprobar si son palabras reservadas o no
                    estado = 0
                    index -= 1
                    self.tokens.append(Token(self.reservadas(lexema), lexema, linea, columna))
                    self.bitacora.insert('end-1c', 'Estado 1.  Aceptando Id/Reservada.' + lexema + ' Estado ====> 0 \n')

            elif estado == 2: #numeros
                if self.text[index].isdigit():
                    columna += 1
                    lexema += self.text[index]
                    self.bitacora.insert('end-1c', 'Estado 2. Reconociendo Enteros\n')
                elif ord(self.text[index]) == 46:
                    estado = 3
                    lexema += self.text[index]
                    columna += 1
                    self.bitacora.insert('end-1c', 'Estado 2. Detectado un ".". Estado ====> 3')
                else:
                    #aceptacion de enteros
                    estado = 0
                    index -= 1
                    self.tokens.append(Token('tk_entero', lexema, linea, columna))
                    self.bitacora.insert('end-1c', ' Estado 2. Aceptando Entero: ' + str(lexema) + ' Estado ====> 0\n')


            elif estado == 3: #decimales
                if self.text[index].isdigit():
                    columna += 1
                    lexema += self.text[index]
                    estado = 4
                    self.bitacora.insert('end-1c', 'Estado 3. Reconociendo Decimales. Estado ====> 4 \n')
                else:
                    estado = 0
                    lexema += self.text[index]
                    self.errores.append(Error(lexema, linea, columna, 'patron decimal incorrecto', 'error lexico'))
                    self.bitacora.insert('end-1c', 'Esteado 3. Error en el patron Decimal. Estado ====> 0 \n')
                    found_error = True
            elif estado == 4:
                if self.text[index].isdigit():
                    columna += 1
                    lexema += self.text[index]
                else:
                    estado = 0
                    self.tokens.append(Token('tk_decimal', lexema, linea, columna))

            elif estado == 5:
                if ord(self.text[index]) != 34:
                    if ord(self.text[index]) == 10:
                        self.errores.append(Error(lexema, linea, columna, 'Las cadenas no aceptan saltos de linea', 'Error Lexico'))
                        found_error = True
                        estado = 0
                        continue

                    lexema += self.text[index]
                    columna += 1
                else:
                    lexema += self.text[index]
                    self.tokens.append(Token('tk_cadena', lexema, linea, columna))
                    estado = 0
                    self.bitacora.insert('end-1c', "Estado 5 Aceptacion Cadenas con comillas simples '. Estado ====> 0 \n")

            elif estado == 6:
                if ord(self.text[index]) != 39:
                    if ord(self.text[index]) == 10:
                        self.errores.append(Error(lexema, linea, columna, 'Las cadenas no aceptan saltos de linea', 'error lexico'))
                        self.bitacora.insert('end-1c', 'Error en Estado 6. Las cadenas no aceptan saltos de linea. Estado ====> 0')
                        found_error = True
                        estado = 0
                        continue

                    lexema += self.text[index]
                    columna += 1
                    self.bitacora.insert('end-1c', 'Estasdo 6. Reconociendo Cadenas ====> Estado 6 \n')
                else:
                    lexema += self.text[index]
                    self.tokens.append(Token('tk_cadena_s', lexema, linea, columna))
                    estado = 0
                    self.bitacora.insert('end-1c', 'Estado 6 Aceptacion Cadenas. Estado ====> 0 \n')

            elif estado == 7:
                if ord(self.text[index]) == 42:
                    estado = 8
                    lexema += self.text[index]
                    columna += 1
                    self.bitacora.insert('end-1c', 'Reconociendo Comentarios ====> Estado 8 \n')
                else:
                    estado = 0
                    self.errores.append(Error(lexema, linea, columna, 'error en patron comentario', 'error lexico'))
                    self.bitacora.insert('end-1c', 'Estado 7 Error en el patron Comentario. Estado ====> 0 \n')
                    found_error = True

            elif estado == 8:
                if ord(self.text[index]) == 42:
                    estado = 9

                lexema += self.text[index]
                columna += 1

                if ord(self.text[index]) == 10:
                    linea += 1
                    columna = 1

                self.bitacora.insert('end-1c', 'Reconociendo Comentarios ====> Estado 9 \n')

            elif estado == 9:
                if ord(self.text[index]) == 47:
                    lexema += self.text[index]
                    columna += 1
                    estado = 10
                    self.bitacora.insert('end-1c', 'Reconociendo Comentarios ====> Estado 10 \n')
                else:
                    index -= 1
                    estado = 8
                    self.bitacora.insert('end-1c', 'Regresando al estado 8' + '\n')

            elif estado == 10:
                index -= 1
                estado = 0
                self.tokens.append(Token('tk_comentario', lexema, linea, columna))
                self.bitacora.insert('end-1c', ' Estado de Aceptacion Comentario: ' + lexema + '\n')

            elif estado == 11:
                estado = 0
                index -= 1
                self.tokens.append(Token(self.simbolos(lexema), lexema, linea, columna))
                self.bitacora.insert('end-1c', ' Estado de Aceptacion Simbolo: ' + lexema + '\n')


            if not found_error and index_auxiliar == index:
                self.out_text.write(aux_text[index])
            else:
                index_auxiliar = index


            index += 1

            if index_auxiliar + 1 < len(self.text):
                index_auxiliar += 1

        print(self.out_text.getvalue())

    def find_path(self):
        if len(self.tokens) == 0:
            return

        token = self.next_token()
        comment = ''
        index = 0
        estado = 0
        temp = ''
        while token != 404:

            if token.token == 'tk_comentario':
                comment = token.lexema

            while index < len(comment):
                if estado == 0:
                    if comment[index].isalpha():
                        temp += comment[index]
                    else:
                        if temp == 'pathl':
                            estado = 1
                            index -= 1

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
                        if ord(temp[len(temp) -1 ]) != 47:
                            temp += '/'
                        return temp

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

    def simbolos(self, simbol):
        s = {
            '{': 'tk_{',
            '}': 'tk_}',
            ':': 'tk_:',
            ';': 'tk_;',
            '-': 'tk_-',
            '*': 'tk_*',
            ',': 'tk_,',
            '#': 'tk_#',
            '.': 'tk_.',
            '%': 'tk_%',
            '(': 'tk_(',
            ')': 'tk_)'
        }

        return s.get(simbol, 404)


    def reservadas(self, word):
        switch = {
            'color': 'r_color',
            'border': 'r_border',
            'text-align': 'r_text-align',
            'font-wight': 'r_font-wight',
            'padding-left': 'r_font-wight',
            'padding-top': 'r_padding-top',
            'line-height': 'r_line-height',
            'margin-top': 'r_margin-top',
            'margin-left': 'r_margin-left',
            'display': 'r_display',
            'top':  'r_top',
            'float': 'r_float',
            'min-width': 'r_min-width',
            'background-color': 'r_background-color',
            'opacity': 'r_opacity',
            'font-family': 'r_font-family',
            'font-size': 'r_font-size',
            'padding-right': 'r_padding-right',
            'padding': 'r_padding',
            'width': 'r_width',
            'margin-right': 'r_margin-right',
            'margin': 'r_margin',
            'position': 'r_position',
            'right': 'r_right',
            'clear': 'r_clear',
            'max-height': 'r_max-height',
            'background-image': 'r_background-image',
            'background': 'r_background',
            'font-style': 'r_font-style',
            'font': 'r_font',
            'padding-bottom': 'r_padding-bottom',
            'height': 'r_height',
            'margin-bottomo': 'r_margin-bottom',
            'border-style': 'r_border-style',
            'bottom': 'r_bottom',
            'left': 'r_left',
            'max-width': 'r_max-width',
            'min-height': 'r_min-height',
            'px': 'r_px',
            'em': 'r_em',
            'vh': 'r_vh',
            'vw': 'r_vw',
            'in': 'r_in',
            'cm': 'r_cm',
            'mm': 'r_mm',
            'pt': 'r_pt',
            'pc': 'r_pc',
            'url': 'r_url',
            'inline-block': 'r_inline-block',
            'relative': 'r_relative',
            'absolute': 'r_absolute',
            'rgba': 'r_rgba'
        }

        return switch.get(word, 'tk_id')