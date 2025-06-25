from app import db
from datetime import datetime
from sqlalchemy import CheckConstraint

class Producto(db.Model):
    __tablename__ = 'Productos'
    
    id = db.Column('Id', db.Integer, primary_key=True, autoincrement=True)
    codigo_producto = db.Column('CodigoProducto', db.String(50), nullable=False, unique=True)
    nombre_producto = db.Column('NombreProducto', db.String(200), nullable=False)
    unidad_medida = db.Column('UnidadMedida', db.String(10), nullable=False)
    unidades_por_fardo_paquete = db.Column('UnidadesPorFardoPaquete', db.Integer, nullable=False, default=1)
    stock_minimo = db.Column('StockMinimo', db.Integer, default=0)
    fecha_modificacion = db.Column('FechaModificacion', db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    usuario_creacion = db.Column('UsuarioCreacion', db.String(50))
    usuario_modificacion = db.Column('UsuarioModificacion', db.String(50))
    estado_producto = db.Column('estadoProducto', db.String(20), default='Activo')
    
    __table_args__ = (
        CheckConstraint(unidad_medida.in_(['Unidad', 'Fardo', 'Paquete']), name='check_unidad_medida'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'codigo_producto': self.codigo_producto,
            'nombre_producto': self.nombre_producto,
            'unidad_medida': self.unidad_medida,
            'unidades_por_fardo_paquete': self.unidades_por_fardo_paquete,
            'stock_minimo': self.stock_minimo,
            'fecha_modificacion': self.fecha_modificacion.isoformat() if self.fecha_modificacion else None,
            'usuario_creacion': self.usuario_creacion,
            'usuario_modificacion': self.usuario_modificacion,
            'estado_producto': self.estado_producto
        }
