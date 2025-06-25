from datetime import datetime
from app.database import db


class Permission(db.Model):
    __tablename__ = 'permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(200))
    accion = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    module = db.relationship('Module', back_populates='permissions')
    
    role_permissions = db.relationship('RolePermission', back_populates='permission', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'accion': self.accion,
            'is_active': self.is_active,
            'module': self.module.nombre if self.module else None,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }