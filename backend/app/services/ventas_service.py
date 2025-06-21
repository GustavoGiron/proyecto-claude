from app.repositories.ventas_repo import VentaRepo, DetalleVentaRepo, PagoRepo, ComisionRepo
from app.repositories.clientes_repo import ClienteRepo
from app.repositories.vendedores_repo import VendedorRepo
from app.repositories.productos_repo import ProductoRepo
from app.services.inventario_service import InventarioService
from datetime import datetime, date
from decimal import Decimal

class VentaService:
    @staticmethod
    def get_all_ventas():
        ventas = VentaRepo.get_all()
        return [venta.to_dict() for venta in ventas]

    @staticmethod
    def get_venta_by_id(id):
        venta = VentaRepo.get_by_id(id)
        if not venta:
            return None
        
        venta_dict = venta.to_dict()
        # Agregar detalles de la venta
        detalles = DetalleVentaRepo.get_by_venta_id(id)
        venta_dict['detalles'] = [detalle.to_dict() for detalle in detalles]
        
        # Agregar pagos de la venta
        pagos = PagoRepo.get_by_venta_id(id)
        venta_dict['pagos'] = [pago.to_dict() for pago in pagos]
        
        return venta_dict

    @staticmethod
    def get_venta_by_numero_envio(numero_envio):
        venta = VentaRepo.get_by_numero_envio(numero_envio)
        if not venta:
            return None
        
        return VentaService.get_venta_by_id(venta.id)

    @staticmethod
    def create_venta(data, usuario_creacion=None):
        """Crea una venta completa con sus detalles"""
        required_fields = ['cliente_id', 'vendedor_id', 'tipo_pago', 'detalles']
        for field in required_fields:
            if not data.get(field):
                return None, f"Campo requerido: {field}"
        
        # Validar que existan cliente y vendedor
        cliente = ClienteRepo.get(data['cliente_id'])
        if not cliente:
            return None, "Cliente no encontrado"
        
        vendedor = VendedorRepo.get_by_id(data['vendedor_id'])
        if not vendedor:
            return None, "Vendedor no encontrado"
        
        # Validar detalles
        if not data['detalles'] or len(data['detalles']) == 0:
            return None, "Debe incluir al menos un producto en la venta"
        
        # Generar número de envío automático
        max_envio = VentaRepo.get_max_numero_envio()
        numero_envio = f"ENV{max_envio + 1:06d}"  # ENV000001, ENV000002, etc.
        
        # Preparar datos de la venta
        venta_data = {
            'numero_envio': numero_envio,
            'fecha_venta': datetime.fromisoformat(data['fecha_venta']).date() if isinstance(data.get('fecha_venta'), str) else data.get('fecha_venta', date.today()),
            'cliente_id': data['cliente_id'],
            'vendedor_id': data['vendedor_id'],
            'tipo_pago': data['tipo_pago'],
            'dias_credito': data.get('dias_credito', 0 if data['tipo_pago'] == 'Contado' else data.get('dias_credito', 0)),
            'numero_factura_dte': data.get('numero_factura_dte'),
            'nombre_factura': data.get('nombre_factura'),
            'nit_cliente': data.get('nit_cliente') or cliente.nit,
            'nit_factura': data.get('nit_factura') or cliente.nit,
            'estado_venta': 'Vigente',
            'estado_cobro': 'Pendiente',
            'estado_entrega': 'Pendiente',
            'usuario_creacion': usuario_creacion
        }
        
        # Calcular fecha de vencimiento si es crédito
        if venta_data['tipo_pago'] == 'Credito' and venta_data['dias_credito'] > 0:
            from datetime import timedelta
            venta_data['fecha_vencimiento'] = venta_data['fecha_venta'] + timedelta(days=venta_data['dias_credito'])
        
        # Validar stock y calcular totales
        subtotal = Decimal('0.00')
        iva_total = Decimal('0.00')
        detalles_procesados = []
        
        for detalle in data['detalles']:
            # Validar producto
            producto = ProductoRepo.get_by_id(detalle['producto_id'])
            if not producto:
                return None, f"Producto con ID {detalle['producto_id']} no encontrado"
            
            # Validar stock disponible
            inventario = InventarioService.get_inventario_by_producto_id(detalle['producto_id'])
            if not inventario:
                return None, f"No hay inventario para el producto {producto.nombre_producto}"
            
            cantidad_unidades = detalle['cantidad'] * producto.unidades_por_fardo_paquete
            if inventario['stock_disponible'] < cantidad_unidades:
                return None, f"Stock insuficiente para {producto.nombre_producto}. Disponible: {inventario['stock_disponible']}, Requerido: {cantidad_unidades}"
            
            # Calcular totales del detalle
            precio = Decimal(str(detalle['precio_por_fardo_paquete']))
            cantidad = detalle['cantidad']
            subtotal_linea = precio * cantidad
            iva_linea = subtotal_linea * Decimal('0.12')  # IVA 12%
            total_linea = subtotal_linea + iva_linea
            
            detalle_procesado = {
                'producto_id': detalle['producto_id'],
                'cantidad': cantidad,
                'cantidad_unidades': cantidad_unidades,
                'precio_por_fardo_paquete': precio,
                'subtotal_linea': subtotal_linea,
                'iva_linea': iva_linea,
                'total_linea': total_linea,
                'observaciones': detalle.get('observaciones'),
                'usuario_creacion': usuario_creacion
            }
            
            detalles_procesados.append(detalle_procesado)
            subtotal += subtotal_linea
            iva_total += iva_linea
        
        # Actualizar totales en la venta
        venta_data['subtotal_venta'] = subtotal
        venta_data['iva_venta'] = iva_total
        venta_data['total_venta'] = subtotal + iva_total
        venta_data['saldo_pendiente'] = subtotal + iva_total
        
        # Crear la venta
        venta, error = VentaRepo.create(venta_data)
        if error:
            return None, error
        
        # Crear los detalles
        for detalle_data in detalles_procesados:
            detalle_data['venta_id'] = venta.id
            detalle, error = DetalleVentaRepo.create(detalle_data)
            if error:
                return None, f"Error al crear detalle: {error}"
            
            # Apartar el stock (reservar productos)
            resultado, error_inventario = InventarioService.registrar_movimiento_inventario(
                detalle_data['producto_id'],
                'Apartado',
                detalle_data['cantidad_unidades'],
                referencia=f"Venta #{venta.numero_envio}",
                motivo=f"Productos apartados para venta",
                usuario=usuario_creacion
            )
            
            if error_inventario:
                return None, f"Error al apartar inventario: {error_inventario}"
        
        # Calcular y crear comisión
        VentaService._calcular_comision(venta.id, vendedor.porcentaje_comision, venta.total_venta)
        
        return VentaService.get_venta_by_id(venta.id), None

    @staticmethod
    def _calcular_comision(venta_id, porcentaje_comision, total_venta):
        """Crea el registro de comisión para la venta"""
        venta = VentaRepo.get_by_id(venta_id)
        if not venta:
            return
        
        comision_data = {
            'venta_id': venta_id,
            'vendedor_id': venta.vendedor_id,
            'total_neto_venta': total_venta,
            'porcentaje_aplicado': porcentaje_comision,
            'monto_comision': (Decimal(str(total_venta)) * Decimal(str(porcentaje_comision))) / Decimal('100'),
            'estado_comision': 'Pendiente'
        }
        
        ComisionRepo.create(comision_data)

    @staticmethod
    def registrar_salida_bodega(venta_id, fecha_salida, usuario_modificacion=None):
        """Registra la salida de productos de bodega y actualiza inventario"""
        venta = VentaRepo.get_by_id(venta_id)
        if not venta:
            return None, "Venta no encontrada"
        
        if venta.estado_entrega == 'Entregado':
            return None, "La venta ya fue entregada"
        
        # Convertir fecha si es string
        if isinstance(fecha_salida, str):
            fecha_salida = datetime.fromisoformat(fecha_salida).date()
        
        # Actualizar fecha de salida y estado de entrega
        venta_data = {
            'fecha_salida_bodega': fecha_salida,
            'estado_entrega': 'Entregado',
            'usuario_modificacion': usuario_modificacion
        }
        
        venta, error = VentaRepo.update(venta_id, venta_data)
        if error:
            return None, error
        
        # Procesar cada detalle para mover inventario de apartado a salida
        detalles = DetalleVentaRepo.get_by_venta_id(venta_id)
        for detalle in detalles:
            # Liberar productos apartados
            resultado, error_liberar = InventarioService.registrar_movimiento_inventario(
                detalle.producto_id,
                'Liberado',
                detalle.cantidad_unidades,
                referencia=f"Salida venta #{venta.numero_envio}",
                motivo="Liberación por salida de bodega",
                usuario=usuario_modificacion
            )
            
            if error_liberar:
                return None, f"Error al liberar apartado: {error_liberar}"
            
            # Registrar salida real
            resultado, error_salida = InventarioService.registrar_movimiento_inventario(
                detalle.producto_id,
                'Salida',
                detalle.cantidad_unidades,
                referencia=f"Salida venta #{venta.numero_envio}",
                motivo=f"Salida de bodega - Entrega a cliente",
                usuario=usuario_modificacion
            )
            
            if error_salida:
                return None, f"Error al registrar salida: {error_salida}"
            
            # Actualizar estado del detalle
            DetalleVentaRepo.update(detalle.id, {'estado_linea': 'Entregado'})
        
        return VentaService.get_venta_by_id(venta_id), None

    @staticmethod
    def registrar_pago(venta_id, pago_data, usuario_creacion=None):
        """Registra un pago para una venta"""
        venta = VentaRepo.get_by_id(venta_id)
        if not venta:
            return None, "Venta no encontrada"
        
        if venta.estado_venta == 'Anulada':
            return None, "No se puede registrar pago para una venta anulada"
        
        required_fields = ['numero_recibo_caja', 'banco', 'numero_cuenta', 'monto_abono']
        for field in required_fields:
            if not pago_data.get(field):
                return None, f"Campo requerido: {field}"
        
        monto_abono = Decimal(str(pago_data['monto_abono']))
        if monto_abono <= 0:
            return None, "El monto del abono debe ser mayor a cero"
        
        if monto_abono > venta.saldo_pendiente:
            return None, f"El monto del abono ({monto_abono}) no puede ser mayor al saldo pendiente ({venta.saldo_pendiente})"
        
        # Preparar datos del pago
        pago_data_processed = {
            'venta_id': venta_id,
            'numero_recibo_caja': pago_data['numero_recibo_caja'],
            'fecha_pago': datetime.fromisoformat(pago_data['fecha_pago']).date() if isinstance(pago_data.get('fecha_pago'), str) else pago_data.get('fecha_pago', date.today()),
            'banco': pago_data['banco'],
            'numero_cuenta': pago_data['numero_cuenta'],
            'numero_transferencia': pago_data.get('numero_transferencia'),
            'monto_abono': monto_abono,
            'saldo_anterior': venta.saldo_pendiente,
            'saldo_actual': venta.saldo_pendiente - monto_abono,
            'usuario_creacion': usuario_creacion
        }
        
        # Crear el pago
        pago, error = PagoRepo.create(pago_data_processed)
        if error:
            return None, error
        
        # Actualizar el saldo y estado de cobro de la venta
        nuevo_saldo = venta.saldo_pendiente - monto_abono
        
        if nuevo_saldo == 0:
            estado_cobro = 'Pagada'
            fecha_pago_completo = pago_data_processed['fecha_pago']
        elif nuevo_saldo > 0:
            estado_cobro = 'Parcial'
            fecha_pago_completo = None
        else:
            return None, "Error en el cálculo del saldo"
        
        venta_update = {
            'saldo_pendiente': nuevo_saldo,
            'estado_cobro': estado_cobro,
            'fecha_pago_completo': fecha_pago_completo,
            'usuario_modificacion': usuario_creacion
        }
        
        venta, error = VentaRepo.update(venta_id, venta_update)
        if error:
            return None, error
        
        return pago.to_dict(), None

    @staticmethod
    def search_ventas(numero_envio=None, cliente_nombre=None, estado_venta=None, estado_cobro=None):
        ventas = VentaRepo.search(numero_envio=numero_envio, cliente_nombre=cliente_nombre, 
                                  estado_venta=estado_venta, estado_cobro=estado_cobro)
        return [venta.to_dict() for venta in ventas]

    @staticmethod
    def get_ventas_pendientes_cobro():
        ventas = VentaRepo.get_ventas_pendientes_cobro()
        return [venta.to_dict() for venta in ventas]

    @staticmethod
    def get_ventas_pendientes_entrega():
        ventas = VentaRepo.get_ventas_pendientes_entrega()
        return [venta.to_dict() for venta in ventas]

    @staticmethod
    def anular_venta(venta_id, usuario_modificacion=None):
        """Anula una venta y libera el inventario apartado"""
        venta = VentaRepo.get_by_id(venta_id)
        if not venta:
            return None, "Venta no encontrada"
        
        if venta.estado_venta == 'Anulada':
            return None, "La venta ya está anulada"
        
        if venta.estado_entrega == 'Entregado':
            return None, "No se puede anular una venta que ya fue entregada"
        
        # Liberar productos apartados
        detalles = DetalleVentaRepo.get_by_venta_id(venta_id)
        for detalle in detalles:
            resultado, error_liberar = InventarioService.registrar_movimiento_inventario(
                detalle.producto_id,
                'Liberado',
                detalle.cantidad_unidades,
                referencia=f"Anulación venta #{venta.numero_envio}",
                motivo="Liberación por anulación de venta",
                usuario=usuario_modificacion
            )
            
            if error_liberar:
                return None, f"Error al liberar inventario: {error_liberar}"
        
        # Actualizar estado de la venta
        venta_data = {
            'estado_venta': 'Anulada',
            'usuario_modificacion': usuario_modificacion
        }
        
        venta, error = VentaRepo.update(venta_id, venta_data)
        if error:
            return None, error
        
        return VentaService.get_venta_by_id(venta_id), None

class ComisionService:
    @staticmethod
    def get_comisiones_by_vendedor(vendedor_id):
        comisiones = ComisionRepo.get_by_vendedor_id(vendedor_id)
        return [comision.to_dict() for comision in comisiones]

    @staticmethod
    def get_comisiones_pendientes():
        comisiones = ComisionRepo.get_comisiones_pendientes()
        return [comision.to_dict() for comision in comisiones]

    @staticmethod
    def marcar_comision_pagada(comision_id, fecha_pago, usuario_pago):
        """Marca una comisión como pagada"""
        comision_data = {
            'estado_comision': 'Pagada',
            'fecha_pago': datetime.fromisoformat(fecha_pago).date() if isinstance(fecha_pago, str) else fecha_pago,
            'usuario_pago': usuario_pago
        }
        
        comision, error = ComisionRepo.update(comision_id, comision_data)
        if error:
            return None, error
        
        return comision.to_dict(), None