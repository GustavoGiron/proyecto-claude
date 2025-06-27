from unittest.mock import patch, MagicMock
from app.utils.emailalert import enviar_alerta_stock_bajo

def test_enviar_alerta_stock_bajo_envio_correcto():
    with patch("smtplib.SMTP") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        resultado = enviar_alerta_stock_bajo(
            producto_id="P001",
            stock_actual=5,
            nombre_producto="Producto Test",
            destinatarios="destinatario@example.com"
        )

        # Validar que se llamó al SMTP con los parámetros correctos
        mock_smtp.assert_called_with("smtp.example.com", 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_with("tarogg7@gmail.com", "contraseña1234")
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()

        # Como la función no retorna nada, el resultado es None
        assert resultado is None
