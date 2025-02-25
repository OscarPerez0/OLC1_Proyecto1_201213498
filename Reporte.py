from io import StringIO

class Reporte:

    def __init__(self, tokens:None, errores:None):
        self.tokens = tokens
        self.errores = errores

    def generarReporteTabla(self, name, flag):
        self.__escribirArchivo(self.__generarReporte(flag), name)


    def generar_reporte_parser(self, name, list):
        self.__escribirArchivo(self.__reporte_parser(list), name)

    def __escribirArchivo(self, data, name):
        try:
            filename = 'Reportes/' + name
            writer = open(filename, 'w')
            writer.write(data)
            writer.close()

        except:
            print('Ocurrio un error al intentar escribir el archivo')


    def __reporte_parser(self, list):
        buffer = StringIO()
        buffer.write('''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Reporte Lexico</title>
                </head>

                <body>

                <div alignment = "center">

                <h1>Reporte</h1>
                <hr>

                <table border>

                ''')

        #generar aqui la tabla
        buffer.write('<tr>')

        buffer.write('<th> Expresion </th>')
        buffer.write('<th> Analisis </th>')

        buffer.write('</tr>')

        for element in list:
            buffer.write('<tr>')

            buffer.write('<td>')
            buffer.write(str(element[0])[:-1])
            buffer.write('</td>')

            buffer.write('<td>')
            buffer.write(str(element[1]))
            buffer.write('</td>')


        buffer.write('''

                </table>
                </div>
                </body>
                </html>
                ''')

        return buffer.getvalue()


    def __generarReporte(self, flag):
        buffer = StringIO()

        buffer.write('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Reporte Lexico</title>
        </head>
        
        <body>
        
        <div alignment = "center">
        
        <h1>Reporte</h1>
        <hr>
        
        <table border>
        
        ''')


        if flag:
            buffer.write(self.__tablaTokens())
        else:
            buffer.write(self.__tablaErrores())



        buffer.write('''
        
        </table>
        </div>
        </body>
        </html>
        ''')

        return buffer.getvalue()

    def __tablaTokens(self):
        print('Reporte de tokens')
        buffer = StringIO()

        buffer.write('<tr>')

        buffer.write('<th> Token </th>')
        buffer.write('<th> Lexema </th>')
        buffer.write('<th> Linea </th>')
        buffer.write('<th> Columna </th>')

        buffer.write('</tr>')


        for token in self.tokens:

            buffer.write('<tr>')

            buffer.write('<td>')
            buffer.write(token.token)
            buffer.write('</td>')

            buffer.write('<td>')
            buffer.write(token.lexema)
            buffer.write('</td>')

            buffer.write('<td>')
            buffer.write(str(token.linea))
            buffer.write('</td>')

            buffer.write('<td>')
            buffer.write(str(token.columna))
            buffer.write('</td>')

            buffer.write('</tr>')

        return buffer.getvalue()


    def __tablaErrores(self):
        print('Reporte de Errores')
        buffer = StringIO()

        buffer.write('<tr>')

        buffer.write('<th> Lexema </th>')
        buffer.write('<th> Tipo </th>')
        buffer.write('<th> Descripcion </th>')
        buffer.write('<th> Linea </th>')
        buffer.write('<th> Columna </th>')

        buffer.write('</tr>')

        for error in self.errores:
            buffer.write('<tr>')

            buffer.write('<td>')
            buffer.write(error.lexema)
            buffer.write('</td>')

            buffer.write('<td>')
            buffer.write(error.tipo)
            buffer.write('</td>')

            buffer.write('<td>')
            buffer.write(error.descripcion)
            buffer.write('</td>')

            buffer.write('<td>')
            buffer.write(str(error.linea))
            buffer.write('</td>')

            buffer.write('<td>')
            buffer.write(str(error.columna))
            buffer.write('</td>')

            buffer.write('</tr>')

        return buffer.getvalue()
