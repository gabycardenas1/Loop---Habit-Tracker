import json
from datetime import date
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image

from ui.reporte import reporte_general
from utils.procesamiento import guardar_datos, cargar_datos_existentes


def abrir_registro():
    # Muestra pantalla de registro y da paso a la visualización de reportes
    app = ctk.CTk()
    app.geometry("900x600")
    app.title("Loop - Registro de Hábitos")
    app.configure(fg_color="#f0f0f0")

    valores_registro = {}

    fecha_actual = str(date.today())
    usuario_actual = "admin"

    # Cargar datos del día si ya existen
    datos_existentes = cargar_datos_existentes(usuario_actual, fecha_actual)

    # Título
    titulo = ctk.CTkLabel(
        app,
        text="Registra tus hábitos de hoy",
        font=("Helvetica", 28, "bold"),
        text_color="#003366",
        fg_color="transparent"
    )
    titulo.pack(pady=(20, 10))

    subtitulo = ctk.CTkLabel(
        app,
        text="Completa los campos para registrar tu día. Loop te ayudará a visualizar tu progreso y mantener el ritmo.",
        font=("Helvetica", 16),
        text_color="#444444",
        fg_color="transparent",
        wraplength=700,
        justify="center"
    )
    subtitulo.pack(pady=(0, 15))

    # Área con scroll
    scroll_frame = ctk.CTkScrollableFrame(app, width=850, height=400, fg_color="#f0f0f0")
    scroll_frame.pack(pady=(0, 10))

    def crear_tarjeta(nombre, icono_path, contenido_widget, info_texto=""):
        frame = ctk.CTkFrame(master=scroll_frame, fg_color="white", width=800, height=130, corner_radius=15)
        frame.pack(pady=10, padx=20)

        img = ctk.CTkImage(Image.open(icono_path), size=(80, 80))
        ctk.CTkLabel(frame, image=img, text="", fg_color="transparent").place(x=15, y=25)

        ctk.CTkLabel(
            frame,
            text=nombre,
            font=("Helvetica", 18, "bold"),
            text_color="#003366",
            fg_color="transparent"
        ).place(x=110, y=25)

        contenido_widget(frame)

        if info_texto:
            ctk.CTkLabel(
                frame,
                text=info_texto,
                font=("Helvetica", 12),
                text_color="gray",
                fg_color="transparent",
                wraplength=200,
                justify="center"
            ).place(x=620, y=65, anchor="center")

    def agua_contenido(frame):
        cantidad = ctk.IntVar(value=datos_existentes.get("agua", 4))
        valores_registro["agua"] = cantidad

        def disminuir():
            cantidad.set(max(0, cantidad.get() - 1))

        def aumentar():
            cantidad.set(cantidad.get() + 1)

        ctk.CTkButton(frame, text="-", width=30, command=disminuir).place(x=110, y=60)
        ctk.CTkLabel(frame, textvariable=cantidad, font=("Helvetica", 16)).place(x=155, y=60)
        ctk.CTkButton(frame, text="+", width=30, command=aumentar).place(x=180, y=60)

        ctk.CTkLabel(frame, text="vasos de agua", font=("Helvetica", 14)).place(x=225, y=61)
        ctk.CTkLabel(frame, text="Cada vaso corresponde a 0.25L", font=("Helvetica", 12), text_color="gray").place(x=110, y=95)

    def ejercicio_contenido(frame):
        entry = ctk.CTkEntry(frame, placeholder_text="Ingrese una cantidad", width=140)
        entry.place(x=110, y=65)
        valores_registro["ejercicio"] = entry

        if "ejercicio" in datos_existentes:
            entry.insert(0, str(datos_existentes["ejercicio"]))

        ctk.CTkLabel(frame, text="minutos de ejercicio", font=("Helvetica", 14)).place(x=260, y=64)

    def lectura_contenido(frame):
        entry = ctk.CTkEntry(frame, placeholder_text="Ingrese una cantidad", width=140)
        entry.place(x=110, y=65)
        valores_registro["lectura"] = entry

        if "lectura" in datos_existentes:
            entry.insert(0, str(datos_existentes["lectura"]))

        ctk.CTkLabel(frame, text="minutos de lectura", font=("Helvetica", 14)).place(x=260, y=64)

    def animo_contenido(frame):
        ctk.CTkLabel(frame, text="Triste", font=("Helvetica", 12)).place(x=110, y=65)
        animo_var = ctk.IntVar(value=datos_existentes.get("animo", 0))
        valores_registro["animo"] = animo_var

        for i in range(1, 6):
            ctk.CTkRadioButton(frame, text=str(i), variable=animo_var, value=i).place(x=155 + (i - 1) * 45, y=68)

        ctk.CTkLabel(frame, text="Feliz", font=("Helvetica", 12)).place(x=380, y=65)

    def sueno_contenido(frame):
        entry = ctk.CTkEntry(frame, placeholder_text="Ingrese una cantidad", width=140)
        entry.place(x=110, y=65)
        valores_registro["sueno"] = entry

        if "sueno" in datos_existentes:
            entry.insert(0, str(datos_existentes["sueno"]))

        ctk.CTkLabel(frame, text="horas de descanso", font=("Helvetica", 14)).place(x=260, y=64)

    # Crear tarjetas
    crear_tarjeta("Sueño", "Recursos/Sueño.png", sueno_contenido, "Los adultos necesitan entre 7 y 9 horas de sueño por noche para mantener una buena salud física y mental.")
    crear_tarjeta("Estado de ánimo", "Recursos/Animo.png", animo_contenido, "Registrar tu estado emocional diariamente mejora la conciencia emocional y puede ayudarte a detectar patrones de bienestar o estrés.")
    crear_tarjeta("Lectura", "Recursos/Leer.png", lectura_contenido, "Leer al menos 15 minutos al día puede mejorar la concentración, reducir el estrés y aumentar la empatía.")
    crear_tarjeta("Agua", "Recursos/Agua.png", agua_contenido, "Beber 2L de agua al día mantiene tu cuerpo hidratado y tu mente activa.")
    crear_tarjeta("Ejercicio", "Recursos/Ejercicio.png", ejercicio_contenido, "Se recomienda al menos 150 minutos semanales de actividad física moderada para mejorar la salud cardiovascular y mental.")

    # Guardar datos
    def guardar_registro():
        try:
            datos = {
                "sueno": float(valores_registro["sueno"].get()),
                "animo": valores_registro["animo"].get(),
                "lectura": int(valores_registro["lectura"].get()),
                "agua": valores_registro["agua"].get(),
                "ejercicio": int(valores_registro["ejercicio"].get())
            }

            ok, error = guardar_datos(usuario_actual, fecha_actual, datos)
            if ok:
                messagebox.showinfo("Registro guardado", "Los hábitos de hoy se guardaron exitosamente.")
            else:
                messagebox.showerror("Error", f"Ocurrió un error al guardar:\n{error}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al preparar los datos:\n{e}")

    # Botones
    boton_frame = ctk.CTkFrame(app, fg_color="#f0f0f0")
    boton_frame.pack(pady=(0, 15))

    botones = [
        ("Guardar", guardar_registro),
        ("Ver mi progreso", lambda: [app.destroy(), reporte_general()])
    ]

    for texto, comando in botones:
        ctk.CTkButton(
            boton_frame,
            text=texto,
            width=180,
            height=40,
            fg_color="#003366",
            hover_color="#002244",
            command=comando
        ).pack(side="left", padx=10)

    app.mainloop()
