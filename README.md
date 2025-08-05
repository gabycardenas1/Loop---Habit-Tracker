# 🌀 Loop — Habit Tracker App

**Loop** es una aplicación de escritorio desarrollada en Python que permite registrar, visualizar y seguir hábitos diarios saludables mediante una interfaz gráfica moderna y minimalista. Fue creada como proyecto final de la materia **Programación I**, con enfoque modular, énfasis en la experiencia de usuario y posibilidades de escalabilidad. Se tomó en cuenta la normativa PEP 8 para construir este aplicativo.

## 🚀 Funcionalidades principales

- Registro diario personalizado de hábitos: estado de ánimo, hidratación, ejercicio, lectura y sueño.
- Almacenamiento de datos estructurado por usuario y fecha (formato JSON).
- Visualización dinámica de reportes diarios y semanales con gráficos.
- Reporte mensual premium habilitado mediante sistema de suscripción simulado.
- Generación de factura PDF con validación de datos.
- Interfaz intuitiva con navegación fluida entre ventanas.

## 🛠️ Tecnologías utilizadas

- Python 3.10  
- customtkinter — interfaz gráfica personalizada  
- Pillow — manejo de imágenes  
- matplotlib — generación de gráficos  
- json, datetime, calendar, os — procesamiento de datos y lógica  
- reportlab — generación de facturas en PDF  

## 📁 Estructura del proyecto

HABIT TRACKER/  
├── data/  
│   ├── data.json              # Registros diarios de hábitos  
│   ├── session.json           # Control de sesión de usuario  
│   └── suscripcion.json       # Estado de suscripción  
│  
├── recursos/                  # Íconos e imágenes de interfaz  
│  
├── temp/                      # Gráficos temporales generados  
│   ├── agua_donut.png  
│   ├── animo_donut.png  
│   ├── ejercicio.png  
│   ├── lectura.png  
│   └── sueno.png  
│  
├── ui/                        # Módulos de interfaz y navegación  
│   ├── inicio.py              # Pantalla de bienvenida  
│   ├── instrucciones.py       # Pantalla de instrucciones  
│   ├── login.py               # Login y registro de usuarios  
│   ├── registro.py            # Registro diario de hábitos  
│   ├── reporte.py             # Reportes diario, semanal, mensual  
│   └── suscripcion.py         # Flujo de compra y validación  
│  
├── utils/                     # Funciones auxiliares  
│   ├── graficos.py            # Generación de gráficos  
│   ├── pdf.py                 # Generación de factura PDF  
│   ├── procesamiento.py       # Lectura y escritura en JSON  
│   └── validaciones.py        # Validaciones de formularios  
│  
├── main.py                    # Script principal que inicia la app  
└── README.md                  # Documentación general del proyecto


## 📦 Instalación

1. Instala las dependencias:  
   `pip install customtkinter pillow matplotlib reportlab`  

2. Ejecuta la aplicación:  
   `python main.py`

## 🙋‍♀️ Autora

**Gabriela Cárdenas**  
Estudiante de Ingeniería en Ciencias de Datos & Desarrollo de Software  
Universidad UTE (UTE)

## 📌 Dependencias

customtkinter  
pillow  
matplotlib  
reportlab