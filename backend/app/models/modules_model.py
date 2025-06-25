from datetime import datetime
from app.database import db


class Module(db.Model):
    __tablename__ = 'modules'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.String(200))
    ruta = db.Column(db.String(100))
    icono = db.Column(db.String(50))
    orden = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    role_modules = db.relationship('RoleModule', back_populates='module', cascade='all, delete-orphan')
    permissions = db.relationship('Permission', back_populates='module', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'ruta': self.ruta,
            'icono': self.icono,
            'orden': self.orden,
            'is_active': self.is_active,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }