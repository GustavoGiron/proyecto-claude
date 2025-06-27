from app import db

class Log(db.Model):
    __tablename__ = 'Logs'
    id = db.Column('Id', db.Integer, primary_key=True)
    fecha = db.Column('Fecha', db.DateTime, server_default=db.func.now())
    funcion = db.Column('Funcion', db.String(100), nullable=False)
    cod_mensaje = db.Column('codMensaje', db.Integer, nullable=False)
    servicio = db.Column('Servicio', db.String(100), nullable=False)
    descripcion = db.Column('Descripcion', db.Text)
