from app.repositories.inventario_repo import (
    InventarioRepo, 
    MovimientoInventarioRepo, 
    IngresoMercanciaRepo, 
    DetalleIngresoMercanciaRepo
)
from app.repositories.productos_repo import ProductoRepo
from datetime import datetime

class InventarioService:
    @staticmethod
    def get_all_inventario():
        inventarios = InventarioRepo.get_all()
        return [inventario.to_dict() for inventario in inventarios]

    @staticmethod
    def get_inventario_by_id(id):
        inventario = InventarioRepo.get_by_id(id)
        return inventario.to_dict() if inventario else None

    @staticmethod
    def get_inventario_by_producto_id(producto_id):
        inventario = InventarioRepo.get_by_producto_id(producto_id)
        return inventario.to_dict() if inventario else None

    @staticmethod
    def create_inventario(data, usuario_creacion=None):
        required_fields = ['producto_id']
        for field in required_fields:
            if not data.get(field):
                return None, f"Campo requerido: {field}"
        
        producto = ProductoRepo.get_by_id(data['producto_id'])
        if not producto:
            return None, "Producto no encontrado"
        
        if usuario_creacion:
            data['usuario_ultima_actualizacion'] = usuario_creacion
        
        inventario, error = InventarioRepo.create(data)
        if error:
            return None, error
        
        return inventario.to_dict(), None

    @staticmethod
    def update_inventario(id, data, usuario_modificacion=None):
        if usuario_modificacion:
            data['usuario_ultima_actualizacion'] = usuario_modificacion
        
        inventario, error = InventarioRepo.update(id, data)
        if error:
            return None, error
        
        return inventario.to_dict(), None

    @staticmethod
    def delete_inventario(id):
        success, error = InventarioRepo.delete(id)
        return success, error

    @staticmethod
    def get_stock_bajo_minimo():
        inventarios = InventarioRepo.get_stock_bajo_minimo()
        return [inventario.to_dict() for inventario in inventarios]

    @staticmethod
    def registrar_movimiento_inventario(producto_id, tipo_movimiento, cantidad, referencia=None, motivo=None, usuario=None):
        tipos_validos = ['Ingreso', 'Salida', 'Ajuste', 'Apartado', 'Liberado']
        if tipo_movimiento not in tipos_validos:
            return None, f"Tipo de movimiento debe ser uno de: {', '.join(tipos_validos)}"
        
        inventario = InventarioRepo.get_by_producto_id(producto_id)
        if not inventario:
            return None, "No existe inventario para este producto"
        
        stock_anterior = inventario.stock_disponible
        
        if tipo_movimiento == 'Ingreso':
            nuevo_stock_disponible = stock_anterior + cantidad
        elif tipo_movimiento == 'Salida':
            if stock_anterior < cantidad:
                return None, "Stock insuficiente para la salida"
            nuevo_stock_disponible = stock_anterior - cantidad
        elif tipo_movimiento == 'Ajuste':
            nuevo_stock_disponible = cantidad
        elif tipo_movimiento == 'Apartado':
            if stock_anterior < cantidad:
                return None, "Stock insuficiente para apartar"
            nuevo_stock_disponible = stock_anterior - cantidad
            nuevo_stock_apartado = inventario.stock_apartado + cantidad
            InventarioRepo.actualizar_stock(producto_id, nuevo_stock_disponible, nuevo_stock_apartado, usuario)
        elif tipo_movimiento == 'Liberado':
            if inventario.stock_apartado < cantidad:
                return None, "Stock apartado insuficiente para liberar"
            nuevo_stock_disponible = stock_anterior + cantidad
            nuevo_stock_apartado = inventario.stock_apartado - cantidad
            InventarioRepo.actualizar_stock(producto_id, nuevo_stock_disponible, nuevo_stock_apartado, usuario)
        
        if tipo_movimiento not in ['Apartado', 'Liberado']:
            InventarioRepo.actualizar_stock(producto_id, nuevo_stock_disponible, None, usuario)
        
        movimiento_data = {
            'producto_id': producto_id,
            'tipo_movimiento': tipo_movimiento,
            'cantidad': cantidad,
            'stock_anterior': stock_anterior,
            'stock_nuevo': nuevo_stock_disponible if tipo_movimiento not in ['Apartado', 'Liberado'] else inventario.stock_disponible,
            'referencia': referencia,
            'motivo': motivo,
            'usuario_movimiento': usuario
        }
        
        movimiento, error = MovimientoInventarioRepo.create(movimiento_data)
        if error:
            return None, error
        
        return movimiento.to_dict(), None

    @staticmethod
    def get_movimientos_by_producto(producto_id):
        movimientos = MovimientoInventarioRepo.get_by_producto_id(producto_id)
        return [movimiento.to_dict() for movimiento in movimientos]

    @staticmethod
    def get_all_movimientos():
        movimientos = MovimientoInventarioRepo.get_all()
        return [movimiento.to_dict() for movimiento in movimientos]

    @staticmethod
    def get_movimientos_by_tipo(tipo_movimiento):
        movimientos = MovimientoInventarioRepo.get_by_tipo_movimiento(tipo_movimiento)
        return [movimiento.to_dict() for movimiento in movimientos]

    @staticmethod
    def get_movimientos_by_fecha_rango(fecha_inicio, fecha_fin):
        try:
            if isinstance(fecha_inicio, str):
                fecha_inicio = datetime.fromisoformat(fecha_inicio)
            if isinstance(fecha_fin, str):
                fecha_fin = datetime.fromisoformat(fecha_fin)
            
            movimientos = MovimientoInventarioRepo.get_by_fecha_rango(fecha_inicio, fecha_fin)
            return [movimiento.to_dict() for movimiento in movimientos]
        except ValueError as e:
            return None, f"Formato de fecha inválido: {str(e)}"

