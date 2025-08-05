import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import calendar
import json
from datetime import date, datetime, timedelta

from ui.suscripcion import suscripcion
from utils.graficos import (
    graficar_animo, graficar_promAgua,
    graficar_ejercicio, graficar_lectura, graficar_sueno
)
from utils.procesamiento import cargar_grafico, crear_tarjeta


def reporte_general(reporte_habilitado=None):
    # Recibe el argumento incial como None para identificar si se debe mostrar o no reporte mensual
    if reporte_habilitado is None:
        try:
            with open("data/suscripcion.json", "r") as f:
                datos = json.load(f)
                reporte_habilitado = datos.get("reporte_habilitado", False)
        except:
            reporte_habilitado = False

    app = ctk.CTk()
    app.geometry("900x600")
    app.title("Reportes - Loop")
    app.configure(fg_color="white")
    app.resizable(False, False)
    
    usuario_actual = "admin"
    fecha_actual = date.today()
    anio, mes = fecha_actual.year, fecha_actual.month

    # Barra superior de navegación
    barra = ctk.CTkFrame(app, height=65, fg_color="#003366", corner_radius=0)
    barra.pack(fill="x", side="top")

    def salir():
        app.destroy()

    def cambiar_vista(vista):
        for widget in frame_contenido.winfo_children():
            widget.destroy()
        if vista == "diario":
            mostrar_reporte_diario()
        elif vista == "semanal":
            mostrar_reporte_semanal()
        elif vista == "mensual":
            if reporte_habilitado:
                mostrar_reporte_mensual()
            else:
                app.destroy()
                suscripcion()

    def volver_a_menu():
        from ui.registro import abrir_registro
        app.destroy()
        abrir_registro()

    flecha_img = ctk.CTkImage(Image.open("Recursos/flecha atras.png"), size=(25, 25))

    boton_atras = ctk.CTkButton(
    barra,
    image=flecha_img,
    text="",
    width=40,
    height=40,
    fg_color="transparent",          
    hover_color="#e6e6e6",    
    command=volver_a_menu
    )
    boton_atras.grid(row=0, column=0, padx=(10, 5), pady=10)

    boton_salir = ctk.CTkImage(Image.open("Recursos/Salir.png"), size=(25, 25))

    boton_salir = ctk.CTkButton(
    barra,
    image=boton_salir,
    text="",
    width=40,
    height=40,
    fg_color="transparent",          
    hover_color="#e6e6e6",     
    command=salir
    )
    boton_salir.grid(row=0, column=1, padx=(5, 5), pady=10)


    ctk.CTkButton(barra, text="Diario",
                fg_color="#003366", hover_color="#001F33",
                font=("Helvetica", 18, "bold"),
                width=120, height=45,
                command=lambda: cambiar_vista("diario")).place(x=270, y=10)

    ctk.CTkButton(barra, text="Semanal",
                fg_color="#003366", hover_color="#001F33",
                font=("Helvetica", 18, "bold"),
                width=120, height=45,
                command=lambda: cambiar_vista("semanal")).place(x=400, y=10)

    ctk.CTkButton(barra, text="Mensual",
                fg_color="#003366", hover_color="#001F33",
                font=("Helvetica", 18, "bold"),
                width=120, height=45,
                command=lambda: cambiar_vista("mensual")).place(x=530, y=10)

    logo_img = ctk.CTkImage(Image.open("Recursos/logo blanco y negro.png"), size=(60, 60))
    logo_label = ctk.CTkLabel(barra, image=logo_img, text="", fg_color="transparent")
    logo_label.place(x=830, y=0)

    # Configuración de contenedor
    frame_contenido = ctk.CTkFrame(app, fg_color="white")
    frame_contenido.pack(fill="both", expand=True)

    # REPORTE MENSUAL
    def mostrar_reporte_mensual():
        for widget in frame_contenido.winfo_children():
            widget.destroy()

        contenedor = ctk.CTkScrollableFrame(frame_contenido, fg_color="#f2f2f2", width=900, height=535)
        contenedor.pack(fill="both", expand=True)

        mes_anio = [date.today().month, date.today().year]  

        def actualizar_vista():
            for widget in contenedor.winfo_children():
                widget.destroy()

            mes = mes_anio[0]
            anio = mes_anio[1]

            # Título del mes con flechas
            titulo_frame = ctk.CTkFrame(contenedor, fg_color="#f2f2f2")
            titulo_frame.pack(pady=(5, 0))

            def mes_anterior():
                if mes_anio[0] == 1:
                    mes_anio[0] = 12
                    mes_anio[1] -= 1
                else:
                    mes_anio[0] -= 1
                actualizar_vista()

            def mes_siguiente():
                if mes_anio[0] == 12:
                    mes_anio[0] = 1
                    mes_anio[1] += 1
                else:
                    mes_anio[0] += 1
                actualizar_vista()

            ctk.CTkButton(titulo_frame, text="◀", width=30, height=30, font=("Helvetica", 16),
                        command=mes_anterior, fg_color="#e0e0e0", text_color="#003366").pack(side="left", padx=5)
            ctk.CTkLabel(titulo_frame, text=f"{calendar.month_name[mes]} {anio}",
                        font=("Helvetica", 20, "bold"), text_color="#003366").pack(side="left", padx=10)
            ctk.CTkButton(titulo_frame, text="▶", width=30, height=30, font=("Helvetica", 16),
                        command=mes_siguiente, fg_color="#e0e0e0", text_color="#003366").pack(side="left", padx=5)

            # Cargar datos del mes seleccionado
            def obtener_datos_mensuales(usuario="admin"):
                with open("data/data.json", "r") as f:
                    datos = json.load(f)
                registros = datos.get("usuarios", {}).get(usuario, {}).get("registros", {})

                mes = mes_anio[0]
                anio = mes_anio[1]
                dias_mes = calendar.monthrange(anio, mes)[1]
                datos_mes = []

                sumaAnimo = 0
                sumaAgua = 0
                contAnimo = 0
                contAgua = 0

                for dia in range(1, dias_mes + 1):
                    fecha = f"{anio}-{mes:02d}-{dia:02d}"
                    registro = registros.get(fecha, {})

                    animo = registro.get("animo", 0)
                    agua = registro.get("agua", 0)
                    ejercicio = registro.get("ejercicio", 0)
                    lectura = registro.get("lectura", 0)
                    sueno = registro.get("sueno", 0)

                    datos_mes.append({
                        "dia": dia,
                        "animo": animo,
                        "agua": agua,
                        "ejercicio": ejercicio,
                        "lectura": lectura,
                        "sueno": sueno
                    })

                    if animo:
                        sumaAnimo += animo
                        contAnimo += 1
                    if agua:
                        sumaAgua += agua
                        contAgua += 1

                promAnimo = round(sumaAnimo / contAnimo, 1) if contAnimo else 0
                promAgua = round(sumaAgua / contAgua, 1) if contAgua else 0

                return datos_mes, promAnimo, promAgua


            # Generar gráficos y tarjetas
            datos, promAnimo, promAgua = obtener_datos_mensuales("admin")
            graficar_animo(promAnimo)
            graficar_promAgua(promAgua)
            graficar_ejercicio(datos)
            graficar_lectura(datos)
            graficar_sueno(datos)

            fila_donuts = ctk.CTkFrame(contenedor, fg_color="#f2f2f2")
            fila_donuts.pack(pady=10)

            ancho_tarjeta = 420
            alto_tarjeta = 200
            tam_donut = 150

            def crear_tarjeta_donut(master, imagen, titulo, relx=0.5, rely=0.42):
                tarjeta = ctk.CTkFrame(master, width=ancho_tarjeta, height=alto_tarjeta, corner_radius=30, fg_color="white")
                tarjeta.pack_propagate(False)
                donut_label = ctk.CTkLabel(tarjeta, image=imagen, text="", fg_color="transparent")
                donut_label.place(relx=relx, rely=rely, anchor="center")
                texto = ctk.CTkLabel(tarjeta, text=titulo, font=("Helvetica", 16, "bold"), text_color="#003366")
                texto.place(relx=0.5, rely=0.85, anchor="center")
                return tarjeta

            tarjeta1 = crear_tarjeta_donut(fila_donuts, cargar_grafico("animo_donut.png", tam_donut, tam_donut), "Ánimo")
            tarjeta1.pack(side="left", padx=20)

            tarjeta2 = crear_tarjeta_donut(fila_donuts, cargar_grafico("agua_donut.png", tam_donut, tam_donut), "Agua")
            tarjeta2.pack(side="left", padx=20)

            tarjeta_ejercicio = crear_tarjeta(contenedor, cargar_grafico("ejercicio.png", 820, 270), ancho=860, alto=290)
            ctk.CTkLabel(tarjeta_ejercicio, text="Ejercicio", font=("Helvetica", 20, "bold"), text_color="#003366").place(relx=0.5, rely=0.07, anchor="center")
            tarjeta_ejercicio.pack(pady=(10, 20))

            tarjeta_lectura = crear_tarjeta(contenedor, cargar_grafico("lectura.png", 820, 270), ancho=860, alto=290)
            ctk.CTkLabel(tarjeta_lectura, text="Lectura", font=("Helvetica", 20, "bold"), text_color="#003366").place(relx=0.5, rely=0.07, anchor="center")
            tarjeta_lectura.pack(pady=(10, 20))

            tarjeta_sueno = crear_tarjeta(contenedor, cargar_grafico("sueno.png", 820, 270), ancho=860, alto=290)
            ctk.CTkLabel(tarjeta_sueno, text="Sueño", font=("Helvetica", 20, "bold"), text_color="#003366").place(relx=0.5, rely=0.07, anchor="center")
            tarjeta_sueno.pack(pady=(10, 30))

        actualizar_vista()


