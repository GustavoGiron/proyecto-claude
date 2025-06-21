from app import db
from app.models.ventas_model import Venta, DetalleVenta, Pago, Comision
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, or_

class VentaRepo:
    @staticmethod
    def get_all():
        return Venta.query.order_by(desc(Venta.fecha_venta)).all()

    @staticmethod
    def get_by_id(id):
        return Venta.query.get(id)

    @staticmethod
    def get_by_numero_envio(numero_envio):
        return Venta.query.filter_by(numero_envio=numero_envio).first()

    @staticmethod
    def create(venta_data):
        try:
            venta = Venta(**venta_data)
            db.session.add(venta)
            db.session.commit()
            return venta, None
        except IntegrityError as e:
            db.session.rollback()
            return None, str(e)
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def update(id, venta_data):
        try:
            venta = Venta.query.get(id)
            if not venta:
                return None, "Venta no encontrada"
            
            for key, value in venta_data.items():
                if hasattr(venta, key):
                    setattr(venta, key, value)
            
            db.session.commit()
            return venta, None
        except IntegrityError as e:
            db.session.rollback()
            return None, str(e)
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def delete(id):
        try:
            venta = Venta.query.get(id)
            if not venta:
                return False, "Venta no encontrada"
            
            db.session.delete(venta)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def search(numero_envio=None, cliente_nombre=None, estado_venta=None, estado_cobro=None):
        query = Venta.query
        
        if numero_envio:
            query = query.filter(Venta.numero_envio.ilike(f'%{numero_envio}%'))
        
        if cliente_nombre:
            query = query.join(Venta.cliente).filter(
                or_(
                    db.text("Clientes.NombreContacto LIKE :nombre"),
                    db.text("Clientes.NombreNegocio LIKE :nombre")
                )
            ).params(nombre=f'%{cliente_nombre}%')
        
        if estado_venta:
            query = query.filter(Venta.estado_venta == estado_venta)
            
        if estado_cobro:
            query = query.filter(Venta.estado_cobro == estado_cobro)
        
        return query.order_by(desc(Venta.fecha_venta)).all()

    @staticmethod
    def get_ventas_pendientes_cobro():
        return Venta.query.filter(
            Venta.estado_cobro.in_(['Pendiente', 'Parcial', 'Morosa'])
        ).order_by(desc(Venta.fecha_venta)).all()

    @staticmethod
    def get_ventas_pendientes_entrega():
        return Venta.query.filter(
            Venta.estado_entrega == 'Pendiente'
        ).order_by(desc(Venta.fecha_venta)).all()

    @staticmethod
    def get_max_numero_envio():
        """Obtiene el número más alto de envío para generar el siguiente"""
        ventas = Venta.query.with_entities(Venta.numero_envio).all()
        max_num = 0
        
        for (numero_envio,) in ventas:
            # Extrae la parte numérica del número de envío
            if numero_envio and numero_envio.startswith('ENV'):
                try:
                    num = int(numero_envio[3:])
                    max_num = max(max_num, num)
                except ValueError:
                    continue
        
        return max_num

class DetalleVentaRepo:
    @staticmethod
    def get_by_venta_id(venta_id):
        return DetalleVenta.query.filter_by(venta_id=venta_id).all()

    @staticmethod
    def get_by_id(id):
        return DetalleVenta.query.get(id)

    @staticmethod
    def create(detalle_data):
        try:
            detalle = DetalleVenta(**detalle_data)
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
            detalle = DetalleVenta.query.get(id)
            if not detalle:
                return None, "Detalle de venta no encontrado"
            
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
            detalle = DetalleVenta.query.get(id)
            if not detalle:
                return False, "Detalle de venta no encontrado"
            
            db.session.delete(detalle)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def delete_by_venta_id(venta_id):
        try:
            detalles = DetalleVenta.query.filter_by(venta_id=venta_id).all()
            for detalle in detalles:
                db.session.delete(detalle)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)

class PagoRepo:
    @staticmethod
    def get_by_venta_id(venta_id):
        return Pago.query.filter_by(venta_id=venta_id).order_by(desc(Pago.fecha_pago)).all()

    @staticmethod
    def get_by_id(id):
        return Pago.query.get(id)

    @staticmethod
    def create(pago_data):
        try:
            pago = Pago(**pago_data)
            db.session.add(pago)
            db.session.commit()
            return pago, None
        except IntegrityError as e:
            db.session.rollback()
            return None, str(e)
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def update(id, pago_data):
        try:
            pago = Pago.query.get(id)
            if not pago:
                return None, "Pago no encontrado"
            
            for key, value in pago_data.items():
                if hasattr(pago, key):
                    setattr(pago, key, value)
            
            db.session.commit()
            return pago, None
        except IntegrityError as e:
            db.session.rollback()
            return None, str(e)
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def delete(id):
        try:
            pago = Pago.query.get(id)
            if not pago:
                return False, "Pago no encontrado"
            
            db.session.delete(pago)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)

class ComisionRepo:
    @staticmethod
    def get_by_venta_id(venta_id):
        return Comision.query.filter_by(venta_id=venta_id).first()

    @staticmethod
    def get_by_vendedor_id(vendedor_id):
        return Comision.query.filter_by(vendedor_id=vendedor_id).order_by(desc(Comision.fecha_generacion)).all()

    @staticmethod
    def get_by_id(id):
        return Comision.query.get(id)

    @staticmethod
    def create(comision_data):
        try:
            comision = Comision(**comision_data)
            db.session.add(comision)
            db.session.commit()
            return comision, None
        except IntegrityError as e:
            db.session.rollback()
            return None, str(e)
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def update(id, comision_data):
        try:
            comision = Comision.query.get(id)
            if not comision:
                return None, "Comisión no encontrada"
            
            for key, value in comision_data.items():
                if hasattr(comision, key):
                    setattr(comision, key, value)
            
            db.session.commit()
            return comision, None
        except IntegrityError as e:
            db.session.rollback()
            return None, str(e)
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def get_comisiones_pendientes():
        return Comision.query.filter_by(estado_comision='Pendiente').order_by(desc(Comision.fecha_generacion)).all()