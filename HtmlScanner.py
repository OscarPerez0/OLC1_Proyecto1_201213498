from Token import Token
from Error import Error


class HtmlScanner:

    def __init__(self, texto):
        self.tokens = []
        self.errores = []
        self.text = texto.lower() + ' '
        self.out_text = ''
        self.index = -1

    def scanner(self):
        lexema = ''
        linea = 1
        columna = 1
        estado = 0
        index = 0
        fake_index = 0
        tag = False
        found_error = False

        while index < len(self.text):
            if estado == 0:
                lexema = ''
                found_error = False
                if self.text[index].isalpha():
                    estado = 1
                    columna += 1
                    lexema += self.text[index]
                elif ord(self.text[index]) == 34:
                    estado = 2
                    columna += 1
                    lexema += self.text[index]
                elif self.text[index].isdigit():
                    estado = 3
                    columna += 1
                    lexema += self.text[index]
                elif self.simbolos(self.text[index]) != 404:
                    estado = 4
                    columna += 1
                    lexema += self.text[index]
                elif 0 <= ord(self.text[index]) <= 32:
                    columna += 1

                    if ord(self.text[index]) == 10:
                        linea += 1
                        columna = 1

                else:
                    if tag:
                        lexema += self.text[index]
                        self.errores.append(Error(lexema, linea, columna, 'Caracter invalido', 'error lexico'))
                        found_error = True
                    else:
                        lexema += self.text[index]
                        self.tokens.append(Token('tk_texto', lexema, linea, columna))



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
                        found_error = True
                        continue

                    lexema += self.text[index]
                    columna += 1
                else:
                    lexema += self.text[index]
                    self.tokens.append(Token('tk_cadena', lexema, linea, columna))
                    estado = 0

            elif estado == 3:
                if self.text[index].isdigit():
                    columna += 1
                    lexema += self.text[index]
                elif ord(self.text[index]) == 46:
                    estado = 5
                    columna += 1
                    lexema += self.text[index]
                else:
                    estado = 0
                    index -= 1
                    self.tokens.append(Token('tk_entero', lexema, linea, columna))

            elif estado == 4:
                comment = False

                if ord(lexema) == 60:
                    if ord(self.text[index]) == 33:
                        estado = 6
                        columna += 1
                        lexema += self.text[index]
                        comment = True
                    else:
                        tag = True
                elif ord(lexema) == 62:
                    tag = False


                if not comment:
                    estado = 0
                    index -= 1
                    self.tokens.append(Token(self.simbolos(lexema), lexema, linea, columna))

            elif estado == 5:
                if self.text[index].isdigit():
                    columna += 1
                    lexema += self.text[index]
                else:
                    estado = 0
                    index -= 1
                    self.tokens.append(Token('tk_decimal', lexema, linea, columna))

            elif estado == 6:
                if ord(self.text[index]) == 45:
                    estado = 7
                    columna += 1
                    lexema += self.text[index]
                else:
                    estado = 0
                    self.errores.append(Error(lexema, linea, columna, 'Patron Comentario invalido', 'Error lexico'))
                    found_error = True
            elif estado == 7:
                if ord(self.text[index]) == 45:
                    estado = 8
                    columna += 1
                    lexema += self.text[index]
                else:
                    estado = 0
                    self.errores.append(Error(lexema, linea, columna, 'Patron Comentario invalido', 'Error lexico'))
                    found_error = True
            elif estado == 8:
                if ord(self.text[index]) == 45:
                    estado = 9

                columna += 1
                lexema += self.text[index]

                if ord(self.text[index]) == 10:
                    linea += 1
                    columna = 1

            elif estado == 9:
                if ord(self.text[index]) == 45:
                    estado = 10
                    columna += 1
                    lexema += self.text[index]
                else:
                    estado = 8
                    index -= 1

            elif estado == 10:
                if ord(self.text[index]) == 62:
                    estado = 11
                    columna += 1
                    lexema += self.text[index]
                else:
                    estado = 8
                    index -= 1

            elif estado == 11:
                estado = 0
                index -= 1
                self.tokens.append(Token('tk_comentario', lexema, linea, columna))

            if not found_error and fake_index == index:
                self.out_text += self.text[index]
            else:
                fake_index = index


            index += 1

            if fake_index + 1 < len(self.text):
                fake_index += 1



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
                    print(self.text[index])
                    if ord(comment[index]) == 58 or ord(comment[index]) == 61:
                        estado = 3

                    elif ord(comment[index]) == 45:
                        estado = 2

                elif estado == 2:
                    print(comment[index])
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
                        print(temp)

                        if temp[len(temp) - 1] != '/':
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

    def reservadas(self, word):
        s = {
            'html': 'r_html',
            'head': 'r_head',
            'title': 'r_title',
            'body': 'r_body',
            'h1': 'r_h1',
            'h2': 'r_h2',
            'h3': 'r_h3',
            'h4': 'r_h4',
            'h5': 'r_h5',
            'h6': 'r_h6',
            'p': 'r_p',
            'img': 'r_img',
            'src': 'r_src',
            'a': 'r_a',
            'href': 'r_href',
            'ul': 'r_ul',
            'ol': 'r_ol',
            'li': 'r_li',
            'style': 'r_style',
            'table': 'r_table',
            'th': 'r_th',
            'tr': 'r_tr',
            'border': 'r_border',
            'td': 'r_td',
            'caption': 'r_caption',
            'colgroup': 'r_colgroup',
            'col': 'r_col',
            'thead': 'r_thead',
            'tbody': 'r_tbody',
            'tfoot': 'r_tfoot'
        }

        return s.get(word, 'tk_id')


    def simbolos(self, simbol):
        switcher = {
            '<': 'tk_<',
            '>': 'tk_>',
            '/': 'tk_/',
            '.': 'tk_.',
            ':': 'tk_:',
            ';': 'tk_;',
            '=': 'tk_='
        }

        return switcher.get(simbol, 404)


