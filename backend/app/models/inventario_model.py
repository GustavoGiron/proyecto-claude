from app import db
from datetime import datetime
from sqlalchemy import CheckConstraint

class Inventario(db.Model):
    __tablename__ = 'Inventario'
    
    id = db.Column('Id', db.Integer, primary_key=True, autoincrement=True)
    producto_id = db.Column('ProductoId', db.Integer, db.ForeignKey('Productos.Id'), nullable=False, unique=True)
    stock_disponible = db.Column('StockDisponible', db.Integer, nullable=False, default=0)
    stock_apartado = db.Column('StockApartado', db.Integer, nullable=False, default=0)
    stock_total = db.Column('StockTotal', db.Integer, server_default=db.text('(StockDisponible + StockApartado)'))
    fecha_ultima_actualizacion = db.Column('FechaUltimaActualizacion', db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    usuario_ultima_actualizacion = db.Column('UsuarioUltimaActualizacion', db.String(50))
    
    producto = db.relationship('Producto', backref='inventario')
    
    def to_dict(self):
        return {
            'id': self.id,
            'producto_id': self.producto_id,
            'stock_disponible': self.stock_disponible,
            'stock_apartado': self.stock_apartado,
            'stock_total': self.stock_disponible + self.stock_apartado,
            'fecha_ultima_actualizacion': self.fecha_ultima_actualizacion.isoformat() if self.fecha_ultima_actualizacion else None,
            'usuario_ultima_actualizacion': self.usuario_ultima_actualizacion,
            'producto': {
                'id': self.producto.id,
                'codigo_producto': self.producto.codigo_producto,
                'nombre_producto': self.producto.nombre_producto
            } if self.producto else None
        }

class MovimientoInventario(db.Model):
    __tablename__ = 'MovimientosInventario'
    
    id = db.Column('Id', db.Integer, primary_key=True, autoincrement=True)
    producto_id = db.Column('ProductoId', db.Integer, db.ForeignKey('Productos.Id'), nullable=False)
    tipo_movimiento = db.Column('TipoMovimiento', db.String(20), nullable=False)
    cantidad = db.Column('Cantidad', db.Integer, nullable=False)
    stock_anterior = db.Column('StockAnterior', db.Integer, nullable=False)
    stock_nuevo = db.Column('StockNuevo', db.Integer, nullable=False)
    referencia = db.Column('Referencia', db.String(100))
    motivo = db.Column('Motivo', db.String(200))
    fecha_movimiento = db.Column('FechaMovimiento', db.DateTime, default=datetime.utcnow)
    usuario_movimiento = db.Column('UsuarioMovimiento', db.String(50))
    
    __table_args__ = (
        CheckConstraint(tipo_movimiento.in_(['Ingreso', 'Salida', 'Ajuste', 'Apartado', 'Liberado']), name='check_tipo_movimiento'),
    )
    
    producto = db.relationship('Producto', backref='movimientos_inventario')
    
    def to_dict(self):
        return {
            'id': self.id,
            'producto_id': self.producto_id,
            'tipo_movimiento': self.tipo_movimiento,
            'cantidad': self.cantidad,
            'stock_anterior': self.stock_anterior,
            'stock_nuevo': self.stock_nuevo,
            'referencia': self.referencia,
            'motivo': self.motivo,
            'fecha_movimiento': self.fecha_movimiento.isoformat() if self.fecha_movimiento else None,
            'usuario_movimiento': self.usuario_movimiento,
            'producto': {
                'id': self.producto.id,
                'codigo_producto': self.producto.codigo_producto,
                'nombre_producto': self.producto.nombre_producto
            } if self.producto else None
        }

class IngresoMercancia(db.Model):
    __tablename__ = 'IngresosMercancia'
    
    id = db.Column('Id', db.Integer, primary_key=True, autoincrement=True)
    fecha_ingreso = db.Column('FechaIngreso', db.Date, nullable=False)
    numero_contenedor = db.Column('NumeroContenedor', db.String(50), nullable=False)
    numero_duca = db.Column('NumeroDuca', db.String(50), nullable=False)
    fecha_duca = db.Column('FechaDuca', db.Date, nullable=False)
    numero_duca_rectificada = db.Column('NumeroDucaRectificada', db.String(50))
    fecha_duca_rectificada = db.Column('FechaDucaRectificada', db.Date)
    observaciones = db.Column('Observaciones', db.Text)
    usuario_creacion = db.Column('UsuarioCreacion', db.String(50))
    
    def to_dict(self):
        return {
            'id': self.id,
            'fecha_ingreso': self.fecha_ingreso.isoformat() if self.fecha_ingreso else None,
            'numero_contenedor': self.numero_contenedor,
            'numero_duca': self.numero_duca,
            'fecha_duca': self.fecha_duca.isoformat() if self.fecha_duca else None,
            'numero_duca_rectificada': self.numero_duca_rectificada,
            'fecha_duca_rectificada': self.fecha_duca_rectificada.isoformat() if self.fecha_duca_rectificada else None,
            'observaciones': self.observaciones,
            'usuario_creacion': self.usuario_creacion
        }

class DetalleIngresoMercancia(db.Model):
    __tablename__ = 'DetalleIngresosMercancia'
    
    id = db.Column('Id', db.Integer, primary_key=True, autoincrement=True)
    ingreso_mercancia_id = db.Column('IngresoMercanciaId', db.Integer, db.ForeignKey('IngresosMercancia.Id'), nullable=False)
    producto_id = db.Column('ProductoId', db.Integer, db.ForeignKey('Productos.Id'), nullable=False)
    cantidad_fardos_paquetes = db.Column('CantidadFardosPaquetes', db.Integer, nullable=False)
    unidades_por_fardo_paquete = db.Column('UnidadesPorFardoPaquete', db.Integer, nullable=False)
    unidades_totales = db.Column('UnidadesTotales', db.Integer, server_default=db.text('(CantidadFardosPaquetes * UnidadesPorFardoPaquete)'))
    usuario_creacion = db.Column('UsuarioCreacion', db.String(50))
    
    ingreso_mercancia = db.relationship('IngresoMercancia', backref='detalles')
    producto = db.relationship('Producto', backref='detalles_ingreso')
    
    def to_dict(self):
        return {
            'id': self.id,
            'ingreso_mercancia_id': self.ingreso_mercancia_id,
            'producto_id': self.producto_id,
            'cantidad_fardos_paquetes': self.cantidad_fardos_paquetes,
            'unidades_por_fardo_paquete': self.unidades_por_fardo_paquete,
            'unidades_totales': self.cantidad_fardos_paquetes * self.unidades_por_fardo_paquete,
            'usuario_creacion': self.usuario_creacion,
            'producto': {
                'id': self.producto.id,
                'codigo_producto': self.producto.codigo_producto,
                'nombre_producto': self.producto.nombre_producto
            } if self.producto else None
        }