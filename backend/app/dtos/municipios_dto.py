from app import ma
from app.models.municipios_model import Municipio

class MunicipioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Municipio
        load_instance = True
        include_fk = True
