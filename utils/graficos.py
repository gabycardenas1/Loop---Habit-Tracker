import matplotlib.pyplot as plt
import os

def crear_directorio_temp():
    if not os.path.exists("temp"):
        os.makedirs("temp")

# Gráfico de dona moderno con valor en el centro
def graficar_donut_con_valor(promedio, nombreArchivo, color="#44C3DA"):
    crear_directorio_temp()
    valores = [promedio, 5 - promedio if nombreArchivo == "animo_donut.png" else max(8 - promedio, 0)]
    colores = [color, "#D9D9D9"]

    fig, ax = plt.subplots(figsize=(4, 4))
    wedges, _ = ax.pie(valores, startangle=90, colors=colores,
                       wedgeprops=dict(width=0.3), counterclock=False)

    ax.text(0, 0, f"{round(promedio)}", ha='center', va='center',
            fontsize=22, fontweight='bold', color='black')

    ax.set(aspect="equal")
    plt.tight_layout()
    plt.savefig(f"temp/{nombreArchivo}", transparent=True)
    plt.close()

def graficar_animo(promedio):
    graficar_donut_con_valor(promedio, "animo_donut.png", "#44C3DA")

def graficar_promAgua(promedio):
    graficar_donut_con_valor(promedio, "agua_donut.png", "#66d9e8")

# Línea: solo ejercicio por día (estilo limpio)
def graficar_ejercicio(datos_dias):
    crear_directorio_temp()
    dias = list(range(1, len(datos_dias) + 1))
    ejercicio = [d.get("ejercicio", 0) for d in datos_dias]

    fig, ax = plt.subplots(figsize=(7.5, 2.3))
    ax.plot(dias, ejercicio, color='#2C3E50', marker='o', markersize = 4)

    ax.set_xticks(dias)
    ax.tick_params(axis='x', labelsize=7)
    ax.tick_params(axis='y', labelsize=7)

    ax.legend(fontsize=9, frameon=False)

    # Ejes limpios y modernos
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#999999")
    ax.spines["bottom"].set_color("#999999")

    plt.tight_layout()
    plt.savefig("temp/ejercicio.png", transparent=True)
    plt.close()

# Barras: lectura por día (minimalista)
def graficar_lectura(datos_dias):
    crear_directorio_temp()
    dias = list(range(1, len(datos_dias) + 1))
    lectura = [d.get("lectura", 0) for d in datos_dias]

    fig, ax = plt.subplots(figsize=(7.5, 2.3))
    ax.bar(dias, lectura, color=['#003366' if i % 2 == 0 else '#6c8db9' for i in dias])

    ax.set_xticks(dias)
    ax.tick_params(axis='x', labelsize=7)
    ax.tick_params(axis='y', labelsize=7)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#999999")
    ax.spines["bottom"].set_color("#999999")

    plt.tight_layout()
    plt.savefig("temp/lectura.png", transparent=True)
    plt.close()

# Área: sueño por día (sin grid)
def graficar_sueno(datos_dias):
    crear_directorio_temp()
    dias = list(range(1, len(datos_dias) + 1))
    sueno = [d.get("sueno", 0) for d in datos_dias]

    fig, ax = plt.subplots(figsize=(7.5, 2.3))
    ax.fill_between(dias, sueno, color='#66d9e8', alpha=0.6)
    ax.plot(dias, sueno, color="#547494")

    ax.set_xticks(dias)
    ax.tick_params(axis='x', labelsize=7)
    ax.tick_params(axis='y', labelsize=7)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#999999")
    ax.spines["bottom"].set_color("#999999")

    plt.tight_layout()
    plt.savefig("temp/sueno.png", transparent=True)
    plt.close()
