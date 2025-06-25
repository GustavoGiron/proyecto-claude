from app.database import db


class RoleModule(db.Model):
    __tablename__ = 'role_modules'
    
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    
    role = db.relationship('Role', back_populates='role_modules')
    module = db.relationship('Module', back_populates='role_modules')
    
    __table_args__ = (db.UniqueConstraint('role_id', 'module_id', name='_role_module_uc'),)