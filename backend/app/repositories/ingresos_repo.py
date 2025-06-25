from app import db
from app.models.inventario_model import IngresoMercancia, DetalleIngresoMercancia, Inventario, MovimientoInventario
from app.models.productos_model import Producto
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from typing import List, Optional, Tuple

class IngresoMercanciaRepo:
    
    @staticmethod
    def get_all() -> List[IngresoMercancia]:
        """Obtener todos los ingresos de mercancía"""
        return IngresoMercancia.query.options(joinedload(IngresoMercancia.detalles)).all()
    
    @staticmethod
    def get_by_id(ingreso_id: int) -> Optional[IngresoMercancia]:
        """Obtener ingreso por ID con sus detalles"""
        return IngresoMercancia.query.options(
            joinedload(IngresoMercancia.detalles).joinedload(DetalleIngresoMercancia.producto)
        ).filter_by(id=ingreso_id).first()
    
    @staticmethod
    def get_by_numero_contenedor(numero_contenedor: str) -> Optional[IngresoMercancia]:
        """Obtener ingreso por número de contenedor"""
        return IngresoMercancia.query.filter_by(numero_contenedor=numero_contenedor).first()
    
    @staticmethod
    def get_by_numero_duca(numero_duca: str) -> Optional[IngresoMercancia]:
        """Obtener ingreso por número DUCA"""
        return IngresoMercancia.query.filter_by(numero_duca=numero_duca).first()
    
    @staticmethod
    def create_ingreso_completo(ingreso_data: dict, detalles_data: List[dict]) -> Tuple[Optional[IngresoMercancia], Optional[str]]:
        """
        Crear un ingreso de mercancía con sus detalles
        Retorna (IngresoMercancia, error_message)
        """
        try:
            # Verificar duplicados
            if IngresoMercanciaRepo.get_by_numero_contenedor(ingreso_data.get('numero_contenedor')):
                return None, f"Ya existe un ingreso con el número de contenedor {ingreso_data.get('numero_contenedor')}"
            
            if IngresoMercanciaRepo.get_by_numero_duca(ingreso_data.get('numero_duca')):
                return None, f"Ya existe un ingreso con el número DUCA {ingreso_data.get('numero_duca')}"
            
            # Crear ingreso principal
            ingreso = IngresoMercancia(**ingreso_data)
            db.session.add(ingreso)
            db.session.flush()  # Para obtener el ID
            
            # Crear detalles
            for detalle_data in detalles_data:
                # Verificar que el producto existe
                producto = Producto.query.get(detalle_data.get('producto_id'))
                if not producto:
                    return None, f"El producto con ID {detalle_data.get('producto_id')} no existe"
                
                # Usar las unidades por fardo/paquete del producto si no se especifica
                if not detalle_data.get('unidades_por_fardo_paquete'):
                    detalle_data['unidades_por_fardo_paquete'] = producto.unidades_por_fardo_paquete
                
                detalle_data['ingreso_mercancia_id'] = ingreso.id
                # Remover campos calculados que no deben insertarse
                detalle_data.pop('unidades_totales', None)
                detalle = DetalleIngresoMercancia(**detalle_data)
                db.session.add(detalle)
            
            db.session.commit()
            
            # Actualizar inventario y registrar movimientos
            usuario_creacion = ingreso_data.get('usuario_creacion', 'sistema')
            for detalle in ingreso.detalles:
                unidades_totales = detalle.cantidad_fardos_paquetes * detalle.unidades_por_fardo_paquete
                
                # Buscar o crear registro de inventario
                inventario = Inventario.query.filter_by(producto_id=detalle.producto_id).first()
                
                if inventario:
                    # Actualizar inventario existente
                    stock_anterior = inventario.stock_disponible
                    inventario.stock_disponible += unidades_totales
                    inventario.usuario_ultima_actualizacion = usuario_creacion
                else:
                    # Crear nuevo registro de inventario
                    stock_anterior = 0
                    inventario = Inventario(
                        producto_id=detalle.producto_id,
                        stock_disponible=unidades_totales,
                        stock_apartado=0,
                        usuario_ultima_actualizacion=usuario_creacion
                    )
                    db.session.add(inventario)
                
                # Registrar movimiento de inventario
                movimiento = MovimientoInventario(
                    producto_id=detalle.producto_id,
                    tipo_movimiento='Ingreso',
                    cantidad=unidades_totales,
                    stock_anterior=stock_anterior,
                    stock_nuevo=stock_anterior + unidades_totales,
                    referencia=f"Contenedor: {ingreso.numero_contenedor}",
                    motivo=f"Ingreso de mercancía - DUCA: {ingreso.numero_duca}",
                    usuario_movimiento=usuario_creacion
                )
                db.session.add(movimiento)
            
            db.session.commit()
            
            # Recargar con relaciones
            return IngresoMercanciaRepo.get_by_id(ingreso.id), None
            
        except IntegrityError as e:
            db.session.rollback()
            return None, f"Error de integridad: {str(e.orig)}"
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def update_ingreso(ingreso_id: int, ingreso_data: dict) -> Tuple[Optional[IngresoMercancia], Optional[str]]:
        """Actualizar datos del ingreso (sin detalles)"""
        try:
            ingreso = IngresoMercancia.query.get(ingreso_id)
            if not ingreso:
                return None, "Ingreso no encontrado"
            
            # Verificar duplicados (excluyendo el actual)
            if 'numero_contenedor' in ingreso_data:
                existing = IngresoMercancia.query.filter(
                    IngresoMercancia.numero_contenedor == ingreso_data['numero_contenedor'],
                    IngresoMercancia.id != ingreso_id
                ).first()
                if existing:
                    return None, f"Ya existe otro ingreso con el número de contenedor {ingreso_data['numero_contenedor']}"
            
            if 'numero_duca' in ingreso_data:
                existing = IngresoMercancia.query.filter(
                    IngresoMercancia.numero_duca == ingreso_data['numero_duca'],
                    IngresoMercancia.id != ingreso_id
                ).first()
                if existing:
                    return None, f"Ya existe otro ingreso con el número DUCA {ingreso_data['numero_duca']}"
            
            # Actualizar campos
            for key, value in ingreso_data.items():
                if hasattr(ingreso, key):
                    setattr(ingreso, key, value)
            
            db.session.commit()
            return IngresoMercanciaRepo.get_by_id(ingreso.id), None
            
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def delete_ingreso(ingreso_id: int) -> Tuple[bool, Optional[str]]:
        """Eliminar ingreso y sus detalles"""
        try:
            ingreso = IngresoMercancia.query.get(ingreso_id)
            if not ingreso:
                return False, "Ingreso no encontrado"
            
            # Eliminar detalles primero
            DetalleIngresoMercancia.query.filter_by(ingreso_mercancia_id=ingreso_id).delete()
            
            # Eliminar ingreso
            db.session.delete(ingreso)
            db.session.commit()
            
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def confirmar_ingreso_a_inventario(ingreso_id: int, usuario_confirmacion: str) -> Tuple[bool, Optional[str]]:
        """
        Confirmar ingreso y aplicar cantidades al inventario
        """
        try:
            ingreso = IngresoMercanciaRepo.get_by_id(ingreso_id)
            if not ingreso:
                return False, "Ingreso no encontrado"
            
            if not ingreso.detalles:
                return False, "El ingreso no tiene detalles"
            
            # Procesar cada detalle
            for detalle in ingreso.detalles:
                unidades_totales = detalle.cantidad_fardos_paquetes * detalle.unidades_por_fardo_paquete
                
                # Buscar o crear registro de inventario
                inventario = Inventario.query.filter_by(producto_id=detalle.producto_id).first()
                
                if inventario:
                    # Actualizar inventario existente
                    stock_anterior = inventario.stock_disponible
                    inventario.stock_disponible += unidades_totales
                    inventario.usuario_ultima_actualizacion = usuario_confirmacion
                else:
                    # Crear nuevo registro de inventario
                    stock_anterior = 0
                    inventario = Inventario(
                        producto_id=detalle.producto_id,
                        stock_disponible=unidades_totales,
                        stock_apartado=0,
                        usuario_ultima_actualizacion=usuario_confirmacion
                    )
                    db.session.add(inventario)
                
                # Registrar movimiento de inventario
                movimiento = MovimientoInventario(
                    producto_id=detalle.producto_id,
                    tipo_movimiento='Ingreso',
                    cantidad=unidades_totales,
                    stock_anterior=stock_anterior,
                    stock_nuevo=stock_anterior + unidades_totales,
                    referencia=f"Contenedor: {ingreso.numero_contenedor}",
                    motivo=f"Ingreso de mercancía - DUCA: {ingreso.numero_duca}",
                    usuario_movimiento=usuario_confirmacion
                )
                db.session.add(movimiento)
            
            db.session.commit()
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, str(e)

