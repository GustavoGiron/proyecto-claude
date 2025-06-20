from app import db

class Departamento(db.Model):
    __tablename__ = 'Departamentos'

    id = db.Column('Id', db.Integer, primary_key=True)
    codigo = db.Column('Codigo', db.String(2), unique=True, nullable=False)
    nombre = db.Column('Nombre', db.String(50), nullable=False)
