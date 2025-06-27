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
    def get_by_nombre_contacto(nombre_contacto):
        return Cliente.query.filter(
            Cliente.nombre_contacto.ilike(f'%{nombre_contacto}%')
        ).all()
    
    @staticmethod
    def search(nombre_contacto=None, nombre_negocio=None, codigo_cliente=None, nit=None):
        query = Cliente.query
        
        if nombre_contacto:
            query = query.filter(Cliente.nombre_contacto.ilike(f'%{nombre_contacto}%'))
        
        if nombre_negocio:
            query = query.filter(Cliente.nombre_negocio.ilike(f'%{nombre_negocio}%'))
            
        if codigo_cliente:
            query = query.filter(Cliente.codigo_cliente.ilike(f'%{codigo_cliente}%'))
            
        if nit:
            query = query.filter(Cliente.nit.ilike(f'%{nit}%'))
        
        return query.all()

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