# REPORTE SEMANAL

    def mostrar_reporte_semanal():
        panel_izq = ctk.CTkFrame(frame_contenido, width=400, fg_color="#003366", corner_radius=0)
        panel_izq.pack(side="left", fill="y")

        ctk.CTkLabel(panel_izq, text="Últimos 7 días", font=("Helvetica", 26, "bold"),
                    text_color="white").place(x=30, y=30)

        ctk.CTkLabel(panel_izq, text="Promedio de tus hábitos", font=("Helvetica", 18, "bold"),
                    text_color="white").place(x=30, y=70)

        tarjetas = {}

        def crear_tarjeta(y, icono, clave, texto):
            frame = ctk.CTkFrame(panel_izq, fg_color="white", corner_radius=25, width=340, height=60)
            frame.place(x=30, y=y)
            img = ctk.CTkImage(Image.open(f"Recursos/{icono}"), size=(40, 40))
            icono_lbl = ctk.CTkLabel(frame, image=img, text="", fg_color="transparent")
            icono_lbl.image = img
            icono_lbl.place(x=15, y=8)
            txt_lbl = ctk.CTkLabel(frame, text=texto, font=("Helvetica", 14),
                                text_color="#003366", fg_color="transparent")
            txt_lbl.place(x=65, y=15)
            tarjetas[clave] = txt_lbl

        crear_tarjeta(130, "Animo.png", "animo", "")
        crear_tarjeta(200, "Agua.png", "agua", "")
        crear_tarjeta(270, "Ejercicio.png", "ejercicio", "")
        crear_tarjeta(340, "Sueño.png", "sueno", "")
        crear_tarjeta(410, "Leer.png", "lectura", "")

        panel_der = ctk.CTkFrame(frame_contenido, width=500, fg_color="#f5f5f5", corner_radius=0)
        panel_der.pack(side="right", fill="both", expand=True)

        try:
            with open("data/data.json", "r") as f:
                datos = json.load(f)
            registros = datos.get("usuarios", {}).get(usuario_actual, {}).get("registros", {})
        except:
            registros = {}

        hoy = date.today()
        ultimos_dias = [(hoy - timedelta(days=i)).isoformat() for i in range(7)]
        acumulados = {"animo": [], "agua": [], "ejercicio": [], "sueno": [], "lectura": []}

        for dia in ultimos_dias:
            registro = registros.get(dia, {})
            for k in acumulados:
                if k in registro:
                    acumulados[k].append(registro[k])

        def promedio(valores):
            return round(sum(valores) / len(valores), 1) if valores else 0

        tarjetas["animo"].configure(text=f"Ánimo promedio: {promedio(acumulados['animo'])}/5")
        tarjetas["agua"].configure(text=f"Agua promedio: {promedio(acumulados['agua'])} vasos")
        tarjetas["ejercicio"].configure(text=f"Ejercicio: {promedio(acumulados['ejercicio'])} min/día")
        tarjetas["sueno"].configure(text=f"Sueño: {promedio(acumulados['sueno'])} horas/día")
        tarjetas["lectura"].configure(text=f"Lectura: {promedio(acumulados['lectura'])} min/día")

        ctk.CTkLabel(panel_der, text="¡Sigue así! La constancia hace la diferencia.",
                    font=("Helvetica", 16), text_color="#003366",
                    wraplength=400, justify="center", fg_color="transparent").place(x=60, y=260)
        
        # Configuración calendario 
        hoy = date.today()
        mes_anio = [hoy.month, hoy.year]  
        botones_dias = {}
        dias_registrados = set()

        def actualizar_reporte_semanal(fecha):
            ultimos_dias = [(fecha - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]
            acumulados = {"animo": [], "agua": [], "ejercicio": [], "sueno": [], "lectura": []}

            for dia in ultimos_dias:
                registro = registros.get(dia, {})
                for k in acumulados:
                    if k in registro:
                        acumulados[k].append(registro[k])

            def promedio(valores):
                return round(sum(valores) / len(valores), 1) if valores else 0

            tarjetas["animo"].configure(text=f"Ánimo promedio: {promedio(acumulados['animo'])}/5")
            tarjetas["agua"].configure(text=f"Agua promedio: {promedio(acumulados['agua'])} vasos")
            tarjetas["ejercicio"].configure(text=f"Ejercicio: {promedio(acumulados['ejercicio'])} min/día")
            tarjetas["sueno"].configure(text=f"Sueño: {promedio(acumulados['sueno'])} horas/día")
            tarjetas["lectura"].configure(text=f"Lectura: {promedio(acumulados['lectura'])} min/día")

            for d, btn in botones_dias.items():
                if d == fecha.day:
                    btn.configure(fg_color="#0055aa", text_color="white")
                elif d in dias_registrados:
                    btn.configure(fg_color="#003366", text_color="white")
                else:
                    btn.configure(fg_color="white", text_color="#003366")

        def dibujar_calendario():
            for widget in panel_der.winfo_children():
                widget.destroy()

            mes, anio = mes_anio
            dias_registrados.clear()
            registros_dict = {}

            try:
                with open("data/data.json", "r") as f:
                    data = json.load(f)
                    registros_dict = data.get("usuarios", {}).get(usuario_actual, {}).get("registros", {})
                    for fecha_str_json in registros_dict:
                        dt = datetime.strptime(fecha_str_json, "%Y-%m-%d").date()
                        if dt.month == mes and dt.year == anio:
                            dias_registrados.add(dt.day)
            except:
                pass

            # Título
            nombre_mes = calendar.month_name[mes]
            ctk.CTkLabel(panel_der, text=f"{nombre_mes} {anio}", font=("Helvetica", 22, "bold"), text_color="#003366").place(x=200, y=30)

            def mes_anterior():
                if mes_anio[0] == 1:
                    mes_anio[0] = 12
                    mes_anio[1] -= 1
                else:
                    mes_anio[0] -= 1
                dibujar_calendario()

            def mes_siguiente():
                if mes_anio[0] == 12:
                    mes_anio[0] = 1
                    mes_anio[1] += 1
                else:
                    mes_anio[0] += 1
                dibujar_calendario()

            ctk.CTkButton(panel_der, text="◀", width=30, height=30, font=("Helvetica", 16),
                        command=mes_anterior, fg_color="#e0e0e0", text_color="#003366").place(x=30, y=25)
            ctk.CTkButton(panel_der, text="▶", width=30, height=30, font=("Helvetica", 16),
                        command=mes_siguiente, fg_color="#e0e0e0", text_color="#003366").place(x=440, y=25)

            cal = calendar.Calendar(firstweekday=0)
            semanas = cal.monthdayscalendar(anio, mes)

            botones_dias.clear()

            for fila, semana in enumerate(semanas):
                for col, dia in enumerate(semana):
                    if dia == 0:
                        continue
                    fecha_dia = date(anio, mes, dia)

                    color = "white"
                    texto_color = "#003366"
                    if fecha_dia == hoy:
                        color = "#cce6ff"
                    if dia in dias_registrados:
                        color = "#003366"
                        texto_color = "white"
                    if dia == hoy.day and mes == hoy.month and anio == hoy.year:
                        color = "#0055aa"

                    btn = ctk.CTkButton(panel_der, text=str(dia),
                                        font=("Helvetica", 14, "bold"),
                                        fg_color=color, text_color=texto_color,
                                        corner_radius=20, width=40, height=40,
                                        command=lambda d=dia: actualizar_reporte_semanal(date(anio, mes, d)))
                    btn.place(x=30 + col * 60, y=90 + fila * 55)
                    botones_dias[dia] = btn

            ctk.CTkLabel(panel_der, text="¡Sigue así! La constancia hace la diferencia.",
                        font=("Helvetica", 15), text_color="#003366",
                        wraplength=400, justify="center", fg_color="transparent").place(x=70, y=450)

            actualizar_reporte_semanal(hoy)

        dibujar_calendario()


    # REPORTE DIARIO
    def mostrar_reporte_diario():
        panel_izq = ctk.CTkFrame(frame_contenido, width=400, fg_color="#003366", corner_radius=0)
        panel_izq.pack(side="left", fill="y")

        titulo_lbl = ctk.CTkLabel(panel_izq, text="¡Tu día en Loop!",
                                font=("Helvetica", 26, "bold"), text_color="white")
        titulo_lbl.place(x=30, y=30)

        fecha_lbl = ctk.CTkLabel(panel_izq, font=("Helvetica", 18, "bold"),
                                text_color="white")
        fecha_lbl.place(x=30, y=70)

        tarjetas = {}

        def crearTarjeta(y, icono, clave, texto):
            frame = ctk.CTkFrame(panel_izq, fg_color="white", corner_radius=25, width=340, height=60)
            frame.place(x=30, y=y)
            img = ctk.CTkImage(Image.open(f"Recursos/{icono}"), size=(40, 40))
            icono_lbl = ctk.CTkLabel(frame, image=img, text="", fg_color="transparent")
            icono_lbl.image = img
            icono_lbl.place(x=15, y=8)
            txt_lbl = ctk.CTkLabel(frame, text=texto, font=("Helvetica", 14),
                                text_color="#003366", fg_color="transparent")
            txt_lbl.place(x=65, y=15)
            tarjetas[clave] = txt_lbl

        crearTarjeta(130, "Animo.png", "animo", "")
        crearTarjeta(200, "Agua.png", "agua", "")
        crearTarjeta(270, "Ejercicio.png", "ejercicio", "")
        crearTarjeta(340, "Sueño.png", "sueno", "")
        crearTarjeta(410, "Leer.png", "lectura", "")

        panel_der = ctk.CTkFrame(frame_contenido, width=500, fg_color="#f5f5f5", corner_radius=0)
        panel_der.pack(side="right", fill="both", expand=True)

        hoy = date.today()
        mes_anio = [hoy.month, hoy.year]  # [mes, año]

        botones_dias = {}

        def dibujar_calendario():
            for widget in panel_der.winfo_children():
                widget.destroy()

            mes, anio = mes_anio
            dias_registrados = set()
            registros_dict = {}

            try:
                with open("data/data.json", "r") as f:
                    data = json.load(f)
                    registros_dict = data.get("usuarios", {}).get(usuario_actual, {}).get("registros", {})
                    for fecha_str_json in registros_dict:
                        dt = datetime.strptime(fecha_str_json, "%Y-%m-%d").date()
                        if dt.month == mes and dt.year == anio:
                            dias_registrados.add(dt.day)
            except:
                pass

            def actualizar_reporte(fecha):
                fecha_lbl.configure(text=f"El {fecha.strftime('%d-%m-%Y')}:")
                registro = registros_dict.get(fecha.isoformat(), {})

                tarjetas["animo"].configure(text=f"Estuviste {registro.get('animo', '—')}/5")
                tarjetas["agua"].configure(text=f"Tomaste {registro.get('agua', '—')} vasos")
                tarjetas["ejercicio"].configure(text=f"Hiciste {registro.get('ejercicio', '—')} min de ejercicio")
                tarjetas["sueno"].configure(text=f"Dormiste {registro.get('sueno', '—')} horas")
                tarjetas["lectura"].configure(text=f"Leíste {registro.get('lectura', '—')} min en el día")

                for d, btn in botones_dias.items():
                    if d == fecha.day:
                        btn.configure(fg_color="#0055aa", text_color="white")
                    elif d in dias_registrados:
                        btn.configure(fg_color="#003366", text_color="white")
                    else:
                        btn.configure(fg_color="white", text_color="#003366")

            # Título de mes y navegación
            nombre_mes = calendar.month_name[mes]
            titulo = ctk.CTkLabel(panel_der, text=f"{nombre_mes} {anio}", font=("Helvetica", 22, "bold"), text_color="#003366")
            titulo.place(x=200, y=30)

            def mes_anterior():
                if mes_anio[0] == 1:
                    mes_anio[0] = 12
                    mes_anio[1] -= 1
                else:
                    mes_anio[0] -= 1
                dibujar_calendario()

            def mes_siguiente():
                if mes_anio[0] == 12:
                    mes_anio[0] = 1
                    mes_anio[1] += 1
                else:
                    mes_anio[0] += 1
                dibujar_calendario()

            ctk.CTkButton(panel_der, text="◀", width=30, height=30, font=("Helvetica", 16),
                        command=mes_anterior, fg_color="#e0e0e0", text_color="#003366").place(x=30, y=25)
            ctk.CTkButton(panel_der, text="▶", width=30, height=30, font=("Helvetica", 16),
                        command=mes_siguiente, fg_color="#e0e0e0", text_color="#003366").place(x=440, y=25)

            cal = calendar.Calendar(firstweekday=0)
            semanas = cal.monthdayscalendar(anio, mes)

            botones_dias.clear()

            for fila, semana in enumerate(semanas):
                for col, dia in enumerate(semana):
                    if dia == 0:
                        continue
                    fecha_dia = date(anio, mes, dia)

                    color = "white"
                    texto_color = "#003366"
                    if fecha_dia == hoy:
                        color = "#cce6ff"
                    if dia in dias_registrados:
                        color = "#003366"
                        texto_color = "white"
                    if dia == hoy.day and mes == hoy.month and anio == hoy.year:
                        color = "#0055aa"

                    btn = ctk.CTkButton(panel_der, text=str(dia),
                                        font=("Helvetica", 14, "bold"),
                                        fg_color=color, text_color=texto_color,
                                        corner_radius=20, width=40, height=40,
                                        command=lambda d=dia: actualizar_reporte(date(anio, mes, d)))
                    btn.place(x=30 + col * 60, y=90 + fila * 55)
                    botones_dias[dia] = btn

            ctk.CTkLabel(panel_der, text="Tu constancia te está acercando a tu mejor versión.",
                        font=("Helvetica", 15), text_color="#003366",
                        wraplength=400, justify="center", fg_color="transparent").place(x=70, y=450)

            if date(anio, mes, hoy.day).month == hoy.month and date(anio, mes, hoy.day).year == hoy.year:
                actualizar_reporte(hoy)

        dibujar_calendario()

    mostrar_reporte_diario()
    app.mainloop()
