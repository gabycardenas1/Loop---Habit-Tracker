import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage

from ui.login import abrir_login  


def abrir_inicio():  
    # Función que muestra la pantalla inicial y la conecta con el módulo de seguridad o Login
    ventana = ctk.CTk()
    ventana.title("Loop - Inicio")
    ventana.geometry("900x600")
    ventana.configure(fg_color="white")
    ventana.resizable(False, False)

    try:
        resample = Image.Resampling.LANCZOS
    except AttributeError:
        resample = Image.ANTIALIAS

    logo = Image.open("Recursos/Logo Loop.png")
    logo_redimensionado = logo.resize((400, 400), resample) 
    imagen_logo = CTkImage(light_image=logo_redimensionado, size=(400, 400))

    label_logo = ctk.CTkLabel(master=ventana, image=imagen_logo, text="", fg_color="transparent")
    label_logo.place(relx=0.5, rely=0.35, anchor="center")

    boton_comenzar = ctk.CTkButton(
        master=ventana,
        text="Comenzar",
        fg_color="#003366",
        hover_color="#001F33",
        font=("Helvetica", 20, "bold"),
        command=lambda: [ventana.destroy(), abrir_login()],
        width=250,
        height=60
    )
    boton_comenzar.place(relx=0.5, rely=0.6, anchor="center")

    ventana.mainloop()
