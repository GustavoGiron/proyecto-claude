from app.repositories.departamentos_repo import DepartamentoRepo

class DepartamentoService:
    @staticmethod
    def list_all():
        return DepartamentoRepo.all()

    @staticmethod
    def get_by_id(id):
        return DepartamentoRepo.get(id)

    @staticmethod
    def get_municipios(id):
        return DepartamentoRepo.get_municipios(id)
