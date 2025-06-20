from app import db

class Municipio(db.Model):
    __tablename__ = 'Municipios'

    id = db.Column('Id', db.Integer, primary_key=True)
    departamento_id = db.Column('DepartamentoId', db.Integer,
                                db.ForeignKey('Departamentos.Id'),
                                nullable=False)
    nombre = db.Column('Nombre', db.String(100), nullable=False)

    departamento = db.relationship(
        'Departamento',
        backref=db.backref('municipios', lazy=True)
    )
