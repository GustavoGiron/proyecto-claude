from app import ma
from app.models.inventario_model import Inventario, MovimientoInventario, IngresoMercancia, DetalleIngresoMercancia
from marshmallow import fields, validates, ValidationError

class InventarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventario
        load_instance = True
        fields = (
            "id", 
            "producto_id", 
            "stock_disponible", 
            "stock_apartado",
            "stock_total",
            "fecha_ultima_actualizacion",
            "usuario_ultima_actualizacion",
            "producto"
        )
    
    @validates('producto_id')
    def validate_producto_id(self, value):
        if not value or value <= 0:
            raise ValidationError('El ID del producto es requerido y debe ser mayor a 0')
    
    @validates('stock_disponible')
    def validate_stock_disponible(self, value):
        if value is not None and value < 0:
            raise ValidationError('El stock disponible no puede ser negativo')
    
    @validates('stock_apartado')
    def validate_stock_apartado(self, value):
        if value is not None and value < 0:
            raise ValidationError('El stock apartado no puede ser negativo')

class MovimientoInventarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MovimientoInventario
        load_instance = True
        fields = (
            "id",
            "producto_id",
            "tipo_movimiento",
            "cantidad",
            "stock_anterior",
            "stock_nuevo",
            "referencia",
            "motivo",
            "fecha_movimiento",
            "usuario_movimiento",
            "producto"
        )
    
    tipo_movimiento = fields.String(validate=lambda x: x in ['Ingreso', 'Salida', 'Ajuste', 'Apartado', 'Liberado'])
    
    @validates('producto_id')
    def validate_producto_id(self, value):
        if not value or value <= 0:
            raise ValidationError('El ID del producto es requerido y debe ser mayor a 0')
    
    @validates('cantidad')
    def validate_cantidad(self, value):
        if not value or value <= 0:
            raise ValidationError('La cantidad es requerida y debe ser mayor a 0')
    
    @validates('stock_anterior')
    def validate_stock_anterior(self, value):
        if value is None or value < 0:
            raise ValidationError('El stock anterior es requerido y no puede ser negativo')
    
    @validates('stock_nuevo')
    def validate_stock_nuevo(self, value):
        if value is None or value < 0:
            raise ValidationError('El stock nuevo es requerido y no puede ser negativo')

class IngresoMercanciaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = IngresoMercancia
        load_instance = True
        fields = (
            "id",
            "fecha_ingreso",
            "numero_contenedor",
            "numero_duca",
            "fecha_duca",
            "numero_duca_rectificada",
            "fecha_duca_rectificada",
            "observaciones",
            "usuario_creacion",
            "detalles"
        )
    
    @validates('numero_contenedor')
    def validate_numero_contenedor(self, value):
        if not value or len(value.strip()) == 0:
            raise ValidationError('El número de contenedor es requerido')
        if len(value) > 50:
            raise ValidationError('El número de contenedor no puede exceder 50 caracteres')
    
    @validates('numero_duca')
    def validate_numero_duca(self, value):
        if not value or len(value.strip()) == 0:
            raise ValidationError('El número de DUCA es requerido')
        if len(value) > 50:
            raise ValidationError('El número de DUCA no puede exceder 50 caracteres')
    
    @validates('numero_duca_rectificada')
    def validate_numero_duca_rectificada(self, value):
        if value and len(value) > 50:
            raise ValidationError('El número de DUCA rectificada no puede exceder 50 caracteres')

class DetalleIngresoMercanciaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DetalleIngresoMercancia
        load_instance = True
        fields = (
            "id",
            "ingreso_mercancia_id",
            "producto_id",
            "cantidad_fardos_paquetes",
            "unidades_por_fardo_paquete",
            "unidades_totales",
            "usuario_creacion",
            "producto"
        )
    
    @validates('ingreso_mercancia_id')
    def validate_ingreso_mercancia_id(self, value):
        if not value or value <= 0:
            raise ValidationError('El ID del ingreso de mercancía es requerido y debe ser mayor a 0')
    
    @validates('producto_id')
    def validate_producto_id(self, value):
        if not value or value <= 0:
            raise ValidationError('El ID del producto es requerido y debe ser mayor a 0')
    
    @validates('cantidad_fardos_paquetes')
    def validate_cantidad_fardos_paquetes(self, value):
        if not value or value <= 0:
            raise ValidationError('La cantidad de fardos/paquetes es requerida y debe ser mayor a 0')
    
    @validates('unidades_por_fardo_paquete')
    def validate_unidades_por_fardo_paquete(self, value):
        if not value or value <= 0:
            raise ValidationError('Las unidades por fardo/paquete son requeridas y deben ser mayor a 0')