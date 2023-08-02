import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from tkintermapview import TkinterMapView
from PIL import Image, ImageTk
import json
import os


class Local:
    def __init__(self, nombre, imagen, id_ubicacion):
        self.nombre = nombre
        self.imagen = imagen
        self.id_ubicacion = id_ubicacion

    def a_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def de_json(cls, datos_json):
        datos = json.loads(datos_json)
        return cls(**datos)

    @staticmethod
    def cargar_locales(archivo_json):
        with open(archivo_json, "r") as archivo:
            datos = json.load(archivo)
        return [Local.de_json(json.dumps(dato)) for dato in datos]


class Ubicacion:
    def __init__(self, id, latitud, longitud, direccion):
        self.id = id
        self.latitud = latitud
        self.longitud = longitud
        self.direccion = direccion

    def a_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def de_json(cls, datos_json):
        datos = json.loads(datos_json)
        return cls(**datos)

    @staticmethod
    def cargar_ubicaciones(archivo_json):
        with open(archivo_json, "r") as archivo:
            datos = json.load(archivo)
        return [Ubicacion.de_json(json.dumps(dato)) for dato in datos]


class VistaPrincipal:
    def __init__(self, root, seleccionar_local_callback=None, seleccionar_ubicacion_callback=None):
        self.root = root
        self.seleccionar_local_callback = seleccionar_local_callback
        self.seleccionar_ubicacion_callback = seleccionar_ubicacion_callback
        self.frame_mapa = tk.Frame(self.root, width=600, height=600)
        self.frame_mapa.pack(side='right')

        self.frame_locales = tk.Frame(self.root, width=300, height=600)
        self.frame_locales.pack(side='left', fill='both', expand=True)

        # Placeholder para el mapa
        self.mapa = TkinterMapView(self.frame_mapa, width=600, height=600, corner_radius=0)
        self.mapa.set_position(-24.7855768, -65.4165233)
        self.mapa.set_zoom(16)
        self.mapa.pack(side='right')

        # Listbox para los locales
        self.lista_locales = tk.Listbox(self.frame_locales)
        self.lista_locales.bind('<<ListboxSelect>>', seleccionar_local_callback)
        self.lista_locales.pack(fill='both', expand=True)

    def agregar_local(self, local):
        nombre = local.nombre
        self.lista_locales.insert(tk.END, nombre)

    def agregar_marcador_mapa(self, latitud, longitud, texto, imagen=None):
        return self.mapa.set_marker(latitud, longitud, text=texto, image=imagen,
                                    command=self.seleccionar_ubicacion_callback)


class ControladorPrincipal:
    def __init__(self, root):
        self.vista = VistaPrincipal(root, self.seleccionar_local, seleccionar_ubicacion)
        self.locales = Local.cargar_locales("locales.json")
        self.ubicaciones = Ubicacion.cargar_ubicaciones("ubicaciones.json")
        self.marcadores = []
        self.imagenes = []

        self.cargar_locales()
        self.cargar_imagenes()
        self.cargar_marcadores()

    def cargar_locales(self):
        for local in self.locales:
            self.vista.agregar_local(local)

    def cargar_imagenes(self):
        for local in self.locales:
            imagen_path = os.path.join("images", local.imagen)
            imagen = ImageTk.PhotoImage(Image.open(imagen_path).resize((200, 200)))
            self.imagenes.append(imagen)

    def cargar_marcadores(self):
        for ubicacion, local in zip(self.ubicaciones, self.locales):
            imagen = self.imagenes[ubicacion.id - 1]
            marcador = self.vista.agregar_marcador_mapa(ubicacion.latitud, ubicacion.longitud, local.nombre, imagen)
            marcador.hide_image(True)
            self.marcadores.append(marcador)

    def seleccionar_local(self, event):
        # Obtiene el índice del elemento seleccionado
        indice_seleccionado = self.vista.lista_locales.curselection()
        # Obtiene el local seleccionado
        local_seleccionado = self.locales[indice_seleccionado[0]]

        ubicacion_seleccionada = Ubicacion(0, 0, 0, "")

        # Busca la ubicación correspondiente al local seleccionado
        for ubicacion in self.ubicaciones:
            if ubicacion.id == local_seleccionado.id_ubicacion:
                ubicacion_seleccionada = ubicacion
                break

        # Centra el mapa en la ubicación seleccionada
        self.vista.mapa.set_position(ubicacion_seleccionada.latitud, ubicacion_seleccionada.longitud)

        print(f"Latitud: {ubicacion_seleccionada.latitud}, Longitud: {ubicacion_seleccionada.longitud}")


def seleccionar_ubicacion(marcador):
    if marcador.image_hidden is True:
        marcador.hide_image(False)
    else:
        marcador.hide_image(True)
    print("Ubicación seleccionada: ", marcador.text)

def abrir_ventana_mapa(ventana_principal):
    root2 = tk.Toplevel(ventana_principal)
    ventana_eventos = ControladorPrincipal(root2)
    ventana_principal.withdraw()
    root2.wait_window()  # Espera hasta que se cierre la ventana del mapa
    ventana_principal.deiconify()  # Muestra nuevamente la ventana principal



if __name__ == "__main__":
    root = tk.Tk()
    app = ControladorPrincipal(root)
    root.title("EventVibe - Mapas y Rutas")
    width = 900
    height = 600
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(alignstr)
    root.resizable(width=False, height=False)
    root.mainloop()
