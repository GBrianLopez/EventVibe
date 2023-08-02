import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import json
from tkinter import messagebox

class Evento:
    def __init__(self, root, ventana_anterior):
        self.root = root
        self.root.title("EventVibe - Eventos")
        width = 600
        height = 505
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        GLabel_554 = tk.Label(self.root)
        ft = tkFont.Font(family='Times', size=68)
        GLabel_554["font"] = ft
        GLabel_554["fg"] = "#333333"
        GLabel_554["justify"] = "center"
        GLabel_554["text"] = "Eventos"
        GLabel_554.place(x=150, y=10, width=332, height=92)

        GButton_volver = tk.Button(self.root, text="Volver", command=lambda: self.volver(ventana_anterior))
        GButton_volver.place(x=10, y=10, width=70, height=30)

        # Crear un Frame para mostrar el Treeview
        self.frame = tk.Frame(self.root)
        self.frame.place(x=10, y=110, width=580, height=380)

        # Crear el Treeview para mostrar los eventos
        self.tree = ttk.Treeview(self.frame, columns=("Evento", "Artista", "Género", "Ubicación", "Asistir"), show="headings")
        self.tree.heading("#1", text="Evento")
        self.tree.heading("#2", text="Artista")
        self.tree.heading("#3", text="Género")
        self.tree.heading("#4", text="Ubicación")
        self.tree.heading("#5", text="Asistir")
        self.tree.pack(fill="both", expand=True)

        # Crear la barra de desplazamiento horizontal
        self.xscrollbar = ttk.Scrollbar(self.frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.xscrollbar.set)
        self.tree.place(x=0, y=0, width=570, height=250)
        self.xscrollbar.pack(side="bottom", fill="x")

        # Cargar los eventos desde el archivo JSON y mostrarlos en el Treeview
        self.cargar_eventos()

        # Agregar botón para crear recordatorio
        self.boton_recordatorio = tk.Button(self.root, text="Crear Recordatorio", command=self.crear_recordatorio)
        self.boton_recordatorio.place(x=5, y=370, width=150, height=30)


    def volver(self, ventana_anterior):
        ventana_anterior.deiconify()
        self.root.destroy()

    def cargar_eventos(self):
        try:
            with open("eventos.json", "r") as file:
                eventos = json.load(file)
        except FileNotFoundError:
            eventos = {}

        for evento, datos in eventos.items():
            artista = datos.get("artista", "")
            genero = datos.get("genero", "")
            ubicacion = datos.get("ubicacion", "")
            self.tree.insert("", "end", values=(evento, artista, genero, ubicacion, ""))

    def crear_recordatorio(self):
        seleccionado = self.tree.selection()
        if seleccionado:
            evento_seleccionado = self.tree.item(seleccionado[0])["values"][0]
            if evento_seleccionado:
                print(f"Se creó un recordatorio para asistir al evento: {evento_seleccionado}")
                messagebox.showinfo("Evento creado", f"Se creo un evento para asistir a {evento_seleccionado}")
                "nota mental: si me da tiempo completar para agregar un evento al json"
            else:
                print("Ningún evento seleccionado")
                messagebox.showwarning("Advertencia", "No se selecciono ningun evento")
        else:
            print("Ningún evento seleccionado")
            messagebox.showwarning("Advertencia", "Ningnun evento seleccionado")

if __name__ == "__main__":
    root = tk.Tk()
    app = Evento(root, None)
    root.mainloop()
