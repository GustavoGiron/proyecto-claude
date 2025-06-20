from app import ma
from app.models.departamentos_model import Departamento

class DepartamentoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Departamento
        load_instance = True
        include_fk = True
