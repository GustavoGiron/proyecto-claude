from app import ma
from app.models.productos_model import Producto
from marshmallow import fields, validates, ValidationError

class ProductoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Producto
        load_instance = True
        fields = (
            "id", 
            "codigo_producto", 
            "nombre_producto", 
            "unidad_medida",
            "unidades_por_fardo_paquete",
            "stock_minimo",
            "fecha_modificacion",
            "usuario_creacion",
            "usuario_modificacion"
        )
    
    unidad_medida = fields.String(validate=lambda x: x in ['Unidad', 'Fardo', 'Paquete'])
    
    @validates('codigo_producto')
    def validate_codigo_producto(self, value):
        if not value or len(value.strip()) == 0:
            raise ValidationError('El código del producto es requerido')
        if len(value) > 50:
            raise ValidationError('El código del producto no puede exceder 50 caracteres')
    
    @validates('nombre_producto')
    def validate_nombre_producto(self, value):
        if not value or len(value.strip()) == 0:
            raise ValidationError('El nombre del producto es requerido')
        if len(value) > 200:
            raise ValidationError('El nombre del producto no puede exceder 200 caracteres')
