from app.repositories.municipios_repo import MunicipioRepo

class MunicipioService:
    @staticmethod
    def list_all():
        return MunicipioRepo.all()

    @staticmethod
    def get_by_id(id):
        return MunicipioRepo.get(id)
