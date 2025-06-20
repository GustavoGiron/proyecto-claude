from app.repositories.vendedores_repo import VendedorRepo
from datetime import datetime

class VendedorService:
    @staticmethod
    def get_all_vendedores():
        vendedores = VendedorRepo.get_all()
        return [vendedor.to_dict() for vendedor in vendedores]

    @staticmethod
    def get_vendedor_by_id(id):
        vendedor = VendedorRepo.get_by_id(id)
        return vendedor.to_dict() if vendedor else None

    @staticmethod
    def get_vendedor_by_codigo(codigo_vendedor):
        vendedor = VendedorRepo.get_by_codigo(codigo_vendedor)
        return vendedor.to_dict() if vendedor else None

    @staticmethod
    def create_vendedor(data, usuario_creacion=None):
        # Remover codigo_vendedor si viene en los datos (se genera automáticamente)
        data.pop('codigo_vendedor', None)
        
        if usuario_creacion:
            data['usuario_creacion'] = usuario_creacion
        
        required_fields = ['nombres', 'apellidos', 'porcentaje_comision']
        for field in required_fields:
            if not data.get(field):
                return None, f"Campo requerido: {field}"
        
        # Validar porcentaje de comisión
        try:
            porcentaje = float(data['porcentaje_comision'])
            if porcentaje < 0 or porcentaje > 100:
                return None, "El porcentaje de comisión debe estar entre 0 y 100"
            data['porcentaje_comision'] = porcentaje
        except (ValueError, TypeError):
            return None, "El porcentaje de comisión debe ser un número válido"
        
        # Generar código de vendedor automático
        max_codigo = VendedorRepo.get_max_codigo_numero()
        next_codigo = max_codigo + 1
        data['codigo_vendedor'] = f"V{next_codigo:03d}"  # Formato: V001, V002, V003, etc.
        
        vendedor, error = VendedorRepo.create(data)
        if error:
            return None, error
        
        return vendedor.to_dict(), None

    @staticmethod
    def update_vendedor(id, data, usuario_modificacion=None):
        if usuario_modificacion:
            data['usuario_modificacion'] = usuario_modificacion
        
        # No permitir modificar el código de vendedor
        data.pop('codigo_vendedor', None)
        
        # Validar porcentaje de comisión si se proporciona
        if 'porcentaje_comision' in data:
            try:
                porcentaje = float(data['porcentaje_comision'])
                if porcentaje < 0 or porcentaje > 100:
                    return None, "El porcentaje de comisión debe estar entre 0 y 100"
                data['porcentaje_comision'] = porcentaje
            except (ValueError, TypeError):
                return None, "El porcentaje de comisión debe ser un número válido"
        
        vendedor, error = VendedorRepo.update(id, data)
        if error:
            return None, error
        
        return vendedor.to_dict(), None

    @staticmethod
    def update_vendedor_by_codigo(codigo_vendedor, data, usuario_modificacion=None):
        if usuario_modificacion:
            data['usuario_modificacion'] = usuario_modificacion
        
        # No permitir modificar el código de vendedor
        data.pop('codigo_vendedor', None)
        
        # Validar porcentaje de comisión si se proporciona
        if 'porcentaje_comision' in data:
            try:
                porcentaje = float(data['porcentaje_comision'])
                if porcentaje < 0 or porcentaje > 100:
                    return None, "El porcentaje de comisión debe estar entre 0 y 100"
                data['porcentaje_comision'] = porcentaje
            except (ValueError, TypeError):
                return None, "El porcentaje de comisión debe ser un número válido"
        
        vendedor, error = VendedorRepo.update_by_codigo(codigo_vendedor, data)
        if error:
            return None, error
        
        return vendedor.to_dict(), None

    @staticmethod
    def delete_vendedor(id):
        success, error = VendedorRepo.delete(id)
        return success, error

    @staticmethod
    def delete_vendedor_by_codigo(codigo_vendedor):
        success, error = VendedorRepo.delete_by_codigo(codigo_vendedor)
        return success, error

    @staticmethod
    def search_vendedores(nombres=None, apellidos=None, codigo=None):
        vendedores = VendedorRepo.search(nombres=nombres, apellidos=apellidos, codigo=codigo)
        return [vendedor.to_dict() for vendedor in vendedores]