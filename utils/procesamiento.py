import json
import calendar
import os
from datetime import datetime
from PIL import Image
from customtkinter import CTkImage
import customtkinter as ctk


def cargar_grafico(nombre_archivo, ancho, alto):
    ruta = os.path.join("temp", nombre_archivo)  
    return ctk.CTkImage(Image.open(ruta), size=(ancho, alto))


def crear_tarjeta(master, grafico, ancho=400, alto=200):
    tarjeta = ctk.CTkFrame(master, width=ancho, height=alto, corner_radius=30, fg_color="white")
    tarjeta.pack_propagate(False)
    label = ctk.CTkLabel(tarjeta, image=grafico, text="", fg_color="transparent")
    label.place(relx=0.5, rely=0.5, anchor="center")
    return tarjeta


def obtener_datos_usuario(usuario="admin"):
    try:
        with open("data/data.json", "r") as f:
            datos = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return [], 0, 0

    registros = datos.get("usuarios", {}).get(usuario, {}).get("registros", {})

    hoy = datetime.now()
    anio, mes_num = hoy.year, hoy.month
    dias_mes = calendar.monthrange(anio, mes_num)[1]

    datos_mes = []
    suma_animo = suma_agua = cont_animo = cont_agua = 0

    for dia in range(1, dias_mes + 1):
        fecha = f"{anio}-{mes_num:02d}-{dia:02d}"
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
            suma_animo += animo
            cont_animo += 1
        if agua:
            suma_agua += agua
            cont_agua += 1

    prom_animo = round(suma_animo / cont_animo, 1) if cont_animo else 0
    prom_agua = round(suma_agua / cont_agua, 1) if cont_agua else 0

    return datos_mes, prom_animo, prom_agua

def crear_indicadores(frame, total):
    indicadores = []
    for _ in range(total):
        punto = ctk.CTkLabel(frame, width=12, height=12, text="", fg_color="#D0D0D0", corner_radius=6)
        punto.pack(side="left", padx=5)
        indicadores.append(punto)
    return indicadores

def guardar_datos(usuario_actual, fecha_actual, nuevos_datos, ruta="data/data.json"):
    try:
        if os.path.exists(ruta):
            with open(ruta, "r") as f:
                data = json.load(f)
        else:
            data = {"usuarios": {}}

        data.setdefault("usuarios", {})
        data["usuarios"].setdefault(usuario_actual, {"password": "", "registros": {}})
        data["usuarios"][usuario_actual]["registros"][fecha_actual] = nuevos_datos

        with open(ruta, "w") as f:
            json.dump(data, f, indent=4)
        return True, None
    except Exception as e:
        return False, str(e)
    
def cargar_datos_existentes(usuario, fecha, ruta="data/data.json"):
    try:
        with open(ruta, "r") as f:
            data = json.load(f)
        return data.get("usuarios", {}).get(usuario, {}).get("registros", {}).get(fecha, {})
    except:
        return {}
    