class IngresoMercanciaService:
    @staticmethod
    def get_all_ingresos():
        ingresos = IngresoMercanciaRepo.get_all()
        return [ingreso.to_dict() for ingreso in ingresos]

    @staticmethod
    def get_ingreso_by_id(id):
        ingreso = IngresoMercanciaRepo.get_by_id(id)
        if not ingreso:
            return None
        
        ingreso_dict = ingreso.to_dict()
        detalles = DetalleIngresoMercanciaRepo.get_by_ingreso_id(id)
        ingreso_dict['detalles'] = [detalle.to_dict() for detalle in detalles]
        
        return ingreso_dict

    @staticmethod
    def create_ingreso(data, usuario_creacion=None):
        required_fields = ['fecha_ingreso', 'numero_contenedor', 'numero_duca', 'fecha_duca']
        for field in required_fields:
            if not data.get(field):
                return None, f"Campo requerido: {field}"
        
        if usuario_creacion:
            data['usuario_creacion'] = usuario_creacion
        
        if isinstance(data.get('fecha_ingreso'), str):
            try:
                data['fecha_ingreso'] = datetime.fromisoformat(data['fecha_ingreso']).date()
            except ValueError:
                return None, "Formato de fecha_ingreso inválido"
        
        if isinstance(data.get('fecha_duca'), str):
            try:
                data['fecha_duca'] = datetime.fromisoformat(data['fecha_duca']).date()
            except ValueError:
                return None, "Formato de fecha_duca inválido"
        
        if data.get('fecha_duca_rectificada') and isinstance(data.get('fecha_duca_rectificada'), str):
            try:
                data['fecha_duca_rectificada'] = datetime.fromisoformat(data['fecha_duca_rectificada']).date()
            except ValueError:
                return None, "Formato de fecha_duca_rectificada inválido"
        
        ingreso, error = IngresoMercanciaRepo.create(data)
        if error:
            return None, error
        
        return ingreso.to_dict(), None

    @staticmethod
    def update_ingreso(id, data):
        if isinstance(data.get('fecha_ingreso'), str):
            try:
                data['fecha_ingreso'] = datetime.fromisoformat(data['fecha_ingreso']).date()
            except ValueError:
                return None, "Formato de fecha_ingreso inválido"
        
        if isinstance(data.get('fecha_duca'), str):
            try:
                data['fecha_duca'] = datetime.fromisoformat(data['fecha_duca']).date()
            except ValueError:
                return None, "Formato de fecha_duca inválido"
        
        if data.get('fecha_duca_rectificada') and isinstance(data.get('fecha_duca_rectificada'), str):
            try:
                data['fecha_duca_rectificada'] = datetime.fromisoformat(data['fecha_duca_rectificada']).date()
            except ValueError:
                return None, "Formato de fecha_duca_rectificada inválido"
        
        ingreso, error = IngresoMercanciaRepo.update(id, data)
        if error:
            return None, error
        
        return ingreso.to_dict(), None

    @staticmethod
    def delete_ingreso(id):
        success, error = IngresoMercanciaRepo.delete(id)
        return success, error

    @staticmethod
    def add_detalle_ingreso(ingreso_id, detalle_data, usuario_creacion=None):
        ingreso = IngresoMercanciaRepo.get_by_id(ingreso_id)
        if not ingreso:
            return None, "Ingreso de mercancía no encontrado"
        
        required_fields = ['producto_id', 'cantidad_fardos_paquetes', 'unidades_por_fardo_paquete']
        for field in required_fields:
            if not detalle_data.get(field):
                return None, f"Campo requerido: {field}"
        
        producto = ProductoRepo.get_by_id(detalle_data['producto_id'])
        if not producto:
            return None, "Producto no encontrado"
        
        detalle_data['ingreso_mercancia_id'] = ingreso_id
        if usuario_creacion:
            detalle_data['usuario_creacion'] = usuario_creacion
        
        detalle, error = DetalleIngresoMercanciaRepo.create(detalle_data)
        if error:
            return None, error
        
        unidades_totales = detalle_data['cantidad_fardos_paquetes'] * detalle_data['unidades_por_fardo_paquete']
        InventarioService.registrar_movimiento_inventario(
            detalle_data['producto_id'],
            'Ingreso',
            unidades_totales,
            referencia=f"Ingreso #{ingreso_id}",
            motivo=f"Ingreso de mercancía - Contenedor: {ingreso.numero_contenedor}",
            usuario=usuario_creacion
        )
        
        return detalle.to_dict(), None