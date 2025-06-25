from app import db
from app.models.productos_model import Producto
from sqlalchemy.exc import IntegrityError

class ProductoRepo:
    @staticmethod
    def get_all():
        return Producto.query.all()
    
    @staticmethod
    def get_all_activos():
        return Producto.query.filter_by(estado_producto='Activo').all()

    @staticmethod
    def get_by_id(id):
        return Producto.query.get(id)

    @staticmethod
    def get_by_codigo(codigo_producto):
        return Producto.query.filter_by(codigo_producto=codigo_producto).first()

    @staticmethod
    def create(producto_data):
        try:
            producto = Producto(**producto_data)
            db.session.add(producto)
            db.session.commit()
            return producto, None
        except IntegrityError as e:
            db.session.rollback()
            return None, str(e)
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def update(id, producto_data):
        try:
            producto = Producto.query.get(id)
            if not producto:
                return None, "Producto no encontrado"
            
            for key, value in producto_data.items():
                if hasattr(producto, key):
                    setattr(producto, key, value)
            producto.estado_producto = "Activo"
            db.session.commit()
            return producto, None
        except IntegrityError as e:
            db.session.rollback()
            return None, str(e)
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def delete(id):
        try:
            producto = Producto.query.get(id)
            if not producto:
                return False, "Producto no encontrado"
            producto.unidades_por_fardo_paquete = 0 
            producto.estado_producto = "Inactivo"
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def search(nombre=None, codigo=None):
        query = Producto.query
        if nombre:
            query = query.filter(Producto.nombre_producto.ilike(f'%{nombre}%'))
        if codigo:
            query = query.filter(Producto.codigo_producto.ilike(f'%{codigo}%'))
        return query.all()