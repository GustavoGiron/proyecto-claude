import threading
from app.repositories.inventario_repo import (
    InventarioRepo,
    MovimientoInventarioRepo,
    IngresoMercanciaRepo,
    DetalleIngresoMercanciaRepo
)
from app.repositories.productos_repo import ProductoRepo
from app.repositories.usuarios_repo import UsuariosRepository
from datetime import datetime
from app.utils.emailalert import enviar_alerta_stock_bajo
import os


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
        usuarios_repo = UsuariosRepository()
        tipos_validos = ['Ingreso', 'Salida', 'Ajuste', 'Apartado', 'Liberado']
        if tipo_movimiento not in tipos_validos:
            return None, f"Tipo de movimiento debe ser uno de: {', '.join(tipos_validos)}"

        inventario = InventarioRepo.get_by_producto_id(producto_id)
        if not inventario:
            inventario_data = {
                'producto_id': producto_id,
                'stock_disponible': 0,
                'stock_apartado': 0,
                'usuario_ultima_actualizacion': usuario
            }
            inventario, error = InventarioRepo.create(inventario_data)
            if error:
                return None, f"Error al crear inventario: {error}"

        stock_anterior = inventario.stock_disponible
        nuevo_stock_disponible = stock_anterior
        nuevo_stock_apartado = inventario.stock_apartado

        if tipo_movimiento == 'Ingreso':
            nuevo_stock_disponible += cantidad
        elif tipo_movimiento == 'Salida':
            if stock_anterior < cantidad:
                return None, "Stock insuficiente para la salida"
            nuevo_stock_disponible -= cantidad
        elif tipo_movimiento == 'Ajuste':
            nuevo_stock_disponible = cantidad
        elif tipo_movimiento == 'Apartado':
            if stock_anterior < cantidad:
                return None, "Stock insuficiente para apartar"
            nuevo_stock_disponible -= cantidad
            nuevo_stock_apartado += cantidad
        elif tipo_movimiento == 'Liberado':
            if inventario.stock_apartado < cantidad:
                return None, "Stock apartado insuficiente para liberar"
            nuevo_stock_disponible += cantidad
            nuevo_stock_apartado -= cantidad

        # Solo actualizar stock si no es Apartado o Liberado
        if tipo_movimiento not in ['Apartado', 'Liberado']:
            InventarioRepo.actualizar_stock(
                producto_id, nuevo_stock_disponible, None, usuario)
        else:
            InventarioRepo.actualizar_stock(
                producto_id, nuevo_stock_disponible, nuevo_stock_apartado, usuario)
        
        # Verificar si el stock disponible es menor que el mínimo
        STOCK_MINIMO = int(os.getenv('STOCK_MINIMO_ALERTA', '100'))
        if tipo_movimiento == 'Salida' and nuevo_stock_disponible < STOCK_MINIMO:
            # Obtener usuarios con rol 1 (Gerencia General)
            gerentes_rol1 = usuarios_repo.get_by_role_id(1)
            # Obtener usuarios con rol 3 (Gerencia Inventario)
            gerentes_rol3 = usuarios_repo.get_by_role_id(3)
            # Extraer solo los correos
            correos_rol1 = [u.email for u in gerentes_rol1 if u.email]
            correos_rol3 = [u.email for u in gerentes_rol3 if u.email]
            destinatarios = correos_rol1 + correos_rol3

            nombre_producto = inventario.producto.nombre_producto if inventario.producto else "Producto Desconocido"
            # Enviar alerta de stock bajo
            try:
                thread = threading.Thread(
                    target=enviar_alerta_stock_bajo,
                    args=(producto_id, nuevo_stock_disponible, nombre_producto, destinatarios)
                )
                thread.start()
            except Exception as e:
                print(f"Error al enviar alerta de stock bajo: {e}")

        # Crear registro del movimiento
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
        movimientos = MovimientoInventarioRepo.get_by_tipo_movimiento(
            tipo_movimiento)
        return [movimiento.to_dict() for movimiento in movimientos]

    @staticmethod
    def get_movimientos_by_fecha_rango(fecha_inicio, fecha_fin):
        try:
            if isinstance(fecha_inicio, str):
                fecha_inicio = datetime.fromisoformat(fecha_inicio)
            if isinstance(fecha_fin, str):
                fecha_fin = datetime.fromisoformat(fecha_fin)

            movimientos = MovimientoInventarioRepo.get_by_fecha_rango(
                fecha_inicio, fecha_fin)
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
        required_fields = ['fecha_ingreso',
                           'numero_contenedor', 'numero_duca', 'fecha_duca']
        for field in required_fields:
            if not data.get(field):
                return None, f"Campo requerido: {field}"

        if usuario_creacion:
            data['usuario_creacion'] = usuario_creacion

        if isinstance(data.get('fecha_ingreso'), str):
            try:
                data['fecha_ingreso'] = datetime.fromisoformat(
                    data['fecha_ingreso']).date()
            except ValueError:
                return None, "Formato de fecha_ingreso inválido"

        if isinstance(data.get('fecha_duca'), str):
            try:
                data['fecha_duca'] = datetime.fromisoformat(
                    data['fecha_duca']).date()
            except ValueError:
                return None, "Formato de fecha_duca inválido"

        if data.get('fecha_duca_rectificada') and isinstance(data.get('fecha_duca_rectificada'), str):
            try:
                data['fecha_duca_rectificada'] = datetime.fromisoformat(
                    data['fecha_duca_rectificada']).date()
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
                data['fecha_ingreso'] = datetime.fromisoformat(
                    data['fecha_ingreso']).date()
            except ValueError:
                return None, "Formato de fecha_ingreso inválido"

        if isinstance(data.get('fecha_duca'), str):
            try:
                data['fecha_duca'] = datetime.fromisoformat(
                    data['fecha_duca']).date()
            except ValueError:
                return None, "Formato de fecha_duca inválido"

        if data.get('fecha_duca_rectificada') and isinstance(data.get('fecha_duca_rectificada'), str):
            try:
                data['fecha_duca_rectificada'] = datetime.fromisoformat(
                    data['fecha_duca_rectificada']).date()
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

        required_fields = [
            'producto_id', 'cantidad_fardos_paquetes', 'unidades_por_fardo_paquete']
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

        unidades_totales = detalle_data['cantidad_fardos_paquetes'] * \
            detalle_data['unidades_por_fardo_paquete']
        InventarioService.registrar_movimiento_inventario(
            detalle_data['producto_id'],
            'Ingreso',
            unidades_totales,
            referencia=f"Ingreso #{ingreso_id}",
            motivo=f"Ingreso de mercancía - Contenedor: {ingreso.numero_contenedor}",
            usuario=usuario_creacion
        )

        return detalle.to_dict(), None
