import pytest
from unittest.mock import patch, MagicMock
from app.services.ventas_service import VentaService


def test_calcular_comision():
    """
    Prueba que `_calcular_comision` invoque correctamente la creación de la comisión.

    Se valida que:
    - Se llama una sola vez a `ComisionRepo.create`.
    - Los datos enviados contienen el ID de la venta, porcentaje aplicado (10),
      y el monto correcto de comisión calculado como el 10% del valor de venta.
    """
    # Mock de venta con atributos esperados
    mock_venta = MagicMock()
    mock_venta.id = 1
    mock_venta.vendedor_id = 10
    with patch('app.services.ventas_service.VentaRepo.get_by_id', return_value=mock_venta), \
            patch('app.services.ventas_service.ComisionRepo.create') as mock_create:

        VentaService._calcular_comision(1, 10, 1000)

        mock_create.assert_called_once()
        args = mock_create.call_args[0][0]
        assert args['venta_id'] == 1
        assert args['porcentaje_aplicado'] == 10
        assert float(args['monto_comision']) == 100.0  # 10% de 1000


def test_registrar_pago_monto_valido(mocker):
    """
    Comprueba que `registrar_pago` registre un abono válido y actualice el estado de la venta.

    Este test simula:
    - Una venta con saldo pendiente y estado 'Vigente'.
    - Un abono parcial de 50 unidades monetarias.

    Se verifica que:
    - El pago se registre correctamente sin errores.
    - El resultado contenga el monto abonado esperado.
    """
    venta_mock = MagicMock()
    venta_mock.saldo_pendiente = 100
    venta_mock.estado_venta = 'Vigente'

    mocker.patch('app.services.ventas_service.VentaRepo.get_by_id',
                 return_value=venta_mock)
    mocker.patch('app.services.ventas_service.PagoRepo.create', return_value=(
        MagicMock(to_dict=lambda: {"monto_abono": 50}), None))
    mocker.patch('app.services.ventas_service.VentaRepo.update',
                 return_value=(venta_mock, None))

    pago_data = {
        "numero_recibo_caja": "RC123",
        "banco": "BancoTest",
        "numero_cuenta": "123456",
        "monto_abono": 50,
        "fecha_pago": "2025-06-26"
    }

    result, error = VentaService.registrar_pago(
        venta_id=1, pago_data=pago_data, usuario_creacion="admin")
    assert error is None
    assert result["monto_abono"] == 50


def test_create_venta_sin_detalles(mocker):
    """
    Verifica que `create_venta` retorne un error cuando no se proporcionan detalles de la venta.

    Se simula:
    - La existencia de cliente y vendedor válidos.
    - Una solicitud de creación de venta con una lista vacía de detalles.

    Se espera que:
    - La creación de la venta falle.
    - Se retorne un mensaje de error indicando que el campo 'detalles' es requerido.
    """
    mocker.patch('app.services.ventas_service.ClienteRepo.get',
                 return_value=MagicMock())
    mocker.patch('app.services.ventas_service.VendedorRepo.get_by_id',
                 return_value=MagicMock())

    venta_data = {
        "cliente_id": 1,
        "vendedor_id": 2,
        "tipo_pago": "Contado",
        "detalles": []
    }

    venta, error = VentaService.create_venta(venta_data)
    assert venta is None
    assert error == "Campo requerido: detalles"
