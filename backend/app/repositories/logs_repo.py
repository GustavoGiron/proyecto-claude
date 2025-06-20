from app import db
from app.models.logs_model import Log

class LogRepo:
    @staticmethod
    def add(funcion: str, cod_mensaje: int, servicio: str, descripcion: str):
        entry = Log(
            funcion=funcion,
            cod_mensaje=cod_mensaje,
            servicio=servicio,
            descripcion=descripcion
        )
        db.session.add(entry)
        db.session.commit()
        return entry
