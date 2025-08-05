from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generarPdf(datos, ruta):
    # Genera factura PDF con datos proporcionados
    c = canvas.Canvas(ruta, pagesize=letter)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(220, 750, "FACTURA")
    c.setFont("Helvetica", 12)
    c.drawString(50, 730, "Empresa: Loop - Habit Tracker")
    c.drawString(50, 715, "Dirección: Quito, Ecuador")
    c.drawString(50, 700, "Teléfono: 0998308306")

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 670, "Datos del Cliente")
    c.setFont("Helvetica", 12)
    c.drawString(50, 650, f"Nombre: {datos['nombre']} {datos['apellido']}")
    c.drawString(50, 635, f"Cédula: {datos['cedula']}")
    c.drawString(50, 620, f"Correo: {datos['correo']}")

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 590, "Detalle de la Compra")
    c.line(50, 580, 550, 580)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, 565, "Producto")
    c.drawString(300, 565, "Precio")
    c.line(50, 560, 550, 560)

    c.setFont("Helvetica", 12)
    c.drawString(60, 545, datos['producto'])
    c.drawString(300, 545, f"${datos['precio_unitario']:.2f}")

    c.line(50, 530, 550, 530)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, 510, "TOTAL:")
    c.drawString(300, 510, f"${datos['precio_unitario']:.2f}")

    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 480, f"Fecha de emisión: {datos['fecha']}")
    c.line(50, 470, 550, 470)
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 455, "Gracias por tu compra y por confiar en Loop - Habit Tracker.")

    c.save()
