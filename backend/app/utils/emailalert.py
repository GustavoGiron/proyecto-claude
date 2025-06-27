# utils/emailalert.py

import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


load_dotenv()

def construir_cuerpo_alerta(producto_id, stock_actual, nombre_producto, minimo_permitido):
    return f"""
    ⚠️ ALERTA DE STOCK BAJO ⚠️

    Se ha detectado que el siguiente producto requiere reposición:

    • Código del producto: {producto_id}
    • Nombre del producto: {nombre_producto}
    • Cantidad actual en inventario: {stock_actual}
    • Cantidad mínima sugerida para reposición: {minimo_permitido}

    Por favor, realice la reposición correspondiente lo antes posible.

    Saludos,
    Sistema de Gestión de Inventario
    """

def crear_mensaje_email(from_email, to_emails, subject, body):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    return msg

def enviar_email(from_email, password, to_emails, mensaje, smtp_host, smtp_port):
    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(from_email, password)
    server.sendmail(from_email, to_emails, mensaje.as_string())
    server.quit()

def enviar_alerta_stock_bajo(producto_id, stock_actual, nombre_producto, destinatarios):
    if isinstance(destinatarios, str):
        destinatarios = [destinatarios]
    elif not destinatarios:
        print("No hay destinatarios válidos.")
        return False

    from_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    smtp_host = os.getenv("EMAIL_HOST")
    smtp_port = int(os.getenv("EMAIL_PORT"))
    minimo_permitido = os.getenv("STOCK_MINIMO_ALERTA", "100")
    
    subject = "Alerta de Stock Bajo"
    body = construir_cuerpo_alerta(producto_id, stock_actual, nombre_producto, minimo_permitido)
    mensaje = crear_mensaje_email(from_email, destinatarios, subject, body)

    try:
        enviar_email(from_email, password, destinatarios, mensaje, smtp_host, smtp_port)
        return True
    except Exception as e:
        print(f"Error al enviar correo de alerta: {e}")
        return False

