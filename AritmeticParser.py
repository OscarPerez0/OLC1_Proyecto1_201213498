from Tabla import Tabla
from stack import Stack

class AritmeticParser:

    def __init__(self, tokens):
        self.tabla = Tabla()
        self.tokens = tokens
        self.pila = Stack()
        self.raiz = Nodo('s')
        self.ctoken = -1
        self.have_error = False
        self.out = {}



    def parse(self):
        self.pila.push('$')
        self.pila.push(self.raiz)
        self.pila.push('s')

        ntemp = None
        # temp = None

        token = self.__next_token()

        des_error = ''

        while True:
            temp = self.pila.peek()

            if self.__is_terminal(temp) or temp == '$':

                if temp == token:
                    self.pila.pop()
                    token = self.__next_token()

                else:
                    des_error = 'Se esperaba el Token' + str(temp) + ' Y se recibio: ' + token
                    self.have_error = True
                    break
            else:
                p = self.tabla.buscar_produccion(temp, token)
                if p != None:
                    self.pila.pop()
                    ntemp = self.pila.pop()

                    if len(p) == 0:
                        ntemp = None
                        continue

                    self.__create_nodes(p, ntemp)
                    self.__push_productions(p, ntemp, len(ntemp.hijos) - 1)

                else:
                    self.have_error = True
                    des_error += 'Se esperaba alguno de los siguientes tokens: ' + str(list(self.tabla.get_production_of(temp))) + ' Y se recibio: ' + token
                    des_error = '' #limpio la variable temporal
                    break

            if temp == '$':
                break

        if not self.have_error:
            print('Analisis sintactico terminado con exito')
        else:
            print('expresion aritmetica incorrecta')
            print(self.out)


    def get_out(self):
        expresion = ''
        estado = ''

        for token in self.tokens:
            expresion += token.lexema


        if self.have_error:
            estado += 'Incorrecto'
        else:
            estado += 'Correcto'


        return (expresion, estado)


    def __registrar_error(self, op, desc, error):
        self.out[op] = {'Estado': error, 'Descripcion': desc}

    def __panic_mode(self, token, temp, exp):

        while token != 'tk_del' and token != '$':
            print('Token consumido: ' + token)
            exp += self.tokens[self.ctoken].lexema
            token = self.__next_token()

        exp = '' #esto funcionara?

        while temp != 'tk_del' and self.pila.peek() != '$':
            temp = self.pila.pop()
            print('Token desapilado: ' + str(temp))


        token = self.__next_token()

    def __create_nodes(self, p, ntemp):
        index = 0
        while index < len(p):
            if not self.__is_terminal(p[index]):
                ntemp.hijos.append(Nodo(p[index]))

            index += 1

    def __push_productions(self, p, ntemp, ntemp_count):
        index = len(p) - 1
        while index >= 0:
            if self.__is_terminal(p[index]):
                self.pila.push(p[index])
            else:
                if ntemp_count == -1:
                    index -= 1
                    continue
                #estoy seguro de que siempre encontrare elementos
                self.pila.push(ntemp.hijos[ntemp_count])
                self.pila.push(p[index])
                ntemp_count -= 1

            index -= 1



    def __next_token(self):
        self.ctoken += 1
        retorno = ''

        if self.ctoken <= len(self.tokens) - 1:
            retorno = self.tokens[self.ctoken].token
            while retorno == 'tk_comentario_m' or retorno == 'tk_comentario_s':
                self.ctoken += 1
                retorno = self.tokens[self.ctoken].token

        return retorno


    def __is_terminal(self, temporal):
        aux = str(temporal)
        if 'tk_' in aux:
            return True
        else:
            return False

    def __match_terminal(self, keyword):
        t = ('tk_+', 'tk_-', 'tk_*', 'tk_/', 'tk_(', 'tk_)', 'tk_entero', 'tk_decimal', 'tk_id')

        if keyword in t:
            return True
        else:
            return False






class Nodo:

    def __init__(self, etiqueta=None, nombre=None, valor=None, tipo=None, hijos=[]):
        self.etiqueta = etiqueta
        self.nombre = nombre
        self.valor = valor
        self.tipo = tipo
        self.hijos = hijos





