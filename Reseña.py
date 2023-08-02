import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
import json
from tkinter import ttk


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
        print("volver")

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
        app = Resenia(root, self.root, self.entry_usuario.get())  # Pasar la referencia de la ventana de inicio de sesión
        root.mainloop()







class Resenia:
    def __init__(self, root, ventana_anterior, usuario):
        self.usuario = usuario
        # Restaurar el título de la ventana y el tamaño
        self.root = root
        self.root.title("EventVibe - Reseñas")
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
        GLabel_554["text"] = "Reseñas y Comentarios"
        GLabel_554.place(x=150, y=-25, width=332, height=92)

        # Boton para volver
        GButton_volver = tk.Button(self.root, text="Volver", command=lambda: self.volver(ventana_anterior))
        GButton_volver.place(x=10, y=10, width=70, height=30)

        # Etiqueta para mostrar mensaje de comentar
        self.mensaje = tk.Label(self.root, text="Dejar un comentario", font="Times 15")
        self.mensaje.place(x=2, y=75)

        # Etiqueta para el comentario
        self.comentario_label = tk.Label(self.root, text="Agregue un comentario: ")
        self.comentario_label.place(x=0, y=100, width=145, height=30)

        # Cuadro de entrada para los comentarios
        self.comentario_entry = tk.Text(self.root, width=40, height=6)
        self.comentario_entry.place(x=5, y=130)

        # Etiqueta para la calificacion
        self.calificacion_label = tk.Label(self.root, text="Calificacion del evento")
        self.calificacion_label.place(x=350, y=100, width=177, height=30)

        # Frame de calificacion
        self.calificacion_Frame = tk.Frame(self.root)
        self.calificacion_Frame.place(x=350, y=120, width=200)
        # Lista para almacenar las estrellas para calificar
        self.estrellas = []
        # Creacion de las estrellas
        for i in range(5):
            estrella = tk.Label(self.calificacion_Frame, text="★", font=("Arial", 20))
            estrella.bind("<Button-1>", lambda event, idx=i: self.seleccionar_calificacion(idx))
            estrella.pack(side="left", padx=2)
            self.estrellas.append(estrella)
        # Variable para almacenar la calificacion
        self.calificacion_seleccionada = 0

        # Botón de guardar y enviar
        GButton_guardar = tk.Button(self.root, text="Guardar y Enviar", command=self.guardar_enviar)
        GButton_guardar.place(x=340, y=190, width=100, height=30)

        #desplazamiento para seleccionar el evento
        self.eventos_combobox = ttk.Combobox(self.root, state="readonly")
        self.eventos_combobox.place(x=5, y=45, width=200, height=25)  # Ajustar la posición y tamaño del desplegable


        """self.artista_label = tk.Label(self.root, text="Label de artista")
        self.artista_label.place(x=5, y=320, width=200, height=30)

        self.genero_label = tk.Label(self.root, text="")
        self.genero_label.place(x=5, y=350, width=200, height=30)

        self.ubicacion_label = tk.Label(self.root, text="Aqui va la ubicacion")
        self.ubicacion_label.place(x=5, y=380, width=200, height=30)"""

        self.cometario_titulo_label = tk.Label(self.root, text="Lista de comentarios", font="15")
        self.cometario_titulo_label.place(x=250, y=250)

        # Crear un Frame para mostrar los datos
        self.frame = tk.Frame(self.root)
        self.frame.place(x=10, y=280, width=580, height=160)

        # Crear el Treeview para mostrar los comentarios
        self.tree = ttk.Treeview(self.frame,
                                 columns=("Usuario", "Comentario", "Calificación", "Evento", "Artista", "Género", "Ubicación"),
                                 show="headings")
        self.tree.heading("#1", text="Usuario")
        self.tree.heading("#2", text="Comentario")
        self.tree.heading("#3", text="Calificación")
        self.tree.heading("#4", text="Evento")
        self.tree.heading("#5", text="Artista")
        self.tree.heading("#6", text="Género")
        self.tree.heading("#7", text="Ubicación")
        self.tree.pack(fill="both", expand=True)

        # Crear la barra de desplazamiento horizontal
        self.xscrollbar = ttk.Scrollbar(self.frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.xscrollbar.set)
        self.tree.place(x=0, y=0, width=570, height=250)
        self.xscrollbar.pack(side="bottom", fill="x")

        # vertical
        self.yscrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.yscrollbar.set)
        self.tree.place(x=0, y=0, width=570, height=150)
        self.yscrollbar.pack(side="right", fill="y")

        self.mostrar_eventos()
        self.mostrar_datos()

    # Accion para volver a la ventana anterior
    def volver(self, ventana_anterior):
        ventana_anterior.deiconify()
        self.root.destroy()
        print("volver")

    "NOTA: funciona pero no xd, ARREGLAR cuando lea esto"

    def guardar_enviar(self):
        nuevo_comentario = self.get_evento_seleccionado()
        if nuevo_comentario:
            try:
                # Cargar los datos existentes desde el archivo JSON
                with open("test.json", "r") as file:
                    datos_existentes = json.load(file)
            except FileNotFoundError:
                datos_existentes = {"usuarios": {}}

            # Verificar si el usuario existe en los datos existentes
            if self.usuario in datos_existentes["usuarios"]:
                # Agregar el nuevo comentario al usuario en el archivo JSON
                datos_existentes["usuarios"][self.usuario]["eventos"].append(nuevo_comentario)

                # Guardar los datos actualizados en el archivo JSON
                with open("test.json", "w") as file:
                    json.dump(datos_existentes, file, indent=4)

                # Mostrar un mensaje de confirmación utilizando messagebox
                messagebox.showinfo("Guardado", "Los datos se han guardado correctamente en test.json")
                self.comentario_entry.delete("1.0", tk.END)
                self.calificacion_seleccionada = 0

                # Luego de guardar, actualizar los datos mostrados en la ventana
                self.mostrar_datos()
            else:
                messagebox.showerror("Error", "Usuario no encontrado en el archivo test.json")

    def mostrar_eventos(self):
        # Cargar los datos existentes desde el archivo JSON
        try:
            with open("eventos.json", "r") as file:
                datos_existentes = json.load(file)
        except FileNotFoundError:
            datos_existentes = {}

        # Obtener los nombres de los eventos disponibles
        nombres_eventos = list(datos_existentes.keys())

        # Actualizar la lista desplegable con los nombres de los eventos
        self.eventos_combobox["values"] = nombres_eventos

        # Restablecer la selección del evento
        self.eventos_combobox.set("")

    def get_evento_seleccionado(self):
        evento_seleccionado = self.eventos_combobox.get()
        if evento_seleccionado:
            try:
                with open("eventos.json", "r") as file:
                    datos_eventos = json.load(file)
            except FileNotFoundError:
                datos_eventos = {}

            evento_info = datos_eventos.get(evento_seleccionado, {})
            return evento_info

        return None

    def cargar_eventos(self):
        try:
            with open("eventos.json", "r") as file:
                eventos = json.load(file)
            return list(eventos.values())
        except FileNotFoundError:
            return []

    # pintar las estrellidas
    def seleccionar_calificacion(self, idx):
        # Restablecer la calificación seleccionada previa
        if self.calificacion_seleccionada is not None:
            self.estrellas[self.calificacion_seleccionada].config(foreground="black")

        # Establecer la nueva calificación seleccionada
        self.calificacion_seleccionada = idx

        # Actualizar el color de las estrellas seleccionadas
        for i in range(idx + 1):
            self.estrellas[i].config(foreground="gold")

    def mostrar_datos(self):
        # Limpiar los datos anteriores del Treeview
        self.tree.delete(*self.tree.get_children())

        # Cargar todos los datos existentes desde el archivo JSON
        try:
            with open("test.json", "r") as file:
                datos_existentes = json.load(file)
        except FileNotFoundError:
            datos_existentes = {}

        # Mostrar los datos en el Treeview
        for usuario, data_usuario in datos_existentes["usuarios"].items():
            eventos_usuario = data_usuario["eventos"]
            for data in eventos_usuario:
                comentario = data.get('comentario', '')  # Usar data.get() para evitar KeyError
                calificacion = data.get('calificacion', '')  # Usar data.get() para evitar KeyError
                nombre_evento = data.get('nombre_evento', '')
                artista = data.get('artista', '')
                genero = data.get('genero', '')
                ubicacion = data.get('ubicacion', '')
                self.tree.insert("", "end",
                                 values=(usuario, comentario, calificacion, nombre_evento, artista, genero, ubicacion))






if __name__ == "__main__":
    root = tk.Tk()
    app = InicioSesion(root)
    root.mainloop()
