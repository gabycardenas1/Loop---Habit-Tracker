import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
from ui.registro import abrir_registro
from utils.procesamiento import crear_indicadores

def abrir_programa():
    # Función que muestra onboarding pre registro de hábitos.
    def dibujar_indicadores():
        for i, punto in enumerate(indicadores):
            punto.configure(fg_color="#003366" if i == indice_actual else "#D0D0D0")

    def actualizar_contenido():
        nueva_img = CTkImage(Image.open(instrucciones[indice_actual]["imagen"]), size=(200, 200))
        imagen_label.configure(image=nueva_img)
        texto_label.configure(text=instrucciones[indice_actual]["texto"])
        imagen_label.image = nueva_img
        dibujar_indicadores()
        actualizar_texto_boton_derecho()

    def siguiente():
        nonlocal indice_actual
        if indice_actual < total_paginas - 1:
            indice_actual += 1
            actualizar_contenido()
        else:
            programa.destroy()
            abrir_registro()

    def anterior():
        nonlocal indice_actual
        indice_actual = (indice_actual - 1) % total_paginas
        actualizar_contenido()

    def actualizar_texto_boton_derecho():
        # Cambia el texto al llegar a la última pantalla del onboarding
        texto = "Explorar Loop" if indice_actual == total_paginas - 1 else "Continuar"
        btn_derecho.configure(text=texto)
    
    programa = ctk.CTk()
    programa.geometry("900x600")
    programa.title("Instrucciones - Loop")
    programa.configure(fg_color="white")
    programa.resizable(False, False)

    instrucciones = [
        {
            "imagen": "Recursos/Estoicismo.png",
            "texto": (
                "Inspirado en el Estoicismo,\n"
                "Loop te ayuda a enfocarte en lo que sí puedes controlar:\n"
                "tus decisiones, tus hábitos, tu bienestar."
            )
        },
        {
            "imagen": "Recursos/Diario.png",
            "texto": (
                "Tus hábitos te construyen.\n"
                "Cada pequeña acción de hoy moldea tu futuro.\n"
                "Loop estará contigo en cada paso."
            )
        },
        {
            "imagen": "Recursos/Actividades.png",
            "texto": (
                "Cada vez que marcas un hábito, eliges cuidar de ti.\n"
                "Registra tus avances, celebra tu constancia."
            )
        }
    ]

    total_paginas = len(instrucciones)
    indicadores = []
    indice_actual = 0

    titulo = ctk.CTkLabel(
        master=programa,
        text="Bienvenido a Loop\nComienza a transformar tus hábitos",
        font=("Helvetica", 30, "bold"),
        text_color="#003366",
        fg_color="white"
    )
    titulo.place(relx=0.5, rely=0.12, anchor="center")

    imagen_label = ctk.CTkLabel(master=programa, text="", fg_color="white")
    imagen_label.place(relx=0.5, rely=0.4, anchor="center")

    texto_label = ctk.CTkLabel(
        master=programa,
        text="",
        font=("Helvetica", 20),
        text_color="#003366",
        fg_color="white"
    )
    texto_label.place(relx=0.5, rely=0.63, anchor="center")

    # Indicadores de progreso
    frame_indicadores = ctk.CTkFrame(programa, fg_color="transparent")
    frame_indicadores.place(relx=0.5, rely=0.75, anchor="center")
    indicadores = crear_indicadores(frame_indicadores, total_paginas)

    # Flechas de navegación
    flecha_izq_img = CTkImage(Image.open("Recursos/Flecha izquierda.png"), size=(90, 90))
    flecha_der_img = CTkImage(Image.open("Recursos/Flecha derecha.png"), size=(90, 90))

    ctk.CTkButton(
        master=programa,
        image=flecha_izq_img,
        text="",
        width=40,
        height=40,
        fg_color="transparent",
        hover_color="#e6e6e6",
        command=anterior
    ).place(relx=0.05, rely=0.5, anchor="center")

    ctk.CTkButton(
        master=programa,
        image=flecha_der_img,
        text="",
        width=40,
        height=40,
        fg_color="transparent",
        hover_color="#e6e6e6",
        command=siguiente
    ).place(relx=0.95, rely=0.5, anchor="center")

    # Botón izquierdo: Omitir
    ctk.CTkButton(
        master=programa,
        text="Omitir",
        fg_color="white",
        border_width=2,
        border_color="#003366",
        font=("Helvetica", 20),
        text_color="#003366",
        hover_color="#f2f2f2",
        width=200,
        height=50,
        command=lambda: programa.destroy() or abrir_registro()
    ).place(relx=0.33, rely=0.88, anchor="center")

    # Botón derecho: Continuar y Empezar
    btn_derecho = ctk.CTkButton(
        master=programa,
        text="Continuar",
        fg_color="#003366",
        hover_color="#001f33",
        font=("Helvetica", 20, "bold"),
        width=200,
        height=50,
        command=siguiente
    )
    btn_derecho.place(relx=0.66, rely=0.88, anchor="center")

    actualizar_contenido()
    programa.mainloop()
