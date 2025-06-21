from app import db
from datetime import datetime, date
from sqlalchemy import CheckConstraint

class Venta(db.Model):
    __tablename__ = 'Ventas'
    
    id = db.Column('Id', db.Integer, primary_key=True, autoincrement=True)
    fecha_venta = db.Column('FechaVenta', db.Date, nullable=False, default=date.today)
    fecha_salida_bodega = db.Column('FechaSalidaBodega', db.Date)
    cliente_id = db.Column('ClienteId', db.Integer, db.ForeignKey('Clientes.Id'), nullable=False)
    nit_cliente = db.Column('NitCliente', db.String(15))
    numero_envio = db.Column('NumeroEnvio', db.String(50), nullable=False, unique=True)
    tipo_pago = db.Column('TipoPago', db.String(10), nullable=False)
    dias_credito = db.Column('DiasCredito', db.Integer, nullable=False, default=0)
    fecha_vencimiento = db.Column('FechaVencimiento', db.Date)
    vendedor_id = db.Column('VendedorId', db.Integer, db.ForeignKey('Vendedores.Id'), nullable=False)
    numero_factura_dte = db.Column('NumeroFacturaDTE', db.String(50))
    nombre_factura = db.Column('NombreFactura', db.String(200))
    nit_factura = db.Column('NitFactura', db.String(15))
    subtotal_venta = db.Column('SubtotalVenta', db.Numeric(12,2), nullable=False, default=0)
    iva_venta = db.Column('IvaVenta', db.Numeric(12,2), nullable=False, default=0)
    total_venta = db.Column('TotalVenta', db.Numeric(12,2), nullable=False, default=0)
    estado_venta = db.Column('EstadoVenta', db.String(20), nullable=False, default='Vigente')
    estado_cobro = db.Column('EstadoCobro', db.String(20), nullable=False, default='Pendiente')
    estado_entrega = db.Column('EstadoEntrega', db.String(20), nullable=False, default='Pendiente')
    fecha_pago_completo = db.Column('FechaPagoCompleto', db.Date)
    saldo_pendiente = db.Column('SaldoPendiente', db.Numeric(12,2), nullable=False, default=0)
    fecha_modificacion = db.Column('FechaModificacion', db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    usuario_creacion = db.Column('UsuarioCreacion', db.String(50))
    usuario_modificacion = db.Column('UsuarioModificacion', db.String(50))
    
    __table_args__ = (
        CheckConstraint(tipo_pago.in_(['Contado', 'Credito']), name='check_tipo_pago'),
        CheckConstraint(estado_venta.in_(['Vigente', 'Anulada']), name='check_estado_venta'),
        CheckConstraint(estado_cobro.in_(['Pendiente', 'Parcial', 'Pagada', 'Morosa']), name='check_estado_cobro'),
        CheckConstraint(estado_entrega.in_(['Pendiente', 'Entregado']), name='check_estado_entrega'),
    )
    
    # Relaciones
    cliente = db.relationship('Cliente', backref='ventas', lazy='select')
    vendedor = db.relationship('Vendedor', backref='ventas', lazy='select')
    
    def to_dict(self):
        return {
            'id': self.id,
            'fecha_venta': self.fecha_venta.isoformat() if self.fecha_venta else None,
            'fecha_salida_bodega': self.fecha_salida_bodega.isoformat() if self.fecha_salida_bodega else None,
            'cliente_id': self.cliente_id,
            'nit_cliente': self.nit_cliente,
            'numero_envio': self.numero_envio,
            'tipo_pago': self.tipo_pago,
            'dias_credito': self.dias_credito,
            'fecha_vencimiento': self.fecha_vencimiento.isoformat() if self.fecha_vencimiento else None,
            'vendedor_id': self.vendedor_id,
            'numero_factura_dte': self.numero_factura_dte,
            'nombre_factura': self.nombre_factura,
            'nit_factura': self.nit_factura,
            'subtotal_venta': float(self.subtotal_venta) if self.subtotal_venta else 0.0,
            'iva_venta': float(self.iva_venta) if self.iva_venta else 0.0,
            'total_venta': float(self.total_venta) if self.total_venta else 0.0,
            'estado_venta': self.estado_venta,
            'estado_cobro': self.estado_cobro,
            'estado_entrega': self.estado_entrega,
            'fecha_pago_completo': self.fecha_pago_completo.isoformat() if self.fecha_pago_completo else None,
            'saldo_pendiente': float(self.saldo_pendiente) if self.saldo_pendiente else 0.0,
            'fecha_modificacion': self.fecha_modificacion.isoformat() if self.fecha_modificacion else None,
            'usuario_creacion': self.usuario_creacion,
            'usuario_modificacion': self.usuario_modificacion
        }

class DetalleVenta(db.Model):
    __tablename__ = 'DetalleVentas'
    
    id = db.Column('Id', db.Integer, primary_key=True, autoincrement=True)
    venta_id = db.Column('VentaId', db.Integer, db.ForeignKey('Ventas.Id'), nullable=False)
    producto_id = db.Column('ProductoId', db.Integer, db.ForeignKey('Productos.Id'), nullable=False)
    cantidad = db.Column('Cantidad', db.Integer, nullable=False)
    cantidad_unidades = db.Column('CantidadUnidades', db.Integer, nullable=False, default=0)
    precio_por_fardo_paquete = db.Column('PrecioPorFardoPaquete', db.Numeric(10,2), nullable=False)
    subtotal_linea = db.Column('SubtotalLinea', db.Numeric(12,2), nullable=False)
    iva_linea = db.Column('IvaLinea', db.Numeric(12,2), nullable=False, default=0)
    total_linea = db.Column('TotalLinea', db.Numeric(12,2), nullable=False)
    estado_linea = db.Column('EstadoLinea', db.String(20), nullable=False, default='Pendiente')
    observaciones = db.Column('Observaciones', db.Text)
    usuario_creacion = db.Column('UsuarioCreacion', db.String(50))
    
    __table_args__ = (
        CheckConstraint(estado_linea.in_(['Pendiente', 'Entregado']), name='check_estado_linea'),
    )
    
    # Relaciones
    venta = db.relationship('Venta', backref='detalles', lazy='select')
    producto = db.relationship('Producto', backref='detalles_venta', lazy='select')
    
    def to_dict(self):
        return {
            'id': self.id,
            'venta_id': self.venta_id,
            'producto_id': self.producto_id,
            'cantidad': self.cantidad,
            'cantidad_unidades': self.cantidad_unidades,
            'precio_por_fardo_paquete': float(self.precio_por_fardo_paquete) if self.precio_por_fardo_paquete else 0.0,
            'subtotal_linea': float(self.subtotal_linea) if self.subtotal_linea else 0.0,
            'iva_linea': float(self.iva_linea) if self.iva_linea else 0.0,
            'total_linea': float(self.total_linea) if self.total_linea else 0.0,
            'estado_linea': self.estado_linea,
            'observaciones': self.observaciones,
            'usuario_creacion': self.usuario_creacion
        }

class Pago(db.Model):
    __tablename__ = 'Pagos'
    
    id = db.Column('Id', db.Integer, primary_key=True, autoincrement=True)
    venta_id = db.Column('VentaId', db.Integer, db.ForeignKey('Ventas.Id'), nullable=False)
    numero_recibo_caja = db.Column('NumeroReciboCaja', db.String(50), nullable=False)
    fecha_pago = db.Column('FechaPago', db.Date, nullable=False, default=date.today)
    banco = db.Column('Banco', db.String(50), nullable=False)
    numero_cuenta = db.Column('NumeroCuenta', db.String(30), nullable=False)
    numero_transferencia = db.Column('NumeroTransferencia', db.String(50))
    monto_abono = db.Column('MontoAbono', db.Numeric(12,2), nullable=False)
    saldo_anterior = db.Column('SaldoAnterior', db.Numeric(12,2), nullable=False)
    saldo_actual = db.Column('SaldoActual', db.Numeric(12,2), nullable=False)
    fecha_creacion = db.Column('FechaCreacion', db.DateTime, default=datetime.utcnow)
    usuario_creacion = db.Column('UsuarioCreacion', db.String(50))
    
    # Relaciones
    venta = db.relationship('Venta', backref='pagos', lazy='select')
    
    def to_dict(self):
        return {
            'id': self.id,
            'venta_id': self.venta_id,
            'numero_recibo_caja': self.numero_recibo_caja,
            'fecha_pago': self.fecha_pago.isoformat() if self.fecha_pago else None,
            'banco': self.banco,
            'numero_cuenta': self.numero_cuenta,
            'numero_transferencia': self.numero_transferencia,
            'monto_abono': float(self.monto_abono) if self.monto_abono else 0.0,
            'saldo_anterior': float(self.saldo_anterior) if self.saldo_anterior else 0.0,
            'saldo_actual': float(self.saldo_actual) if self.saldo_actual else 0.0,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'usuario_creacion': self.usuario_creacion
        }

class Comision(db.Model):
    __tablename__ = 'Comisiones'
    
    id = db.Column('Id', db.Integer, primary_key=True, autoincrement=True)
    venta_id = db.Column('VentaId', db.Integer, db.ForeignKey('Ventas.Id'), nullable=False)
    vendedor_id = db.Column('VendedorId', db.Integer, db.ForeignKey('Vendedores.Id'), nullable=False)
    total_neto_venta = db.Column('TotalNetoVenta', db.Numeric(12,2), nullable=False)
    porcentaje_aplicado = db.Column('PorcentajeAplicado', db.Numeric(5,2), nullable=False)
    monto_comision = db.Column('MontoComision', db.Numeric(12,2), nullable=False)
    estado_comision = db.Column('EstadoComision', db.String(20), nullable=False, default='Pendiente')
    fecha_generacion = db.Column('FechaGeneracion', db.DateTime, default=datetime.utcnow)
    fecha_pago = db.Column('FechaPago', db.Date)
    usuario_pago = db.Column('UsuarioPago', db.String(50))
    observaciones = db.Column('Observaciones', db.Text)
    
    __table_args__ = (
        CheckConstraint(estado_comision.in_(['Pendiente', 'Pagada']), name='check_estado_comision'),
    )
    
    # Relaciones
    venta = db.relationship('Venta', backref='comisiones', lazy='select')
    vendedor = db.relationship('Vendedor', backref='comisiones', lazy='select')
    
    def to_dict(self):
        return {
            'id': self.id,
            'venta_id': self.venta_id,
            'vendedor_id': self.vendedor_id,
            'total_neto_venta': float(self.total_neto_venta) if self.total_neto_venta else 0.0,
            'porcentaje_aplicado': float(self.porcentaje_aplicado) if self.porcentaje_aplicado else 0.0,
            'monto_comision': float(self.monto_comision) if self.monto_comision else 0.0,
            'estado_comision': self.estado_comision,
            'fecha_generacion': self.fecha_generacion.isoformat() if self.fecha_generacion else None,
            'fecha_pago': self.fecha_pago.isoformat() if self.fecha_pago else None,
            'usuario_pago': self.usuario_pago,
            'observaciones': self.observaciones
        }