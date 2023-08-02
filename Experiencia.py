import tkinter as tk
import tkinter.font as tkFont
import json
import tkinter.ttk as ttk
from tkinter import messagebox

class Experiencia:
    def __init__(self, root, ventana_anterior):
        self.root = root
        self.root.title("EventVibe - Experiencias de Usuario")
        width = 800
        height = 505
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        GLabel_554 = tk.Label(self.root)
        ft = tkFont.Font(family='Times', size=20)
        GLabel_554["font"] = ft
        GLabel_554["fg"] = "#333333"
        GLabel_554["justify"] = "center"
        GLabel_554["text"] = "Experiencias "
        GLabel_554.place(x=250, y=10, width=332, height=92)

        GButton_volver = tk.Button(self.root, text="Volver", command=lambda: self.volver(ventana_anterior))
        GButton_volver.place(x=10, y=10, width=70, height=30)

        self.tree = ttk.Treeview(self.root, columns=("Usuario", "Evento", "Experiencia"), show="headings")
        self.tree.heading("#1", text="Usuario")
        self.tree.heading("#2", text="Evento")
        self.tree.heading("#3", text="Experiencia")
        self.tree.place(x=10, y=100, width=780, height=350)

        self.button_mostrar = tk.Button(self.root, text="Mostrar", command=self.mostrar_texto)
        self.button_mostrar.place(x=10, y=460, width=100, height=30)

        self.button_ocultar = tk.Button(self.root, text="Ocultar", command=self.ocultar_texto)
        self.button_ocultar.place(x=120, y=460, width=100, height=30)

        self.experiencia_original = {}  # Variable para guardar los comentarios originales
        self.mostrar_experiencias()

    def volver(self, ventana_anterior):
        ventana_anterior.deiconify()
        self.root.destroy()

    def mostrar_experiencias(self):
        try:
            with open("test.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        for usuario, info in data["usuarios"].items():
            eventos_usuario = info.get("eventos", [])
            for evento in eventos_usuario:
                comentario = evento.get("comentario", "")
                nombre_evento = evento.get("nombre_evento", "")
                experiencia = evento.get("experiencia", None)

                if not comentario or not nombre_evento or experiencia is None:
                    continue

                texto_experiencia = experiencia.get("texto", "")
                spoiler = experiencia.get("spoiler", False)

                if spoiler:
                    texto_experiencia = "*" * len(texto_experiencia)

                key = f"{usuario} - {nombre_evento}"  # Convertir la tupla a un solo string para usarlo como clave
                self.tree.insert("", "end", values=(usuario, nombre_evento, texto_experiencia, spoiler))
                self.experiencia_original[key] = experiencia

    def mostrar_texto(self):
        try:
            item = self.tree.selection()[0]
            key = self.tree.item(item, "values")[0:2]
            key = " - ".join(key)
            experiencia = self.experiencia_original.get(key, None)

            if experiencia and experiencia["spoiler"]:
                texto_experiencia = experiencia.get("texto", "")
                self.tree.item(item, values=(key.split(" - ")[0], key.split(" - ")[1], texto_experiencia, False))
        except:
            messagebox.showwarning("Advertencia", "No selecciono ningun comentario")

    def ocultar_texto(self):
        try:
            item = self.tree.selection()[0]
            key = self.tree.item(item, "values")[0:2]
            key = " - ".join(key)
            experiencia = self.experiencia_original.get(key, None)

            if experiencia and experiencia["spoiler"]:
                self.tree.item(item, values=(key.split(" - ")[0], key.split(" - ")[1], "*" * len(experiencia["texto"]), True))
            else:
                messagebox.showinfo("Adicional", "El comentario no se puede ocultar puesto que no esta marcado como spooiler")
        except:
            messagebox.showwarning("Advertencia", "No selecciono ningun comentario")

if __name__ == "__main__":
    root = tk.Tk()
    app = Experiencia(root, None)
