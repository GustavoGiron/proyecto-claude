from app import db
from datetime import datetime

class Vendedor(db.Model):
    __tablename__ = 'Vendedores'

    id = db.Column('Id', db.Integer, primary_key=True, autoincrement=True)
    codigo_vendedor = db.Column('CodigoVendedor', db.String(20), unique=True, nullable=False)
    nombres = db.Column('Nombres', db.String(100), nullable=False)
    apellidos = db.Column('Apellidos', db.String(100), nullable=False)
    telefono = db.Column('Telefono', db.String(20))
    direccion = db.Column('Direccion', db.Text)
    porcentaje_comision = db.Column('PorcentajeComision', db.Numeric(5,2), nullable=False)
    fecha_modificacion = db.Column('FechaModificacion', db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    usuario_creacion = db.Column('UsuarioCreacion', db.String(50))
    usuario_modificacion = db.Column('UsuarioModificacion', db.String(50))

    def to_dict(self):
        return {
            'id': self.id,
            'codigo_vendedor': self.codigo_vendedor,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'nombre_completo': f"{self.nombres} {self.apellidos}",
            'telefono': self.telefono,
            'direccion': self.direccion,
            'porcentaje_comision': float(self.porcentaje_comision) if self.porcentaje_comision else 0.0,
            'fecha_modificacion': self.fecha_modificacion.isoformat() if self.fecha_modificacion else None,
            'usuario_creacion': self.usuario_creacion,
            'usuario_modificacion': self.usuario_modificacion
        }