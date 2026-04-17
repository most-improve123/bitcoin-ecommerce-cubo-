from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import qrcode
import io
import os
from datetime import datetime
import hashlib

def generate_invoice(customer_name, items, total_btc):
    # Crear un buffer para el PDF
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)

    # Datos de la factura
    invoice_id = hashlib.sha256(f"{customer_name}{datetime.now().timestamp()}".encode()).hexdigest()[:8]
    btc_address = "3FZbgi29cpjq2GjdwV8eyHuJJnkLtktZc5"  # Dirección de ejemplo
    current_date = datetime.now().strftime("%Y-%m-%d")

    # --- Generar el QR con la dirección Bitcoin, monto e ID de factura ---
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr_data = f"bitcoin:{btc_address}?amount={total_btc}&invoice={invoice_id}"
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # --- Guardar el QR en un archivo temporal ---
    qr_temp_path = "temp_qr.png"
    qr_img.save(qr_temp_path)

    # --- Encabezado de la factura ---
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, f"FACTURA - Bitcoin E-Commerce")
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"Cliente: {customer_name}")
    c.drawString(100, 700, f"Fecha: {current_date}")
    c.drawString(100, 680, f"ID Factura: {invoice_id}")

    # --- Tabla de productos ---
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 640, "Detalle de Compra:")
    c.line(50, 630, 550, 630)  # Línea horizontal

    # Encabezados de la tabla
    c.setFont("Helvetica-Bold", 10)
    c.drawString(60, 610, "Producto")
    c.drawString(250, 610, "Cantidad")
    c.drawString(350, 610, "Precio (BTC)")
    c.drawString(450, 610, "Total (BTC)")
    c.line(50, 600, 550, 600)  # Línea horizontal

    # Filas de productos
    c.setFont("Helvetica", 10)
    y_position = 580
    for item in items:
        c.drawString(60, y_position, item["name"])
        c.drawString(250, y_position, str(item["quantity"]))
        c.drawString(350, y_position, f"{item['price_btc']:.8f}")
        c.drawString(450, y_position, f"{item['total']:.8f}")
        y_position -= 20

    # --- Total ---
    c.line(50, y_position + 10, 550, y_position + 10)  # Línea horizontal
    c.setFont("Helvetica-Bold", 12)
    c.drawString(350, y_position - 10, f"TOTAL A PAGAR:")
    c.drawString(450, y_position - 10, f"{total_btc:.8f} BTC")

    # --- Instrucciones de pago ---
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position - 40, "Instrucciones de Pago:")
    c.setFont("Helvetica", 10)
    c.drawString(50, y_position - 60, "1. Escanea el código QR con tu billetera Bitcoin.")
    c.drawString(50, y_position - 80, f"2. Verifica que el monto sea {total_btc:.8f} BTC.")
    c.drawString(50, y_position - 100, f"3. Incluye este ID de factura como referencia: {invoice_id}")

    # --- Añadir el QR al PDF desde el archivo temporal ---
    c.drawImage(qr_temp_path, x=350, y=y_position - 150, width=120, height=120, preserveAspectRatio=True)
    c.setFont("Helvetica", 10)
    c.drawString(350, y_position - 170, f"Escanea el QR para pagar {total_btc:.8f} BTC.")
    c.drawString(350, y_position - 190, f"ID de factura: {invoice_id}")

    # --- Guardar el PDF ---
    c.save()
    pdf_buffer.seek(0)

    # Guardar en un archivo
    filename = f"factura_{customer_name.replace(' ', '_')}.pdf"
    with open(filename, "wb") as f:
        f.write(pdf_buffer.getvalue())

    # Eliminar el archivo temporal del QR
    os.remove(qr_temp_path)

    return filename