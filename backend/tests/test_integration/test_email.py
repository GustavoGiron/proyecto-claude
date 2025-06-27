from app.utils.emailalert import enviar_alerta_stock_bajo
import os
from dotenv import load_dotenv

def test_enviar_alerta_stock_bajo_real_envio():
    load_dotenv(dotenv_path=".env")

    resultado = enviar_alerta_stock_bajo(
        producto_id="PRUEBA001",
        stock_actual=5,
        nombre_producto="Producto de prueba",
        destinatarios=os.getenv("EMAIL_USER")
    )

    assert resultado is True