import tkinter as tk
import tkinter.font as tkFont
import Principal
from ttkthemes import ThemedStyle
from tkinter import ttk

class App:
    def __init__(self, root):
        # setting title
        root.title("EventVibe")
        # setting window size
        width = 600
        height = 505
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLabel_912 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=78)
        GLabel_912["font"] = ft
        GLabel_912["fg"] = "#333333"
        GLabel_912["justify"] = "center"
        GLabel_912["text"] = "EventVibe"
        GLabel_912.place(x=80, y=150, width=463, height=103)

        self.botonIniciar = tk.Button(bg="#f0f0f0", cursor="arrow", font="Times 10", fg="#000000", justify="center", text="INICIAR", command=self.boton_iniciar)
        #self.botonIniciar = ttk.Button( cursor="arrow", text="INICIAR", command=self.boton_iniciar)
        self.botonIniciar.place(x=240, y=300, width=125, height=51)

        """style = ThemedStyle(root)
        style.set_theme("ubuntu")"""

    def boton_iniciar(self):
        print("funciona")
        root2 = tk.Toplevel(root)  # Crea una nueva ventana de nivel superior
        ventana_principal = Principal.Principal(root2)  # Instancia la clase Principal
        root.withdraw()  # Oculta la ventana principal
        root2.protocol("WM_DELETE_WINDOW", self.cerrar_ventana_principal)  # Maneja el cierre de la ventana principal
        root2.mainloop()

    def cerrar_ventana_principal(self):
        root.deiconify()  # Muestra la ventana principal
        root.destroy()  # Destruye la ventana principal


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = App(root)
        root.mainloop()
    except:
        print("Programa finalizado")