class DetalleIngresoRepo:
    
    @staticmethod
    def get_by_ingreso(ingreso_id: int) -> List[DetalleIngresoMercancia]:
        """Obtener detalles de un ingreso específico"""
        return DetalleIngresoMercancia.query.options(
            joinedload(DetalleIngresoMercancia.producto)
        ).filter_by(ingreso_mercancia_id=ingreso_id).all()
    
    @staticmethod
    def add_detalle(ingreso_id: int, detalle_data: dict) -> Tuple[Optional[DetalleIngresoMercancia], Optional[str]]:
        """Agregar detalle a un ingreso existente"""
        try:
            # Verificar que el ingreso existe
            ingreso = IngresoMercancia.query.get(ingreso_id)
            if not ingreso:
                return None, "Ingreso no encontrado"
            
            # Verificar que el producto existe
            producto = Producto.query.get(detalle_data.get('producto_id'))
            if not producto:
                return None, f"El producto con ID {detalle_data.get('producto_id')} no existe"
            
            # Verificar que no existe ya ese producto en el ingreso
            existing = DetalleIngresoMercancia.query.filter_by(
                ingreso_mercancia_id=ingreso_id,
                producto_id=detalle_data.get('producto_id')
            ).first()
            if existing:
                return None, f"El producto {producto.codigo_producto} ya está incluido en este ingreso"
            
            detalle_data['ingreso_mercancia_id'] = ingreso_id
            if not detalle_data.get('unidades_por_fardo_paquete'):
                detalle_data['unidades_por_fardo_paquete'] = producto.unidades_por_fardo_paquete
            
            # Remover campos calculados que no deben insertarse
            detalle_data.pop('unidades_totales', None)
            detalle = DetalleIngresoMercancia(**detalle_data)
            db.session.add(detalle)
            db.session.commit()
            
            # Actualizar inventario y registrar movimiento
            usuario_creacion = detalle_data.get('usuario_creacion', 'sistema')
            unidades_totales = detalle.cantidad_fardos_paquetes * detalle.unidades_por_fardo_paquete
            
            # Buscar o crear registro de inventario
            inventario = Inventario.query.filter_by(producto_id=detalle.producto_id).first()
            
            if inventario:
                # Actualizar inventario existente
                stock_anterior = inventario.stock_disponible
                inventario.stock_disponible += unidades_totales
                inventario.usuario_ultima_actualizacion = usuario_creacion
            else:
                # Crear nuevo registro de inventario
                stock_anterior = 0
                inventario = Inventario(
                    producto_id=detalle.producto_id,
                    stock_disponible=unidades_totales,
                    stock_apartado=0,
                    usuario_ultima_actualizacion=usuario_creacion
                )
                db.session.add(inventario)
            
            # Registrar movimiento de inventario
            movimiento = MovimientoInventario(
                producto_id=detalle.producto_id,
                tipo_movimiento='Ingreso',
                cantidad=unidades_totales,
                stock_anterior=stock_anterior,
                stock_nuevo=stock_anterior + unidades_totales,
                referencia=f"Contenedor: {ingreso.numero_contenedor}",
                motivo=f"Ingreso de mercancía - DUCA: {ingreso.numero_duca}",
                usuario_movimiento=usuario_creacion
            )
            db.session.add(movimiento)
            db.session.commit()
            
            return detalle, None
            
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def update_detalle(detalle_id: int, detalle_data: dict) -> Tuple[Optional[DetalleIngresoMercancia], Optional[str]]:
        """Actualizar un detalle específico"""
        try:
            detalle = DetalleIngresoMercancia.query.get(detalle_id)
            if not detalle:
                return None, "Detalle no encontrado"
            
            for key, value in detalle_data.items():
                if hasattr(detalle, key) and key != 'id':
                    setattr(detalle, key, value)
            
            db.session.commit()
            return detalle, None
            
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def delete_detalle(detalle_id: int) -> Tuple[bool, Optional[str]]:
        """Eliminar un detalle específico"""
        try:
            detalle = DetalleIngresoMercancia.query.get(detalle_id)
            if not detalle:
                return False, "Detalle no encontrado"
            
            db.session.delete(detalle)
            db.session.commit()
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, str(e)