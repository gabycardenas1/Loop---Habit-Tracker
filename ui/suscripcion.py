import customtkinter as ctk
from tkinter import messagebox, filedialog
import os, json
from datetime import datetime
from PIL import Image
from customtkinter import CTkImage
from utils.pdf import generarPdf
from utils.validaciones import validarCedula, validar_tarjeta, validar_clave_seguridad


def suscripcion():
    import customtkinter as ctk
    from tkinter import messagebox, filedialog
    from datetime import datetime
    import os, json
    from PIL import Image
    from customtkinter import CTkImage
    from utils.pdf import generarPdf
    from utils.validaciones import validarCedula, validar_tarjeta, validar_clave_seguridad

    # Ventana principal
    ventana = ctk.CTk()
    ventana.geometry("900x600")
    ventana.title("Suscripción Mensual")
    ventana.configure(fg_color="white")

    # ==== FRAME BASE IZQUIERDO ====
    frame_izq = ctk.CTkFrame(ventana, width=450, height=600, fg_color="white", corner_radius=0)
    frame_izq.pack(side="left", fill="y")

    # Imagen decorativa
    try:
        imagen = CTkImage(Image.open("Recursos/fondo.jpg"), size=(450, 600))
        ctk.CTkLabel(frame_izq, image=imagen, text="").pack()
    except:
        ctk.CTkLabel(frame_izq, text="Loop Reporte", text_color="black", font=("Helvetica", 28, "bold")).pack(expand=True)

    # ==== FRAME SCROLL DERECHO ====
    frame_scroll = ctk.CTkScrollableFrame(ventana, width=450, height=600, fg_color="white")
    frame_scroll.pack(side="right", fill="both", expand=True)

    # ==== TÍTULO ====
    ctk.CTkLabel(
        frame_scroll,
        text="Suscripción al Reporte Mensual",
        font=("Helvetica", 24, "bold"),
        text_color="#003366"
    ).pack(pady=(40, 5))

    ctk.CTkLabel(
        frame_scroll,
        text="Accede a tu progreso mensual y mantén tu motivación.\nSolo cuesta $3.99",
        font=("Helvetica", 14),
        text_color="#444444",
        wraplength=400,
        justify="center"
    ).pack(pady=(0, 25))

    # ==== CAMPOS ====
    def crear_campo(master, texto, oculto=False):
        ctk.CTkLabel(master, text=texto, font=("Helvetica", 16), text_color="#333").pack(pady=(5, 0))
        entrada = ctk.CTkEntry(master, width=350, show="*" if oculto else "")
        entrada.pack(pady=5)
        return entrada

    nombre = crear_campo(frame_scroll, "Nombre:")
    apellido = crear_campo(frame_scroll, "Apellido:")
    cedula = crear_campo(frame_scroll, "Cédula:")
    correo = crear_campo(frame_scroll, "Correo electrónico:")

    # ==== INFO DE PAGO ====
    ctk.CTkLabel(
        frame_scroll,
        text="Información de pago",
        font=("Helvetica", 16, "bold"),
        text_color="#003366"
    ).pack(pady=(30, 10))

    numero_tarjeta = crear_campo(frame_scroll, "Número de tarjeta:")
    clave_seguridad = crear_campo(frame_scroll, "Clave de seguridad:", oculto=True)

    # ==== BOTÓN DE SUSCRIPCIÓN ====
    def suscribirse():
        from ui.reporte import reporte_general

        datos = {
            "nombre": nombre.get().strip(),
            "apellido": apellido.get().strip(),
            "cedula": cedula.get().strip(),
            "correo": correo.get().strip(),
            "producto": "Suscripción Reporte Mensual Loop",
            "precio_unitario": 3.99,
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }

        if not all(datos.values()) or not numero_tarjeta.get().strip() or not clave_seguridad.get().strip():
            messagebox.showerror("Error", "Completa todos los campos.")
            return

        if not validarCedula(datos["cedula"]):
            messagebox.showerror("Error", "Cédula ecuatoriana no válida.")
            return

        if not validar_tarjeta(numero_tarjeta.get().strip()):
            messagebox.showerror("Error", "Número de tarjeta inválido.")
            return

        if not validar_clave_seguridad(clave_seguridad.get().strip()):
            messagebox.showerror("Error", "Clave de seguridad inválida (3 o 4 dígitos).")
            return

        confirmacion = messagebox.askyesno(
            "Confirmar",
            f"¿Confirmas el pago de ${datos['precio_unitario']:.2f}?"
        )

        if not confirmacion:
            return

        ruta = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            initialfile="factura_loop.pdf"
        )

        if ruta:
            generarPdf(datos, ruta)

            try:
                os.makedirs("data", exist_ok=True)
                with open("data/suscripcion.json", "w") as f:
                    json.dump({"reporte_habilitado": True}, f)
            except Exception as e:
                print("Error guardando suscripción:", e)

            messagebox.showinfo("Gracias", "¡Suscripción exitosa! Ahora puedes ver tu reporte mensual.")
            ventana.destroy()
            reporte_general(reporte_habilitado=True)

    ctk.CTkButton(
        frame_scroll,
        text="Suscribirme por $3.99",
        fg_color="#003366",
        hover_color="#001F33",
        font=("Helvetica", 18, "bold"),
        height=50,
        width=250,
        command=suscribirse
    ).pack(pady=25)

    # ==== BOTÓN ATRÁS ====
    def volver():
        from ui.reporte import reporte_general
        ventana.destroy()
        reporte_general()

    ctk.CTkButton(
        frame_scroll,
        text="Atrás",
        width=150,
        height=40,
        fg_color="white",
        border_width=2,
        border_color="#003366",
        text_color="#003366",
        hover_color="#e6e6e6",
        font=("Helvetica", 16),
        command=volver
    ).pack(pady=(0, 20))

    ventana.mainloop()
