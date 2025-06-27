from app.database import db


class RolePermission(db.Model):
    __tablename__ = 'role_permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), nullable=False)
    
    role = db.relationship('Role', back_populates='role_permissions')
    permission = db.relationship('Permission', back_populates='role_permissions')
    
    __table_args__ = (db.UniqueConstraint('role_id', 'permission_id', name='_role_permission_uc'),)