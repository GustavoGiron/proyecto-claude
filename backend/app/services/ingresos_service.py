from app.repositories.ingresos_repo import IngresoMercanciaRepo, DetalleIngresoRepo
from typing import List, Optional, Dict, Any, Tuple

class IngresoMercanciaService:
    
    @staticmethod
    def get_all_ingresos() -> List[Dict[str, Any]]:
        """Obtener todos los ingresos de mercancía"""
        ingresos = IngresoMercanciaRepo.get_all()
        return [ingreso.to_dict() for ingreso in ingresos]
    
    @staticmethod
    def get_ingreso_by_id(ingreso_id: int) -> Optional[Dict[str, Any]]:
        """Obtener ingreso por ID con sus detalles"""
        ingreso = IngresoMercanciaRepo.get_by_id(ingreso_id)
        if ingreso:
            result = ingreso.to_dict()
            # Agregar detalles con información de productos
            result['detalles'] = [detalle.to_dict() for detalle in ingreso.detalles]
            return result
        return None
    
    @staticmethod
    def search_ingresos(numero_contenedor: str = None, numero_duca: str = None, 
                       fecha_desde: str = None, fecha_hasta: str = None) -> List[Dict[str, Any]]:
        """Buscar ingresos por diferentes criterios"""
        # Por ahora implementamos búsqueda básica
        if numero_contenedor:
            ingreso = IngresoMercanciaRepo.get_by_numero_contenedor(numero_contenedor)
            return [ingreso.to_dict()] if ingreso else []
        
        if numero_duca:
            ingreso = IngresoMercanciaRepo.get_by_numero_duca(numero_duca)
            return [ingreso.to_dict()] if ingreso else []
        
        # Si no hay criterios específicos, devolver todos
        return IngresoMercanciaService.get_all_ingresos()
    
    @staticmethod
    def create_ingreso_completo(data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Crear un ingreso de mercancía completo con sus detalles
        """
        # Separar datos del ingreso y detalles
        detalles_data = data.pop('detalles', [])
        
        if not detalles_data:
            return None, "Debe incluir al menos un detalle de producto"
        
        # Crear ingreso con detalles
        ingreso, error = IngresoMercanciaRepo.create_ingreso_completo(data, detalles_data)
        
        if error:
            return None, error
        
        return IngresoMercanciaService.get_ingreso_by_id(ingreso.id), None
    
    @staticmethod
    def update_ingreso(ingreso_id: int, data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Actualizar datos básicos del ingreso (sin detalles)"""
        # Remover detalles si vienen en los datos
        data.pop('detalles', None)
        
        ingreso, error = IngresoMercanciaRepo.update_ingreso(ingreso_id, data)
        
        if error:
            return None, error
        
        return IngresoMercanciaService.get_ingreso_by_id(ingreso.id), None
    
    @staticmethod
    def delete_ingreso(ingreso_id: int) -> Tuple[bool, Optional[str]]:
        """Eliminar ingreso completo"""
        return IngresoMercanciaRepo.delete_ingreso(ingreso_id)
    
    @staticmethod
    def confirmar_ingreso_a_inventario(ingreso_id: int, usuario_confirmacion: str = None) -> Tuple[bool, Optional[str]]:
        """
        Confirmar el ingreso y aplicar las cantidades al inventario
        """
        success, error = IngresoMercanciaRepo.confirmar_ingreso_a_inventario(
            ingreso_id, 
            usuario_confirmacion or "sistema"
        )
        
        if error:
            return False, error
        
        return True, "Ingreso confirmado exitosamente. Inventarios actualizados."

class DetalleIngresoService:
    
    @staticmethod
    def get_detalles_by_ingreso(ingreso_id: int) -> List[Dict[str, Any]]:
        """Obtener detalles de un ingreso específico"""
        detalles = DetalleIngresoRepo.get_by_ingreso(ingreso_id)
        return [detalle.to_dict() for detalle in detalles]
    
    @staticmethod
    def add_detalle_to_ingreso(ingreso_id: int, data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Agregar un detalle a un ingreso existente"""
        detalle, error = DetalleIngresoRepo.add_detalle(ingreso_id, data)
        
        if error:
            return None, error
        
        return detalle.to_dict(), None
    
    @staticmethod
    def update_detalle(detalle_id: int, data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Actualizar un detalle específico"""
        detalle, error = DetalleIngresoRepo.update_detalle(detalle_id, data)
        
        if error:
            return None, error
        
        return detalle.to_dict(), None
    
    @staticmethod
    def delete_detalle(detalle_id: int) -> Tuple[bool, Optional[str]]:
        """Eliminar un detalle específico"""
        return DetalleIngresoRepo.delete_detalle(detalle_id)
    
    @staticmethod
    def calculate_totales_ingreso(ingreso_id: int) -> Dict[str, Any]:
        """Calcular totales del ingreso"""
        detalles = DetalleIngresoRepo.get_by_ingreso(ingreso_id)
        
        total_fardos_paquetes = sum(d.cantidad_fardos_paquetes for d in detalles)
        total_unidades = sum(d.cantidad_fardos_paquetes * d.unidades_por_fardo_paquete for d in detalles)
        total_productos_diferentes = len(detalles)
        
        return {
            'total_productos_diferentes': total_productos_diferentes,
            'total_fardos_paquetes': total_fardos_paquetes,
            'total_unidades': total_unidades,
            'detalles': [d.to_dict() for d in detalles]
        }