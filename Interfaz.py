import tkinter as tk
from tkinter import filedialog, ttk
import os


class Gui():
    def __init__(self, parent):
        self.root = parent
        self.log = None
        self.editor = None
        self.type_file = None
        self.currentPath = ""
        self.create_widgets()

    def create_widgets(self):
        self.create_menubar()
        self.create_log()

    def create_log(self):
        self.editor = tk.Text(self.root, height = 25)
        self.editor.pack(fill = tk.X, pady = 5)


        self.log = tk.Text(self.root, height = 10, bg = "black", fg = "white")
        self.log.pack(fill = tk.X, pady = 5)

    def create_menubar(self):
        menubar = tk.Menu(self.root, tearoff=0)
        filemenu = tk.Menu(menubar, tearoff=0)
        tools = tk.Menu(menubar, tearoff=0)
        report = tk.Menu(menubar, tearoff=0)

        filemenu.add_command(label="Nuevo")
        filemenu.add_command(label="Abrir", command = self.onOpen)
        filemenu.add_command(label="Guardar", command = self.save)
        filemenu.add_command(label="Guardar Como", command = self.saveAs)
        filemenu.add_command(label="Salir", command = self.root.quit)

        tools.add_command(label="Analizar Archivo", command = self.run)

        menubar.add_cascade(label="Archivo", menu=filemenu)
        menubar.add_cascade(label="Herramientas", menu=tools)
        menubar.add_cascade(label="Reportes", menu=report)

        self.root.config(menu=menubar)


    def onOpen(self):
        ftypes = [('Css Files', '*.css'), ('JavaScript Files', '*.js'), ('Html Files', '*.html')]
        dialog = filedialog.askopenfilename(initialdir = '/home', title='Select File', filetypes = ftypes)
        self.type_file = os.path.splitext(dialog)[1]
        self.currentPath = dialog

        print(self.type_file)
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

        print(text)

        self.editor.delete('1.0', "end-1c")
        self.editor.insert('end-1c', text)

    def writeFile(self, path, content):
        pointer = open(path, 'w')
        pointer.write(content)


    def run(self):
        print('run scanner ')

        if self.type_file == '.css':
            print('css scanner en proceso')
        elif self.type_file == '.js':
            print('js scanner en proceso')
        elif self.type_file == '.html':
            print('html scanner en proceso')
        else:
            print('ninguno')


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


