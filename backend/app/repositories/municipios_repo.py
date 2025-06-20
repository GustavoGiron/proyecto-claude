from app.models.municipios_model import Municipio

class MunicipioRepo:
    @staticmethod
    def all():
        return Municipio.query.all()

    @staticmethod
    def get(id):
        return Municipio.query.get(id)
