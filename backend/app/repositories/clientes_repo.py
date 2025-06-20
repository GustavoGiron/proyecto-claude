from app import db
from app.models.clientes_model import Cliente

class ClienteRepo:
    @staticmethod
    def all():
        return Cliente.query.all()

    @staticmethod
    def get(id):
        return Cliente.query.get(id)

    @staticmethod
    def get_by_codigo(codigo):
        return Cliente.query.filter_by(codigo_cliente=codigo).first()

    @staticmethod
    def add(data: dict):
        cliente = Cliente(**data)
        db.session.add(cliente)
        db.session.commit()
        return cliente

    @staticmethod
    def update(id, data: dict):
        cliente = Cliente.query.get(id)
        if not cliente:
            return None
        for key, val in data.items():
            setattr(cliente, key, val)
        db.session.commit()
        return cliente

    @staticmethod
    def update_by_codigo(codigo, data: dict):
        cliente = Cliente.query.filter_by(codigo_cliente=codigo).first()
        if not cliente:
            return None
        for key, val in data.items():
            setattr(cliente, key, val)
        db.session.commit()
        return cliente

    @staticmethod
    def delete(id):
        cliente = Cliente.query.get(id)
        if not cliente:
            return False
        db.session.delete(cliente)
        db.session.commit()
        return True

    @staticmethod
    def delete_by_codigo(codigo):
        cliente = Cliente.query.filter_by(codigo_cliente=codigo).first()
        if not cliente:
            return False
        db.session.delete(cliente)
        db.session.commit()
        return True