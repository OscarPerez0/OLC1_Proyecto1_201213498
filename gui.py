import tkinter as tk
import os
from tkinter import filedialog, ttk
from jsscanner import JsScanner
from CssScanner import CssScanner
from HtmlScanner import HtmlScanner
from Reporte import Reporte
from AritmeticScanner import AritmeticScanner
from AritmeticParser import AritmeticParser
from Arbol import Arbol
from Grafo import Grafo


import platform

#Before run execute sudo chmod o+rwx

class Gui():
    def __init__(self, parent):
        self.root = parent
        self.log = None
        self.editor = None
        self.type_file = None
        self.scanner = None
        self.parser = None
        self.expresiones = []
        self.current_file_name = ''
        self.currentPath = ""
        self.create_widgets()

        #necesarias para invocar los distintos analizadores



    def create_widgets(self):
        self.create_menubar()
        self.create_log()

    def create_log(self):
        self.editor = tk.Text(self.root, height = 25)
        self.editor.pack(fill = tk.X, pady = 5)


        self.log = tk.Text(self.root, height = 15, bg = "black", fg = "white")
        self.log.pack(fill = tk.X, pady = 5)

    def create_menubar(self):
        menubar = tk.Menu(self.root, tearoff=0)
        filemenu = tk.Menu(menubar, tearoff=0)
        tools = tk.Menu(menubar, tearoff=0)
        report = tk.Menu(menubar, tearoff=0)

        filemenu.add_command(label="Nuevo", command=self.nuevo())
        filemenu.add_command(label="Abrir", command=self.onOpen)
        filemenu.add_command(label = "Abrir Archivo rmt", command=self.onOpenRmt) #escribir la funcion para este comando
        filemenu.add_command(label="Guardar", command=self.save)
        filemenu.add_command(label="Guardar Como", command=self.saveAs)
        filemenu.add_command(label="Salir", command=self.root.quit)

        tools.add_command(label="Analizar Archivo", command=self.run)
        tools.add_command(label = "Aanlizar Rmt", command=self.runRmt) #add command

        report.add_command(label='Reporte de Tablas', command=self.reporte_tablas)
        report.add_command(label='Reporte Rmt', command=self.reporte_expresiones)
        report.add_command(label='Reporte Arbol', command=self.generar_reporte_arbol)
        report.add_command(label='Reporte Automata', command=self.generar_reporte_grafo)

        menubar.add_cascade(label="Archivo", menu=filemenu)
        menubar.add_cascade(label="Herramientas", menu=tools)
        menubar.add_cascade(label="Reportes", menu=report)



        self.root.config(menu=menubar)


    def onOpen(self):
        ftypes = [('Css Files', '*.css'), ('JavaScript Files', '*.js'), ('Html Files', '*.html')]
        dialog = filedialog.askopenfilename(initialdir = '~/Escritorio', title='Select File', filetypes = ftypes)


        if not dialog:
            return


        self.type_file = os.path.splitext(dialog)[1]
        self.currentPath = dialog
        self.current_file_name = os.path.basename(dialog)
        self.readFile(dialog)

    def onOpenRmt(self):
        type = [('Rmt Files', '*.rmt')]
        dialog = filedialog.askopenfilename(initialdir = '~/Escritorio', title = 'Select File', filetypes = type)

        if not dialog:
            return

        self.readFile(dialog)


    def save(self):
        print('save function')
        if self.currentPath != "":
            self.writeFile(self.currentPath, self.editor.get("1.0", "end-1c"))
        else:
            self.saveAs()

    def saveAs(self):
        print('save As function')

        ftypes = [('Css Files', '*.css'), ('JavaScript Files', '*.js'), ('Html Files', '*.html')]
        filename = filedialog.asksaveasfile(mode = "w", defaultextension = ".*")

        if filename is None:
            return

        content = self.editor.get("1.0", "end-1c")
        filename.write(content)
        filename.close()



    def readFile(self, path):
        print('Seleccionando el tipo de archivo ' + path)
        pointer = open(path, 'r')
        text = pointer.read()

        self.editor.delete('1.0', "end-1c")
        self.editor.insert('end-1c', text)

    def writeFile(self, path, content):
        pointer = open(path, 'w')
        pointer.write(content)

    def nuevo(self):
        self.scanner = None
        self.parser = None
        self.expresiones.clear()

    def reporte_tablas(self):
        if self.scanner != None:
            reporte = Reporte(self.scanner.tokens, self.scanner.errores)
            reporte.generarReporteTabla('reporte_tokens.html', True)
            reporte.generarReporteTabla('reporte_errores.html', False)
        else:
            print('no se puede generar reportes. Antes se debe analizar algun archivo')

    def reporte_expresiones(self):
        if self.scanner != None:
            if isinstance(self.scanner, AritmeticScanner):
                reporte = Reporte(self.scanner.tokens, self.scanner.errores)
                reporte.generar_reporte_parser('reporte_parser.html', self.expresiones)

    def generar_reporte_grafo(self):
        if self.scanner != None:

            if isinstance(self.scanner, JsScanner):
                grafo = Grafo(self.scanner.out_er)
                grafo.generar_grafo()
            else:
                print('El diagrama de Grafo unicamente se genera para el archivo Js')


    def generar_reporte_arbol(self):
        if self.scanner != None:
            if isinstance(self.scanner, JsScanner):
                arbol = Arbol(self.scanner.out_er)
                arbol.generar_grafo()
            else:
                print('El diagrama de Arbol unicamente se genera para el archivo Js')

    def runRmt(self):
        texto = self.editor.get('1.0', 'end-1c')
        if not texto:
            print('no hay nada que analizar papirrin')
        else:
            self.scanner = AritmeticScanner(texto)
            self.scanner.scanner()
            self.scanner.generate_lists()

            if not self.scanner.errores:
                for list_tks in self.scanner.lists:
                    self.parser = AritmeticParser(list_tks)
                    self.parser.parse()
                    self.expresiones.append(self.parser.get_out())
            else:
                print('se han encontrado errores lexicos en el archivo Rmt')

    def run(self):
        if self.type_file == None:
            print('no se puede tomar una decision sobre que analizador ejecutar. Guarde el archivo o eliga un archivo valido')
            return

        if self.type_file == '.css':
            print('css scanner executing')
            self.scanner = CssScanner(self.editor.get('1.0', 'end-1c'), self.log)
            self.scanner.scanner()
            path = self.scanner.find_path()

            if path != None:
                self.create_dirs(path)
                self.writeFile(path + self.current_file_name, self.scanner.out_text.getvalue())

        elif self.type_file == '.js':
            print('js scanner executing')
            self.scanner = JsScanner(self.editor.get('1.0', 'end-1c'), self.editor)
            self.scanner.scanner()
            path = self.scanner.find_path()

            if path != None:
                self.create_dirs(path)
                self.writeFile(path + self.current_file_name, self.scanner.out_text.getvalue())

        elif self.type_file == '.html':
            print('html scanner executing')
            self.scanner = HtmlScanner(self.editor.get('1.0', 'end-1c'))
            self.scanner.scanner()
            path = self.scanner.find_path()

            if path != None:
                self.create_dirs(path)
                self.writeFile(path + self.current_file_name, self.scanner.out_text)

        else:
            print('La extension del archivo leido no se reconoce')

    def create_dirs(self, path):
        if os.path.exists(path):
            return

        try:
            original_umask =  os.umask(0)
            os.makedirs(path, mode = 0o777)
        except OSError:
            print('Create Directory Failed')
        finally:
            os.umask(original_umask)


def main():
    print('main ')
    r = tk.Tk()
    ui = Gui(r)
    r.geometry('800x600')
    r.title('Compiladores_1_Proyecto_1')
    r.resizable(0,0)
    r.mainloop()


if __name__ == '__main__':
    main()


