from app import ma
from app.models.vendedores_model import Vendedor
from marshmallow import fields, validates, ValidationError

class VendedorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vendedor
        load_instance = True
        fields = (
            "id",
            "codigo_vendedor", 
            "nombres",
            "apellidos",
            "nombre_completo",
            "telefono",
            "direccion", 
            "porcentaje_comision",
            "fecha_modificacion",
            "usuario_creacion",
            "usuario_modificacion"
        )
    
    nombre_completo = fields.Method("get_nombre_completo")
    
    def get_nombre_completo(self, obj):
        return f"{obj.nombres} {obj.apellidos}"
    
    @validates('nombres')
    def validate_nombres(self, value):
        if not value or len(value.strip()) == 0:
            raise ValidationError('Los nombres son requeridos')
        if len(value) > 100:
            raise ValidationError('Los nombres no pueden exceder 100 caracteres')
    
    @validates('apellidos')
    def validate_apellidos(self, value):
        if not value or len(value.strip()) == 0:
            raise ValidationError('Los apellidos son requeridos')
        if len(value) > 100:
            raise ValidationError('Los apellidos no pueden exceder 100 caracteres')
    
    @validates('porcentaje_comision')
    def validate_porcentaje_comision(self, value):
        if value is None:
            raise ValidationError('El porcentaje de comisión es requerido')
        if value < 0 or value > 100:
            raise ValidationError('El porcentaje de comisión debe estar entre 0 y 100')
    
    @validates('telefono')
    def validate_telefono(self, value):
        if value and len(value) > 20:
            raise ValidationError('El teléfono no puede exceder 20 caracteres')
        # Validación opcional del formato 0000-0000
        if value and '-' in value:
            parts = value.split('-')
            if len(parts) != 2 or not all(part.isdigit() for part in parts):
                raise ValidationError('El formato de teléfono debe ser 0000-0000')
    
    @validates('codigo_vendedor')
    def validate_codigo_vendedor(self, value):
        if value and len(value) > 20:
            raise ValidationError('El código de vendedor no puede exceder 20 caracteres')