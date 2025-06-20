from app import db
from app.models.inventario_model import Inventario, MovimientoInventario, IngresoMercancia, DetalleIngresoMercancia
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, desc

class InventarioRepo:
    @staticmethod
    def get_all():
        return Inventario.query.all()

    @staticmethod
    def get_by_id(id):
        return Inventario.query.get(id)

    @staticmethod
    def get_by_producto_id(producto_id):
        return Inventario.query.filter_by(producto_id=producto_id).first()

    @staticmethod
    def create(inventario_data):
        try:
            inventario = Inventario(**inventario_data)
            db.session.add(inventario)
            db.session.commit()
            return inventario, None
        except IntegrityError as e:
            db.session.rollback()
            return None, str(e)
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def update(id, inventario_data):
        try:
            inventario = Inventario.query.get(id)
            if not inventario:
                return None, "Inventario no encontrado"
            
            for key, value in inventario_data.items():
                if hasattr(inventario, key):
                    setattr(inventario, key, value)
            
            db.session.commit()
            return inventario, None
        except IntegrityError as e:
            db.session.rollback()
            return None, str(e)
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def delete(id):
        try:
            inventario = Inventario.query.get(id)
            if not inventario:
                return False, "Inventario no encontrado"
            
            db.session.delete(inventario)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def get_stock_bajo_minimo():
        return db.session.query(Inventario).join(Inventario.producto).filter(
            Inventario.stock_disponible < db.text('Productos.StockMinimo')
        ).all()

    @staticmethod
    def actualizar_stock(producto_id, stock_disponible=None, stock_apartado=None, usuario=None):
        try:
            inventario = Inventario.query.filter_by(producto_id=producto_id).first()
            if not inventario:
                return None, "Inventario no encontrado para el producto"
            
            if stock_disponible is not None:
                inventario.stock_disponible = stock_disponible
            if stock_apartado is not None:
                inventario.stock_apartado = stock_apartado
            if usuario:
                inventario.usuario_ultima_actualizacion = usuario
            
            db.session.commit()
            return inventario, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

class MovimientoInventarioRepo:
    @staticmethod
    def get_all():
        return MovimientoInventario.query.order_by(desc(MovimientoInventario.fecha_movimiento)).all()

    @staticmethod
    def get_by_id(id):
        return MovimientoInventario.query.get(id)

    @staticmethod
    def get_by_producto_id(producto_id):
        return MovimientoInventario.query.filter_by(producto_id=producto_id).order_by(desc(MovimientoInventario.fecha_movimiento)).all()

    @staticmethod
    def create(movimiento_data):
        try:
            movimiento = MovimientoInventario(**movimiento_data)
            db.session.add(movimiento)
            db.session.commit()
            return movimiento, None
        except IntegrityError as e:
            db.session.rollback()
            return None, str(e)
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def get_by_tipo_movimiento(tipo_movimiento):
        return MovimientoInventario.query.filter_by(tipo_movimiento=tipo_movimiento).order_by(desc(MovimientoInventario.fecha_movimiento)).all()

    @staticmethod
    def get_by_fecha_rango(fecha_inicio, fecha_fin):
        return MovimientoInventario.query.filter(
            and_(
                MovimientoInventario.fecha_movimiento >= fecha_inicio,
                MovimientoInventario.fecha_movimiento <= fecha_fin
            )
        ).order_by(desc(MovimientoInventario.fecha_movimiento)).all()

class IngresoMercanciaRepo:
    @staticmethod
    def get_all():
        return IngresoMercancia.query.order_by(desc(IngresoMercancia.fecha_ingreso)).all()

    @staticmethod
    def get_by_id(id):
        return IngresoMercancia.query.get(id)

    @staticmethod
    def create(ingreso_data):
        try:
            ingreso = IngresoMercancia(**ingreso_data)
            db.session.add(ingreso)
            db.session.commit()
            return ingreso, None
        except IntegrityError as e:
            db.session.rollback()
            return None, str(e)
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def update(id, ingreso_data):
        try:
            ingreso = IngresoMercancia.query.get(id)
            if not ingreso:
                return None, "Ingreso de mercancía no encontrado"
            
            for key, value in ingreso_data.items():
                if hasattr(ingreso, key):
                    setattr(ingreso, key, value)
            
            db.session.commit()
            return ingreso, None
        except IntegrityError as e:
            db.session.rollback()
            return None, str(e)
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def delete(id):
        try:
            ingreso = IngresoMercancia.query.get(id)
            if not ingreso:
                return False, "Ingreso de mercancía no encontrado"
            
            db.session.delete(ingreso)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)

class DetalleIngresoMercanciaRepo:
    @staticmethod
    def get_by_ingreso_id(ingreso_id):
        return DetalleIngresoMercancia.query.filter_by(ingreso_mercancia_id=ingreso_id).all()

    @staticmethod
    def get_by_id(id):
        return DetalleIngresoMercancia.query.get(id)

    @staticmethod
    def create(detalle_data):
        try:
            detalle = DetalleIngresoMercancia(**detalle_data)
            db.session.add(detalle)
            db.session.commit()
            return detalle, None
        except IntegrityError as e:
            db.session.rollback()
            return None, str(e)
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def update(id, detalle_data):
        try:
            detalle = DetalleIngresoMercancia.query.get(id)
            if not detalle:
                return None, "Detalle de ingreso no encontrado"
            
            for key, value in detalle_data.items():
                if hasattr(detalle, key):
                    setattr(detalle, key, value)
            
            db.session.commit()
            return detalle, None
        except IntegrityError as e:
            db.session.rollback()
            return None, str(e)
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def delete(id):
        try:
            detalle = DetalleIngresoMercancia.query.get(id)
            if not detalle:
                return False, "Detalle de ingreso no encontrado"
            
            db.session.delete(detalle)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)