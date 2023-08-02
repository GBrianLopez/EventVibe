import tkinter as tk
import tkinter.font as tkFont
import json
from tkinter import ttk
from tkinter import messagebox

class InicioSesion:
    def __init__(self, root, ventana_anterior):
        self.root = root
        self.root.title("EventVibe - Inicio de Sesión")
        # Setting window size
        width = 600
        height = 500
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
        GLabel_554["text"] = "EventVibe - Inicio de Sesión"
        GLabel_554.place(x=150, y=10, width=360, height=40)

        self.label_usuario = tk.Label(self.root, text="Nombre de Usuario:")
        self.label_usuario.place(x=150, y=60, width=120, height=25)

        self.entry_usuario = tk.Entry(self.root)
        self.entry_usuario.place(x=280, y=60, width=130, height=25)

        self.label_contrasena = tk.Label(self.root, text="Contraseña:")
        self.label_contrasena.place(x=150, y=100, width=120, height=25)

        self.entry_contrasena = tk.Entry(self.root, show="*")
        self.entry_contrasena.place(x=280, y=100, width=130, height=25)

        self.boton_iniciar_sesion = tk.Button(self.root, text="Iniciar Sesión", command=self.iniciar_sesion)
        self.boton_iniciar_sesion.place(x=160, y=150, width=100, height=30)

        self.boton_registrar = tk.Button(self.root, text="Registrar", command=self.registrar_usuario)
        self.boton_registrar.place(x=280, y=150, width=100, height=30)

        #boton para voler
        GButton_volver = tk.Button(self.root, text="Volver", command=lambda: self.volver(ventana_anterior))
        GButton_volver.place(x=10, y=10, width=70, height=30)

    # accion para volver a la ventana anterior
    def volver(self, ventana_anterior):
        ventana_anterior.deiconify()
        self.root.destroy()

    def iniciar_sesion(self):
        nombre_usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()

        if self.validar_credenciales(nombre_usuario, contrasena):
            self.abrir_ventana_historial(nombre_usuario)
        else:
            messagebox.showerror("Error de inicio de sesión", "Usuario o contraseña incorrectos.")

    def validar_credenciales(self, nombre_usuario, contrasena):
        try:
            with open("test.json", "r") as file:
                data = json.load(file)
                if "usuarios" in data:
                    usuarios = data["usuarios"]
                    if nombre_usuario in usuarios and "contrasena" in usuarios[nombre_usuario] and usuarios[nombre_usuario]["contrasena"] == contrasena:
                        return True
        except FileNotFoundError:
            print("Archivo JSON no encontrado")
        return False

    def registrar_usuario(self):
        nombre_usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()

        if not contrasena:
            messagebox.showerror("Error de registro", "Debe ingresar una contraseña.")
        elif self.validar_usuario_existente(nombre_usuario):
            messagebox.showerror("Error de registro", "El usuario ya existe.")
        else:
            self.registrar_nuevo_usuario(nombre_usuario, contrasena)
            messagebox.showinfo("Registro exitoso", "El usuario ha sido registrado exitosamente.")

    def validar_usuario_existente(self, nombre_usuario):
        try:
            with open("test.json", "r") as file:
                data = json.load(file)
                if "usuarios" in data:
                    usuarios = data["usuarios"]
                    return nombre_usuario in usuarios
        except FileNotFoundError:
            print("Archivo JSON no encontrado")
        return False

    def registrar_nuevo_usuario(self, nombre_usuario, contrasena):
        try:
            with open("test.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        if "usuarios" not in data:
            data["usuarios"] = {}

        data["usuarios"][nombre_usuario] = {
            "contrasena": contrasena,
            "eventos": []
        }

        with open("test.json", "w") as file:
            json.dump(data, file, indent=4)

    def abrir_ventana_historial(self, nombre_usuario):
        self.root.withdraw()  # Ocultar la ventana de inicio de sesión
        root = tk.Toplevel()  # Crear una nueva ventana
        app = Historial(root, nombre_usuario, self.root)  # Pasar la referencia de la ventana de inicio de sesión
        root.mainloop()


class Historial:
    def __init__(self, root, nombre_usuario, ventana_inicio_sesion):
        self.root = root
        self.root.title("EventVibe - Historial de Eventos Asistidos")
        # Setting window size
        width = 600
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
        GLabel_554["text"] = "Historial de Eventos"
        GLabel_554.place(x=150, y=10, width=332, height=92)

        # Crear el widget Treeview con las barras de desplazamiento vertical y horizontal
        self.columnas_treeview()

        # Cargar datos desde el archivo JSON
        self.usuarios = {}
        self.nombre_usuario = nombre_usuario
        self.cargar_datos_desde_json()
        self.ventana_inicio_sesion = ventana_inicio_sesion

        # boton para voler
        GButton_volver = tk.Button(self.root, text="Volver", command=lambda: self.volver())
        GButton_volver.place(x=10, y=10, width=70, height=30)


    # accion para volver a la ventana anterior
    def volver(self):
        self.root.withdraw()  # Ocultar la ventana de historial de eventos
        self.ventana_inicio_sesion.deiconify()

    def columnas_treeview(self):
        # Configurar el Treeview
        self.tabla = ttk.Treeview(self.root, columns=("Nombre Usuario", "Nombre Evento", "Artista", "Género", "Ubicación"))
        self.tabla.place(x=10, y=100, width=580, height=390)

        # Crear la barra de desplazamiento vertical y asociarla al Treeview
        scrollbar_y = ttk.Scrollbar(self.root, orient="vertical", command=self.tabla.yview)
        scrollbar_y.place(x=590, y=100, height=390)
        self.tabla.configure(yscrollcommand=scrollbar_y.set)

        # Crear la barra de desplazamiento horizontal y asociarla al Treeview
        scrollbar_x = ttk.Scrollbar(self.root, orient="horizontal", command=self.tabla.xview)
        scrollbar_x.place(x=10, y=490, width=580)
        self.tabla.configure(xscrollcommand=scrollbar_x.set)

        self.tabla.column("#0", width=0, stretch=tk.NO)  # Ajustar el ancho de la columna índice "#0" a cero

        self.tabla.column("Nombre Usuario", width=150, anchor=tk.CENTER)
        self.tabla.column("Nombre Evento", width=150, anchor=tk.CENTER)
        self.tabla.column("Artista", width=100, anchor=tk.CENTER)
        self.tabla.column("Género", width=100, anchor=tk.CENTER)
        self.tabla.column("Ubicación", width=100, anchor=tk.CENTER)

        self.tabla.heading("#0", text="", anchor=tk.CENTER)
        self.tabla.heading("Nombre Usuario", text="Nombre Usuario", anchor=tk.CENTER)
        self.tabla.heading("Nombre Evento", text="Nombre Evento", anchor=tk.CENTER)
        self.tabla.heading("Artista", text="Artista", anchor=tk.CENTER)
        self.tabla.heading("Género", text="Género", anchor=tk.CENTER)
        self.tabla.heading("Ubicación", text="Ubicación", anchor=tk.CENTER)

        self.tabla["displaycolumns"] = ("Nombre Usuario", "Nombre Evento", "Artista", "Género", "Ubicación")

    def cargar_datos_desde_json(self):
        try:
            with open("test.json", "r") as file:
                data = json.load(file)
                if "usuarios" in data:
                    self.usuarios = data["usuarios"]
                    eventos_usuario = self.usuarios[self.nombre_usuario]["eventos"]
                    for evento in eventos_usuario:
                        nombre_evento = evento["nombre_evento"]
                        artista = evento["artista"]
                        genero = evento["genero"]
                        ubicacion = evento["ubicacion"]
                        self.tabla.insert("", tk.END,
                                          values=(self.nombre_usuario, nombre_evento, artista, genero, ubicacion))
        except FileNotFoundError:
            print("Archivo JSON no encontrado")

if __name__ == "__main__":
    root = tk.Tk()
    app = InicioSesion(root)
    root.mainloop()


