from datetime import datetime
from app.database import db


class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    usuarios = db.relationship('Usuario', back_populates='role')
    role_modules = db.relationship('RoleModule', back_populates='role', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'is_active': self.is_active,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'modules': [rm.module.nombre for rm in self.role_modules if rm.module]
        }