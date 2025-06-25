from app.repositories.productos_repo import ProductoRepo
from datetime import datetime

class ProductoService:
    @staticmethod
    def get_all_productos():
        productos = ProductoRepo.get_all()
        return [producto.to_dict() for producto in productos]

    @staticmethod
    def get_all_productos_activos():
        productos = ProductoRepo.get_all_activos()
        return [producto.to_dict() for producto in productos]

    @staticmethod
    def get_producto_by_id(id):
        producto = ProductoRepo.get_by_id(id)
        return producto.to_dict() if producto else None

    @staticmethod
    def get_producto_by_codigo(codigo_producto):
        producto = ProductoRepo.get_by_codigo(codigo_producto)
        return producto.to_dict() if producto else None

    @staticmethod
    def create_producto(data, usuario_creacion=None):
        if usuario_creacion:
            data['usuario_creacion'] = usuario_creacion
        
        required_fields = ['codigo_producto', 'nombre_producto', 'unidad_medida']
        for field in required_fields:
            if not data.get(field):
                return None, f"Campo requerido: {field}"
        
        if data.get('unidad_medida') not in ['Unidad', 'Fardo', 'Paquete']:
            return None, "unidad_medida debe ser 'Unidad', 'Fardo' o 'Paquete'"
        
        producto, error = ProductoRepo.create(data)
        if error:
            return None, error
        
        return producto.to_dict(), None

    @staticmethod
    def update_producto(id, data, usuario_modificacion=None):
        if usuario_modificacion:
            data['usuario_modificacion'] = usuario_modificacion
        
        if data.get('unidad_medida') and data.get('unidad_medida') not in ['Unidad', 'Fardo', 'Paquete']:
            return None, "unidad_medida debe ser 'Unidad', 'Fardo' o 'Paquete'"
        
        producto, error = ProductoRepo.update(id, data)
        if error:
            return None, error
        
        return producto.to_dict(), None

    @staticmethod
    def delete_producto(id):
        success, error = ProductoRepo.delete(id)
        return success, error

    @staticmethod
    def search_productos(nombre=None, codigo=None):
        productos = ProductoRepo.search(nombre=nombre, codigo=codigo)
        return [producto.to_dict() for producto in productos]
