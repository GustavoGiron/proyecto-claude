from app.models.departamentos_model import Departamento
from app.models.municipios_model import Municipio

class DepartamentoRepo:
    @staticmethod
    def all():
        return Departamento.query.all()

    @staticmethod
    def get(id):
        return Departamento.query.get(id)

    @staticmethod
    def get_municipios(dept_id):
        return Municipio.query.filter_by(departamento_id=dept_id).all()
