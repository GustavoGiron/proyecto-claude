import pytest
from app.utils.emailalert import (
    construir_cuerpo_alerta,
    crear_mensaje_email
)
from email.mime.text import MIMEText

def test_construir_cuerpo_alerta():
    """
    Verifica que `construir_cuerpo_alerta` construya correctamente el cuerpo del mensaje
    de alerta con los datos suministrados.

    Este test comprueba que el cuerpo del mensaje contiene:
    - El ID del producto.
    - El stock actual.
    - El nombre del producto.
    - El stock mínimo.
    - El título de alerta 'ALERTA DE STOCK BAJO'.
    """
    producto_id = "P001"
    stock_actual = 3
    nombre_producto = "Teclado Mecánico"
    minimo = "10"

    cuerpo = construir_cuerpo_alerta(producto_id, stock_actual, nombre_producto, minimo)

    assert producto_id in cuerpo
    assert str(stock_actual) in cuerpo
    assert nombre_producto in cuerpo
    assert str(minimo) in cuerpo
    assert "ALERTA DE STOCK BAJO" in cuerpo

def test_crear_mensaje_email():
    """
    Valida que `crear_mensaje_email` construya un objeto de correo electrónico correcto.

    Se comprueba que:
    - Los campos 'From', 'To' y 'Subject' se asignan correctamente.
    - El cuerpo del mensaje esté presente y sea del tipo `MIMEText`.
    - El contenido del cuerpo coincida con el texto esperado.
    """
    from_email = "sistema@inventario.com"
    destinatarios = ["usuario@correo.com"]
    subject = "Test Subject"
    body = "Contenido de prueba"

    mensaje = crear_mensaje_email(from_email, destinatarios, subject, body)

    assert mensaje['From'] == from_email
    assert mensaje['To'] == ", ".join(destinatarios)
    assert mensaje['Subject'] == subject

    # Aseguramos que el cuerpo esté correctamente en el mensaje
    contenido = mensaje.get_payload()[0]
    assert isinstance(contenido, MIMEText)
    assert body in contenido.get_payload()
