from marshmallow import Schema, fields, validate, validates, ValidationError
from app import ma

class DetalleIngresoSchema(ma.Schema):
    """Schema para validar detalles de ingreso de mercancía"""
    id = fields.Integer(dump_only=True)
    producto_id = fields.Integer(required=True, validate=validate.Range(min=1))
    cantidad_fardos_paquetes = fields.Integer(required=True, validate=validate.Range(min=1))
    unidades_por_fardo_paquete = fields.Integer(required=True, validate=validate.Range(min=1))
    unidades_totales = fields.Integer(dump_only=True)
    usuario_creacion = fields.String(allow_none=True)
    
    # Información del producto (solo lectura)
    producto = fields.Nested({
        'id': fields.Integer(),
        'codigo_producto': fields.String(),
        'nombre_producto': fields.String()
    }, dump_only=True)

class IngresoMercanciaSchema(ma.Schema):
    """Schema para validar ingreso de mercancía"""
    id = fields.Integer(dump_only=True)
    fecha_ingreso = fields.Date(required=True)
    numero_contenedor = fields.String(required=True, validate=validate.Length(min=1, max=50))
    numero_duca = fields.String(required=True, validate=validate.Length(min=1, max=50))
    fecha_duca = fields.Date(required=True)
    numero_duca_rectificada = fields.String(allow_none=True, validate=validate.Length(max=50))
    fecha_duca_rectificada = fields.Date(allow_none=True)
    observaciones = fields.String(allow_none=True)
    usuario_creacion = fields.String(allow_none=True)
    
    # Detalles del ingreso
    detalles = fields.List(fields.Nested(DetalleIngresoSchema), dump_only=True)

class CrearIngresoMercanciaSchema(ma.Schema):
    """Schema para crear un ingreso de mercancía con sus detalles"""
    fecha_ingreso = fields.Date(required=True)
    numero_contenedor = fields.String(required=True, validate=validate.Length(min=1, max=50))
    numero_duca = fields.String(required=True, validate=validate.Length(min=1, max=50))
    fecha_duca = fields.Date(required=True)
    numero_duca_rectificada = fields.String(allow_none=True, validate=validate.Length(max=50))
    fecha_duca_rectificada = fields.Date(allow_none=True)
    observaciones = fields.String(allow_none=True)
    usuario_creacion = fields.String(allow_none=True)
    
    # Lista de detalles de productos
    detalles = fields.List(fields.Nested(DetalleIngresoSchema, exclude=['id']), required=True, validate=validate.Length(min=1))
    
    @validates('detalles')
    def validate_detalles(self, value, **kwargs):
        if not value:
            raise ValidationError('Debe incluir al menos un detalle de producto')

class ConfirmarIngresoSchema(ma.Schema):
    """Schema para confirmar un ingreso y actualizar inventarios"""
    aplicar_a_inventario = fields.Boolean(required=True)
    usuario_confirmacion = fields.String(allow_none=True)