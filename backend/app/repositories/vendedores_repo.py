from app import db
from app.models.vendedores_model import Vendedor
from sqlalchemy.exc import IntegrityError

class VendedorRepo:
    @staticmethod
    def get_all():
        return Vendedor.query.all()

    @staticmethod
    def get_by_id(id):
        return Vendedor.query.get(id)

    @staticmethod
    def get_by_codigo(codigo_vendedor):
        return Vendedor.query.filter_by(codigo_vendedor=codigo_vendedor).first()

    @staticmethod
    def create(vendedor_data):
        try:
            vendedor = Vendedor(**vendedor_data)
            db.session.add(vendedor)
            db.session.commit()
            return vendedor, None
        except IntegrityError as e:
            db.session.rollback()
            return None, str(e)
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def update(id, vendedor_data):
        try:
            vendedor = Vendedor.query.get(id)
            if not vendedor:
                return None, "Vendedor no encontrado"
            
            for key, value in vendedor_data.items():
                if hasattr(vendedor, key):
                    setattr(vendedor, key, value)
            
            db.session.commit()
            return vendedor, None
        except IntegrityError as e:
            db.session.rollback()
            return None, str(e)
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def update_by_codigo(codigo_vendedor, vendedor_data):
        try:
            vendedor = Vendedor.query.filter_by(codigo_vendedor=codigo_vendedor).first()
            if not vendedor:
                return None, "Vendedor no encontrado"
            
            for key, value in vendedor_data.items():
                if hasattr(vendedor, key):
                    setattr(vendedor, key, value)
            
            db.session.commit()
            return vendedor, None
        except IntegrityError as e:
            db.session.rollback()
            return None, str(e)
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def delete(id):
        try:
            vendedor = Vendedor.query.get(id)
            if not vendedor:
                return False, "Vendedor no encontrado"
            
            db.session.delete(vendedor)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def delete_by_codigo(codigo_vendedor):
        try:
            vendedor = Vendedor.query.filter_by(codigo_vendedor=codigo_vendedor).first()
            if not vendedor:
                return False, "Vendedor no encontrado"
            
            db.session.delete(vendedor)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def search(nombres=None, apellidos=None, codigo=None):
        query = Vendedor.query
        if nombres:
            query = query.filter(Vendedor.nombres.ilike(f'%{nombres}%'))
        if apellidos:
            query = query.filter(Vendedor.apellidos.ilike(f'%{apellidos}%'))
        if codigo:
            query = query.filter(Vendedor.codigo_vendedor.ilike(f'%{codigo}%'))
        return query.all()

    @staticmethod
    def get_max_codigo_numero():
        """Obtiene el número más alto en los códigos de vendedor para generar el siguiente"""
        vendedores = Vendedor.query.with_entities(Vendedor.codigo_vendedor).all()
        max_num = 0
        
        for (codigo,) in vendedores:
            # Extrae la parte numérica del código (ej: V001 -> 1, V010 -> 10)
            if codigo and codigo.startswith('V') and len(codigo) > 1:
                try:
                    num = int(codigo[1:])
                    max_num = max(max_num, num)
                except ValueError:
                    continue
        
        return max_num