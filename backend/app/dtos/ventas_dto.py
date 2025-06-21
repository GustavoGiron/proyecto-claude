from app import ma
from app.models.ventas_model import Venta, DetalleVenta, Pago, Comision
from marshmallow import fields, validates, ValidationError, Schema
from datetime import date

class VentaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Venta
        load_instance = True
        fields = (
            "id",
            "fecha_venta",
            "fecha_salida_bodega", 
            "cliente_id",
            "nit_cliente",
            "numero_envio",
            "tipo_pago",
            "dias_credito",
            "fecha_vencimiento",
            "vendedor_id",
            "numero_factura_dte",
            "nombre_factura",
            "nit_factura",
            "subtotal_venta",
            "iva_venta",
            "total_venta",
            "estado_venta",
            "estado_cobro",
            "estado_entrega",
            "fecha_pago_completo",
            "saldo_pendiente",
            "fecha_modificacion",
            "usuario_creacion",
            "usuario_modificacion"
        )
    
    tipo_pago = fields.String(validate=lambda x: x in ['Contado', 'Credito'])
    
    @validates('cliente_id')
    def validate_cliente_id(self, value):
        if not value or value <= 0:
            raise ValidationError('El ID del cliente es requerido y debe ser mayor a 0')
    
    @validates('vendedor_id')
    def validate_vendedor_id(self, value):
        if not value or value <= 0:
            raise ValidationError('El ID del vendedor es requerido y debe ser mayor a 0')

class DetalleVentaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DetalleVenta
        load_instance = True
        fields = (
            "id",
            "venta_id",
            "producto_id",
            "cantidad",
            "cantidad_unidades",
            "precio_por_fardo_paquete",
            "subtotal_linea",
            "iva_linea",
            "total_linea",
            "estado_linea",
            "observaciones",
            "usuario_creacion"
        )
    
    @validates('producto_id')
    def validate_producto_id(self, value):
        if not value or value <= 0:
            raise ValidationError('El ID del producto es requerido y debe ser mayor a 0')
    
    @validates('cantidad')
    def validate_cantidad(self, value):
        if not value or value <= 0:
            raise ValidationError('La cantidad es requerida y debe ser mayor a 0')

class PagoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pago
        load_instance = True
        fields = (
            "id",
            "venta_id",
            "numero_recibo_caja",
            "fecha_pago",
            "banco",
            "numero_cuenta",
            "numero_transferencia",
            "monto_abono",
            "saldo_anterior",
            "saldo_actual",
            "fecha_creacion",
            "usuario_creacion"
        )
    
    banco = fields.String(validate=lambda x: x in ['Industrial', 'Banrural', 'G&T', 'BAM'])
    
    @validates('numero_recibo_caja')
    def validate_numero_recibo_caja(self, value):
        if not value or len(value.strip()) == 0:
            raise ValidationError('El número de recibo de caja es requerido')

class ComisionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comision
        load_instance = True
        fields = (
            "id",
            "venta_id",
            "vendedor_id", 
            "total_neto_venta",
            "porcentaje_aplicado",
            "monto_comision",
            "estado_comision",
            "fecha_generacion",
            "fecha_pago",
            "usuario_pago",
            "observaciones"
        )

# Esquemas para operaciones específicas
class CrearVentaSchema(Schema):
    fecha_venta = fields.Date(load_default=date.today)
    cliente_id = fields.Integer(required=True)
    vendedor_id = fields.Integer(required=True)
    tipo_pago = fields.String(required=True, validate=lambda x: x in ['Contado', 'Credito'])
    dias_credito = fields.Integer(load_default=0)
    numero_factura_dte = fields.String(allow_none=True)
    nombre_factura = fields.String(allow_none=True)
    nit_cliente = fields.String(allow_none=True)
    nit_factura = fields.String(allow_none=True)
    detalles = fields.List(fields.Nested('DetalleVentaCreateSchema'), required=True)
    
    @validates('detalles')
    def validate_detalles(self, value):
        if not value or len(value) == 0:
            raise ValidationError('Debe incluir al menos un producto en la venta')

class DetalleVentaCreateSchema(Schema):
    producto_id = fields.Integer(required=True)
    cantidad = fields.Integer(required=True)
    precio_por_fardo_paquete = fields.Decimal(required=True)
    observaciones = fields.String(allow_none=True)
    
    @validates('cantidad')
    def validate_cantidad(self, value):
        if value <= 0:
            raise ValidationError('La cantidad debe ser mayor a 0')
    
    @validates('precio_por_fardo_paquete')
    def validate_precio(self, value):
        if value <= 0:
            raise ValidationError('El precio debe ser mayor a 0')

class RegistrarSalidaSchema(Schema):
    fecha_salida_bodega = fields.Date(load_default=date.today)

class RegistrarPagoSchema(Schema):
    numero_recibo_caja = fields.String(required=True)
    fecha_pago = fields.Date(load_default=date.today)
    banco = fields.String(required=True, validate=lambda x: x in ['Industrial', 'Banrural', 'G&T', 'BAM'])
    numero_cuenta = fields.String(required=True)
    numero_transferencia = fields.String(allow_none=True)
    monto_abono = fields.Decimal(required=True)
    
    @validates('monto_abono')
    def validate_monto_abono(self, value):
        if value <= 0:
            raise ValidationError('El monto del abono debe ser mayor a 0')