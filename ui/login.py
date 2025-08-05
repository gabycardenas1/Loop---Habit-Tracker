import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import messagebox
from PIL import Image
import json
import os

from ui.instrucciones import abrir_programa


def abrir_login():
    # Función que muestra Login y da paso a las instrucciones.
    app = ctk.CTk()
    app.title("Loop - Login")
    app.geometry("900x600")
    app.resizable(False, False)

    # Configuración de paneles izquierdo y derecho
    frame_izquierdo = ctk.CTkFrame(app, width=450, height=600, fg_color="#004aad", corner_radius=0)
    frame_izquierdo.place(x=0, y=0)

    frame_derecho = ctk.CTkFrame(app, width=450, height=600, fg_color="#ffffff", corner_radius=0)
    frame_derecho.place(x=450, y=0)

    # Frame izquierdo
    try:
        resample = Image.Resampling.LANCZOS
    except AttributeError:
        resample = Image.ANTIALIAS

    logo_img = Image.open("Recursos/logo blanco y negro.png")
    logo_resized = logo_img.resize((200, 200), resample)
    logo_ctk = CTkImage(light_image=logo_resized, dark_image=logo_resized, size=(200, 200))

    ctk.CTkLabel(frame_izquierdo, image=logo_ctk, text="", fg_color="transparent").place(relx=0.5, rely=0.3, anchor="center")
    ctk.CTkLabel(frame_izquierdo, text="¡Bienvenido a Loop!", text_color="white",
                 font=("Helvetica", 28, "bold"), fg_color="transparent").place(relx=0.5, rely=0.45, anchor="center")
    ctk.CTkLabel(frame_izquierdo,
                 text="Crea el hábito. Mide el cambio. \nConsulta reportes diarios, semanales o \nmensuales y alcanza tus metas.",
                 text_color="white", font=("Helvetica", 16), fg_color="transparent", justify="center"
                 ).place(relx=0.5, rely=0.6, anchor="center")

    # Frame derecho
    ctk.CTkLabel(frame_derecho, text="Bienvenido de nuevo", text_color="#003366",
                 font=("Helvetica", 25, "bold"), fg_color="transparent").place(relx=0.5, y=120, anchor="center")

    ctk.CTkLabel(frame_derecho, text="Hazlo fácil, hazlo diario.", text_color="#666666",
                 font=("Helvetica", 15), fg_color="transparent").place(relx=0.5, y=160, anchor="center")

    center_x = 225
    entry_width = 300

    entry_usuario = ctk.CTkEntry(frame_derecho, width=entry_width, font=("Helvetica", 16),
                                  placeholder_text="Correo o usuario")
    entry_usuario.place(x=center_x - entry_width // 2, y=200)

    entry_password = ctk.CTkEntry(frame_derecho, width=entry_width, font=("Helvetica", 16),
                                   show="*", placeholder_text="Contraseña")
    entry_password.place(x=center_x - entry_width // 2, y=250)

    intentos_restantes = [3]

    def iniciar_sesion():
        usuario = entry_usuario.get().strip()
        password = entry_password.get().strip()

        if not usuario or not password:
            messagebox.showwarning("Advertencia", "Debe llenar ambos campos.")
            return

        if intentos_restantes[0] <= 0:
            messagebox.showerror("Bloqueado", "Ya no te quedan intentos.")
            return

        ruta_data = os.path.join("data", "data.json")
        ruta_session = os.path.join("data", "session.json")

        if os.path.exists(ruta_data):
            with open(ruta_data, "r") as f:
                data = json.load(f)
        else:
            data = {"usuarios": {}}

        usuarios = data.get("usuarios", {})

        if usuario in usuarios and usuarios[usuario]["password"] == password:
            with open(ruta_session, "w") as f:
                json.dump({"usuario_actual": usuario}, f)

            app.destroy()
            abrir_programa()
        else:
            intentos_restantes[0] -= 1
            messagebox.showerror("Error", f"Credenciales incorrectas. Intentos restantes: {intentos_restantes[0]}")

    ctk.CTkButton(frame_derecho, text="Iniciar sesión", fg_color="#003366", hover_color="#000000",
                  font=("Helvetica", 16, "bold"), width=250, height=45,
                  command=iniciar_sesion).place(relx=0.5, y=330, anchor="center")

    ctk.CTkButton(frame_derecho, text="Salir", fg_color="white", border_width=2, border_color="#003366",
                  font=("Helvetica", 16), text_color="#003366", hover_color="#f2f2f2",
                  width=250, height=45, command=app.destroy).place(relx=0.5, y=390, anchor="center")

    ctk.CTkLabel(frame_derecho, text="By GC", text_color="#666666",
                 font=("Helvetica", 12), fg_color="transparent", cursor="hand2").place(relx=0.5, y=580, anchor="center")

    app.mainloop()
