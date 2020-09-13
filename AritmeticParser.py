from Compi.stack import Stack

class AritmeticParse:

    def __init__(self, tokens):
        self.tokens = tokens
        self.precedence = []
        self.set_precedences()
    # () precendencia 2
    # / * precedencia 1
    # + - precedencia 0

    def set_precedences(self):
        self.precedence.append(('tk_(', 2))
        self.precedence.append(('tk_)', 2))

        self.precedence.append(('tk_*', 1))
        self.precedence.append(('tk_/', 1))

        self.precedence.append(('tk_+', 0))
        self.precedence.append(('tk_-', 0))

    # misma precedencia -> se cambia
    # mayor precedencia -> se agrega a la pila
    # menor precedencia -> saca operadores

    # parentesis derecho -> vacia la pila

    def parser(self):

        print('analizando expresion aritmetica')

        stack = Stack()
        list = []

        for token in self.tokens:
            # print('iterando: ' + token.lexema)
            if token.token != 'tk_id' and token.token != 'tk_numero':
                if(stack.empty()):
                    stack.push(token)
                    continue

                peek = self.findToken(self.precedence, stack.peek().token)
                current = self.findToken(self.precedence, token.token)
                result = current[0][1] - peek[0][1]

                if result == 0:
                    self.insert(stack.pop(), list)
                    stack.push(token)
                elif result == 1:
                    stack.push(token)
                else:
                    self.clearStack(stack, list)
                    stack.push(token)

                if token.token == 'tk_)':
                    self.clearStack(stack, list)
            else:
                #arono bro
                self.insert(token, list)
                # list.append(token)



        #ahora en este punto se deberia de poder validar si la operacion esta escrita correctamente
        if not stack.empty():
            self.clearStack(stack, list)


        cadena = ''
        for token in list:
            cadena += token.lexema + ','

        print(cadena)

    def insert(self, element, list):
        print('insertando: ' ' ' +element.lexema)
        if element.token != 'tk_(' and element.token != 'tk_)':
            list.append(element)

    def findToken(self, iterable, element):
        return list(filter(lambda x: x[0] == element, iterable))

    def clearStack(self, stack, list):
        while stack.empty() == False:
            delete = stack.pop()
            print('sacando' + ' ' + delete.lexema)
            self.insert(delete, list)
