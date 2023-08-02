import tkinter as tk
import tkinter.font as tkFont
from tkcalendar import DateEntry
from tkinter import ttk
import json
import Evento
from MapayRuta import abrir_ventana_mapa
import Reseña
import Historial
import Experiencia


class Principal:
    def __init__(self, root):
        #setting title
        self.root = root
        self.root.title("EventVibe")
        #setting window size
        width=600
        height=505
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        GLabel_718=tk.Label(self.root)
        GLabel_718["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=10)
        GLabel_718["font"] = ft
        GLabel_718["fg"] = "#333333"
        GLabel_718["justify"] = "center"
        GLabel_718["text"] = "."
        GLabel_718.place(x=0,y=40,width=599,height=40)

        # Boton de eventos
        GButton_524= tk.Button(self.root)
        GButton_524["anchor"] = "center"
        GButton_524["bg"] = "#ffffff"
        GButton_524["borderwidth"] = "0px"
        ft = tkFont.Font(family='Times',size=10)
        GButton_524["font"] = ft
        GButton_524["fg"] = "#000000"
        GButton_524["justify"] = "center"
        GButton_524["text"] = "Eventos"
        GButton_524.place(x=0,y=40,width=100,height=39)
        GButton_524["command"] = self.boton_eventos

        # Boton Mapas y Rutas
        GButton_435=tk.Button(self.root)
        GButton_435["bg"] = "#ffffff"
        GButton_435["borderwidth"] = "0px"
        ft = tkFont.Font(family='Times',size=10)
        GButton_435["font"] = ft
        GButton_435["fg"] = "#000000"
        GButton_435["justify"] = "center"
        GButton_435["text"] = "Mapas y Rutas"
        GButton_435.place(x=110,y=40,width=119,height=39)
        GButton_435["command"] = self.boton_mapas_y_rutas

        # boton de reseñas
        GButton_295=tk.Button(self.root)
        GButton_295["bg"] = "#ffffff"
        GButton_295["borderwidth"] = "0px"
        ft = tkFont.Font(family='Times',size=10)
        GButton_295["font"] = ft
        GButton_295["fg"] = "#000000"
        GButton_295["justify"] = "center"
        GButton_295["text"] = "Reseñas"
        GButton_295.place(x=230,y=40,width=120,height=39)
        GButton_295["command"] = self.boton_resenias

        # boton de historial
        GButton_737=tk.Button(self.root)
        GButton_737["bg"] = "#ffffff"
        GButton_737["borderwidth"] = "0px"
        ft = tkFont.Font(family='Times',size=10)
        GButton_737["font"] = ft
        GButton_737["fg"] = "#000000"
        GButton_737["justify"] = "center"
        GButton_737["text"] = "Historial"
        GButton_737.place(x=350,y=40,width=110,height=39)
        GButton_737["command"] = self.boton_historial

        # boton de experiencia
        GButton_981=tk.Button(self.root)
        GButton_981["bg"] = "#ffffff"
        GButton_981["borderwidth"] = "0px"
        ft = tkFont.Font(family='Times',size=10)
        GButton_981["font"] = ft
        GButton_981["fg"] = "#000000"
        GButton_981["justify"] = "center"
        GButton_981["text"] = "Experiencia"
        GButton_981.place(x=460,y=40,width=138,height=38)
        GButton_981["command"] = self.boton_experiencia

        # boton de buscar
        """GButton_744=tk.Button(self.root)
        GButton_744["bg"] = "#000000"
        GButton_744["borderwidth"] = "0px"
        ft = tkFont.Font(family='Times',size=12)
        GButton_744["font"] = ft
        GButton_744["fg"] = "#ffffff"
        GButton_744["justify"] = "center"
        GButton_744["text"] = "Buscar"
        GButton_744.place(x=440,y=210,width=93,height=44)
        GButton_744["command"] = self.GButton_744_command"""

        GLabel_20 = tk.Label(self.root)
        ft = tkFont.Font(family='Times', size=28)
        GLabel_20["font"] = ft
        GLabel_20["fg"] = "#333333"
        GLabel_20["justify"] = "center"
        GLabel_20["text"] = "¡Miles de eventos! Busca aquí el tuyo"
        GLabel_20.place(x=0, y=100, width=592, height=45)


        GLabel_221=tk.Label(self.root)
        ft = tkFont.Font(family='Times',size=18)
        GLabel_221["font"] = ft
        GLabel_221["fg"] = "#333333"
        GLabel_221["justify"] = "center"
        GLabel_221["text"] = "EventVibe"
        GLabel_221.place(x=0,y=0,width=152,height=38)

        #entry de busqueda
        """GLineEdit_614=tk.Entry(self.root)
        GLineEdit_614["bg"] = "#ffffff"
        GLineEdit_614["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_614["font"] = ft
        GLineEdit_614["fg"] = "#000000"
        GLineEdit_614["justify"] = "center"
        GLineEdit_614["text"] = "Introduce un texto..."
        GLineEdit_614.place(x=60,y=210,width=379,height=45)"""




        # checkbox  para búsqueda por fecha
        self.calendar_var = tk.BooleanVar(value=False)
        self.date_checkbox = tk.Checkbutton(self.root, text="Buscar por fecha", variable=self.calendar_var,
                                            font=("Arial", 12))
        self.date_checkbox.place(x=370, y=205)

        # Treeview para mostrar resultados de la búsqueda
        self.tree = ttk.Treeview(self.root, columns=("Nombre", "Artista", "Género", "Ubicación", "Fecha"))
        self.tree.heading("#1", text="Nombre")
        self.tree.heading("#2", text="Artista")
        self.tree.heading("#3", text="Género")
        self.tree.heading("#4", text="Ubicación")
        self.tree.heading("#5", text="Fecha")
        self.tree.place(x=60, y=250, width=480, height=180)
        self.tree.column("#0", width=0)

        # Agregar una barra de desplazamiento horizontal
        self.scrollbar_x = ttk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.scrollbar_x.place(x=60, y=460, width=480)  # Ubicar la barra de desplazamiento en la posición deseada

        # Configurar la barra de desplazamiento horizontal para el treeview
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)

        # Botón de buscar
        GButton_744 = tk.Button(self.root)
        GButton_744["bg"] = "#000000"
        GButton_744["borderwidth"] = 0
        ft = tkFont.Font(family='Times', size=12)
        GButton_744["font"] = ft
        GButton_744["fg"] = "#ffffff"
        GButton_744["justify"] = "center"
        GButton_744["text"] = "Buscar"
        GButton_744.place(x=440, y=160, width=93, height=44)
        GButton_744["command"] = self.GButton_744_command

        self.GLineEdit_search = tk.Entry(self.root, bg="#ffffff", borderwidth=1, font=("Times", 10))
        self.GLineEdit_search.place(x=60, y=160, width=379, height=45)

        # Crear el checkbox para habilitar la búsqueda por fecha
        self.use_date_var = tk.BooleanVar()
        self.use_date_checkbox = ttk.Checkbutton(self.root, text="Mostrar/ocultar calendario", variable=self.use_date_var,
                                                 command=self.toggle_date_entry)
        self.use_date_checkbox.place(x=60, y=208)

        # Crear el campo de selección de fecha (inicialmente oculto)
        self.GLineEdit_date = DateEntry(self.root, bg="#ffffff", font=("Times", 10))
        self.GLineEdit_date.place(x=210, y=260)
        self.GLineEdit_date.place_forget()


    def boton_eventos(self):
        print("Eventos")
        root2 = tk.Toplevel(self.root)  # Crea una nueva ventana de nivel superior
        ventana_eventos = Evento.Evento(root2, self.root)  # Instancia la clase Principal
        self.root.withdraw()  # Oculta la ventana principal
        root2.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)  # Maneja el cierre de la ventana principal
        root2.mainloop()


    def boton_mapas_y_rutas(self):
        print("Mapas y rutas")
        abrir_ventana_mapa(self.root)


    def boton_resenias(self):
        print("Reseñas")
        root2 = tk.Toplevel(self.root)
        ventana_eventos = Reseña.InicioSesion(root2, self.root)
        self.root.withdraw()
        root2.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
        root2.mainloop()

    def boton_historial(self):
        print("Historial")
        root2 = tk.Toplevel(self.root)
        ventana_eventos = Historial.InicioSesion(root2, self.root)
        self.root.withdraw()
        root2.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
        root2.mainloop()

    def boton_experiencia(self):
        print("Experiencia")
        root2 = tk.Toplevel(self.root)
        ventana_eventos = Experiencia.Experiencia(root2, self.root)
        self.root.withdraw()
        root2.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
        root2.mainloop()

    def toggle_date_entry(self):
        # Mostrar u ocultar el campo de selección de fecha según el estado del checkbox
        if self.use_date_var.get():
            self.GLineEdit_date.place(x=230, y=208)
        else:
            self.GLineEdit_date.place_forget()

    def GButton_744_command(self):
        # Obtener el texto ingresado en el campo de búsqueda
        search_text = self.GLineEdit_search.get().lower()

        # Obtener la fecha ingresada en el campo de fecha si el checkbox está marcado
        selected_date = None
        if self.calendar_var.get():
            selected_date = self.GLineEdit_date.get_date()

        # Realizar la búsqueda en el archivo eventos.json
        with open("eventos.json", "r") as file:
            event_data = json.load(file)

        filtered_events = []
        for event_name, event_info in event_data.items():
            # Realizar búsqueda por texto
            if search_text in event_name.lower() or \
                    search_text in event_info["artista"].lower() or \
                    search_text in event_info["genero"].lower() or \
                    search_text in event_info["ubicacion"].lower():
                # Realizar búsqueda por fecha si se ingresó una fecha válida
                if selected_date is not None:
                    if "fecha" in event_info and event_info["fecha"] == selected_date.strftime("%Y-%m-%d"):
                        filtered_events.append((event_name, event_info))
                else:
                    filtered_events.append((event_name, event_info))

        # Limpiar el treeview antes de mostrar los resultados
        self.tree.delete(*self.tree.get_children())

        # Mostrar los resultados en el treeview
        for event_name, event_info in filtered_events:
            event_date = event_info.get("fecha", "")
            self.tree.insert("", "end", values=(event_name, event_info["artista"], event_info["genero"],
                                                event_info["ubicacion"], event_date))


    def cerrar_ventana(self):
        self.root.deiconify()  # Muestra la ventana principal
        self.root.destroy()  # Destruye la ventana principal


if __name__ == "__main__":
    root = tk.Tk()
    app = Principal(root)
    root.mainloop()