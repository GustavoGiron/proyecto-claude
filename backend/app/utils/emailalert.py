# utils/email_notifier.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def enviar_alerta_stock_bajo(producto_id, stock_actual, producto_nombre): 
    """
    Actualmente solo se le envia el correo a un destinatario,
    pero se puede modificar para enviar a varios destinatarios.

    def enviar_alerta_stock_bajo(producto_id, stock_actual, nombre_producto, destinatarios):
    from_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    to_emails = destinatarios if isinstance(destinatarios, list) else [destinatarios]

    """
    from_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    to_email = os.getenv("EMAIL_RECEIVER")
    minimo_permitido = os.getenv("STOCK_MINIMO_ALERTA", "10")
    subject = f"Alerta de Stock Bajo"
    body = f"""
    ⚠️ ALERTA DE STOCK BAJO ⚠️
    
    Se ha detectado que el siguiente producto requiere reposición:
    
    • Código del producto: {producto_id}
    • Nombre del producto: {producto_nombre}
    • Cantidad actual en inventario: {stock_actual}
    • Cantidad mínima sugerida para reposición: {minimo_permitido}
    
    Por favor, realice la reposición correspondiente lo antes posible.
    
    Saludos,
    Sistema de Gestión de Inventario
    """

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(os.getenv("EMAIL_HOST"), int(os.getenv("EMAIL_PORT")))
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Error al enviar correo de alerta: {e}")
        