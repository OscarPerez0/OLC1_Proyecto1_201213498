from Nodo import Nodo
from io import StringIO
import os
from PIL import Image

class Arbol:

    def __init__(self, ers):
        self.er = []
        self.genera_er(ers)
        self.error = False
        self.raiz = None

    def genera_er(self, ers):
        cant_o = len(ers) - 1

        self.er.append('.')

        index = 0
        while index < cant_o:
            self.er.append("|")
            index += 1


        #ahora tengo que agregar las ers
        temp = list(ers.values())
        for aux in temp:
            i = 0
            while i < len(aux):
                self.er.append(aux[i])
                i += 1

        self.er.append('#')

    def generar_grafo(self):
        local = self.er.copy()
        self.doblar(local)
        while len(local) > 1:
            self.doblar(local)

        if not self.error:
            self.desdoblar(local[0])
            self.graficar_arbol()


    def doblar(self, local):
        index = 0
        while index < len(local):
            if self.is_operador(local[index]):
                if self.is_binario(local[index]):
                    pos_act = index
                    if (pos_act + 2) <= len(local) - 1:
                        if self.se_dobla_binario(local[index + 1], local[index + 2]):
                            aux = Auxiliar(local[index], local[index + 1], local[index + 2])
                            local[index] = aux
                            local.pop(index + 1)
                            local.pop(index + 1)
                    else:
                        self.error = True
                else:
                    pos_act = index
                    if (pos_act + 1) <= len(local) - 1:
                        if self.se_dobla_unario(local[index + 1]):
                            aux = Auxiliar(local[index], local[index + 1])
                            local[index] = aux
                            local.pop(index + 1)
                    else:
                        self.error = True
            index += 1


    def desdoblar(self, auxiliar):
        self.raiz = Nodo()
        self.raiz.set_valor(auxiliar)

        self.expander(self.raiz)

        # temporal = Nodo()
        # temporal.set_valor('#')
        #
        #
        # aux = self.raiz
        # self.raiz = Nodo()
        # self.raiz.set_valor('.')
        # self.raiz.create_hijos()
        # self.raiz.agregar_hijo(aux)
        # self.raiz.agregar_hijo(temporal)


    def expander(self, raiz):
        if raiz == None:
            return

        if isinstance(raiz.valor, Auxiliar):
            temp = raiz.valor
            operador = temp.op

            raiz.set_valor(operador)
            if raiz.hijos_null():
                raiz.create_hijos()

            if self.is_binario(operador):
                t = Nodo()
                t.set_valor(temp.o1)
                raiz.agregar_hijo(t)

                t1 = Nodo()
                t1.set_valor(temp.o2)
                raiz.agregar_hijo(t1)
            else:
                t = Nodo()
                t.set_valor(temp.o1)
                raiz.agregar_hijo(t)
        else:
            return

        self.expander(raiz.hijos[0])
        if len(raiz.hijos) > 1:
            self.expander(raiz.hijos[1])

    def graficar_arbol(self):
        print('escribir aqui el archivo')

        try:
            buffer = StringIO()

            buffer.write('Digraph G{\n graph[overlap=true, fontsize = 0.5];\n')
            buffer.write('edge[color = black];\n')
            buffer.write(self.generar_dot(self.raiz))
            buffer.write('\n}')


            file = open('Reportes/grafo.dot', mode= 'w')
            file.write(buffer.getvalue())
            file.close()

            os.system('dot -Tpng Reportes/grafo.dot -o Reportes/grafo.png')
            img = Image.open('Reportes/grafo.png')
            img.show()
            print('todo listo paps')
        except:
            print('some errors found')

    def generar_dot(self,raiz):
        if raiz == None:
            return ""

        buffer = StringIO()

        buffer.write('nodo')
        buffer.write(str(hash(raiz)))
        buffer.write('[label= "')
        buffer.write(self.change_string(raiz.valor))
        buffer.write('"];\n')

        for temporal in raiz.hijos:
            if temporal != None:
                buffer.write('nodo')
                buffer.write(str(hash(temporal)))
                buffer.write('[label= "')
                buffer.write(self.change_string(temporal.valor))
                buffer.write('"];\n')

                buffer.write('nodo' + str(hash(raiz)))
                buffer.write('->')
                buffer.write('nodo' + str(hash(temporal)))
                buffer.write('\n')

                if not temporal.hijos_null():
                    buffer.write(self.generar_dot(temporal))

        return buffer.getvalue()

    def change_string(self, string):
        salida = ''
        if string == "@":
             salida = "*"
        elif string == 'p':
            salida = '.'
        else:
            if string == '"':
                salida = '\\"'
            else:
                salida = string

        return salida


    def se_dobla_binario(self, a, b):
        if not self.is_operador(a) and not self.is_operador(b):
            return True
        return False

    def se_dobla_unario(self, a):
        if not self.is_operador(a):
            return True
        return False

    def is_operador(self, op):
        if op == '+' or op == '*' or op == '?' or op == '|' or op == '.':
            return True
        return False

    def is_binario(self, op):
        if op == '|' or op == '.':
            return True
        return False

    def is_unario(self, op):
        if op == '+' or op == '*' or op == '?':
            return True
        return False


class Auxiliar:
    def __init__(self, op, o1, o2= None):
        self.op = op
        self.o1 = o1
        self.o2 = o2