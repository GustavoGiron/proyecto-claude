# backend/app/dtos/clientes_dto.py

from app import ma
from app.models.clientes_model import Cliente

class ClienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cliente
        load_instance = True
        include_fk = True
        # exponemos todos los campos necesarios
        fields = (
            "id",
            "numero_cliente",
            "codigo_cliente",
            "nombre_contacto",
            "nombre_negocio",
            "departamento_id",
            "municipio_id",
            "direccion",
            "nit",
            "encargado_bodega",
            "telefono",
            "tipo_venta_autoriz",
            "observaciones",
            "fecha_creacion",
            "fecha_modificacion",
            "usuario_creacion",
            "usuario_modificacion",
            "estado"
        )
