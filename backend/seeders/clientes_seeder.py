from app import create_app, db
from app.models.clientes_model import Cliente
from datetime import datetime

def seed_clientes():
    """Crear 10 clientes de prueba"""
    clientes_data = [
        {
            "numero_cliente": 1001,
            "codigo_cliente": "C001",
            "nombre_contacto": "Juan Pérez García",
            "nombre_negocio": "Ferretería El Martillo",
            "departamento_id": 1,
            "municipio_id": 1,
            "direccion": "4ta Calle 3-45 Zona 1",
            "nit": "1234567-8",
            "encargado_bodega": "Pedro López",
            "telefono": "5551-2345",
            "tipo_venta_autoriz": "Ambas",
            "observaciones": "Cliente frecuente, buen historial de pagos",
            "usuario_creacion": "admin"
        },
        {
            "numero_cliente": 1002,
            "codigo_cliente": "C002",
            "nombre_contacto": "María Rodríguez",
            "nombre_negocio": "Tienda La Económica",
            "departamento_id": 1,
            "municipio_id": 1,
            "direccion": "Avenida Central 10-20 Zona 3",
            "nit": "2345678-9",
            "encargado_bodega": "Carlos Méndez",
            "telefono": "5552-3456",
            "tipo_venta_autoriz": "Credito",
            "observaciones": "Cliente desde 2020",
            "usuario_creacion": "admin"
        },
        {
            "numero_cliente": 1003,
            "codigo_cliente": "C003",
            "nombre_contacto": "Luis Martínez",
            "nombre_negocio": "Distribuidora San José",
            "departamento_id": 1,
            "municipio_id": 1,
            "direccion": "12 Avenida 5-67 Zona 4",
            "nit": "3456789-0",
            "encargado_bodega": "Ana Morales",
            "telefono": "5553-4567",
            "tipo_venta_autoriz": "Contado",
            "observaciones": "Solo compras al contado",
            "usuario_creacion": "admin"
        },
        {
            "numero_cliente": 1004,
            "codigo_cliente": "C004",
            "nombre_contacto": "Carmen González",
            "nombre_negocio": "Abarrotería Mi Pueblo",
            "departamento_id": 1,
            "municipio_id": 1,
            "direccion": "3ra Avenida 8-90 Zona 2",
            "nit": "4567890-1",
            "encargado_bodega": "José Ramírez",
            "telefono": "5554-5678",
            "tipo_venta_autoriz": "Ambas",
            "observaciones": "Compras mensuales regulares",
            "usuario_creacion": "admin"
        },
        {
            "numero_cliente": 1005,
            "codigo_cliente": "C005",
            "nombre_contacto": "Roberto Díaz",
            "nombre_negocio": "Comercial El Ahorro",
            "departamento_id": 1,
            "municipio_id": 1,
            "direccion": "Boulevard Principal 15-30 Zona 5",
            "nit": "5678901-2",
            "encargado_bodega": "Patricia Flores",
            "telefono": "5555-6789",
            "tipo_venta_autoriz": "Credito",
            "observaciones": "Cliente VIP, descuentos especiales",
            "usuario_creacion": "admin"
        },
        {
            "numero_cliente": 1006,
            "codigo_cliente": "C006",
            "nombre_contacto": "Alejandra Sánchez",
            "nombre_negocio": "Mini Market Express",
            "departamento_id": 1,
            "municipio_id": 1,
            "direccion": "6ta Calle 12-34 Zona 6",
            "nit": "6789012-3",
            "encargado_bodega": "Miguel Herrera",
            "telefono": "5556-7890",
            "tipo_venta_autoriz": "Contado",
            "observaciones": "Pagos inmediatos",
            "usuario_creacion": "admin"
        },
        {
            "numero_cliente": 1007,
            "codigo_cliente": "C007",
            "nombre_contacto": "Fernando Castro",
            "nombre_negocio": "Depósito La Confianza",
            "departamento_id": 1,
            "municipio_id": 1,
            "direccion": "Calzada Principal 20-45 Zona 7",
            "nit": "7890123-4",
            "encargado_bodega": "Laura Vásquez",
            "telefono": "5557-8901",
            "tipo_venta_autoriz": "Ambas",
            "observaciones": "Compras por volumen",
            "usuario_creacion": "admin"
        },
        {
            "numero_cliente": 1008,
            "codigo_cliente": "C008",
            "nombre_contacto": "Patricia López",
            "nombre_negocio": "Supermercado Central",
            "departamento_id": 1,
            "municipio_id": 1,
            "direccion": "1ra Avenida 25-67 Zona 8",
            "nit": "8901234-5",
            "encargado_bodega": "Ricardo Morales",
            "telefono": "5558-9012",
            "tipo_venta_autoriz": "Credito",
            "observaciones": "Cadena de supermercados",
            "usuario_creacion": "admin"
        },
        {
            "numero_cliente": 1009,
            "codigo_cliente": "C009",
            "nombre_contacto": "Diego Ramírez",
            "nombre_negocio": "Almacén Don Diego",
            "departamento_id": 1,
            "municipio_id": 1,
            "direccion": "9na Calle 30-12 Zona 9",
            "nit": "9012345-6",
            "encargado_bodega": "Sofía Mendoza",
            "telefono": "5559-0123",
            "tipo_venta_autoriz": "Contado",
            "observaciones": "Cliente nuevo",
            "usuario_creacion": "admin"
        },
        {
            "numero_cliente": 1010,
            "codigo_cliente": "C010",
            "nombre_contacto": "Andrea Flores",
            "nombre_negocio": "Distribuidora Las Flores",
            "departamento_id": 1,
            "municipio_id": 1,
            "direccion": "Diagonal 10 35-89 Zona 10",
            "nit": "0123456-7",
            "encargado_bodega": "Manuel García",
            "telefono": "5550-1234",
            "tipo_venta_autoriz": "Ambas",
            "observaciones": "Excelente relación comercial",
            "usuario_creacion": "admin"
        }
    ]
    
    try:
        clientes_creados = 0
        for data in clientes_data:
            # Verificar si el cliente ya existe
            cliente_existente = Cliente.query.filter_by(codigo_cliente=data['codigo_cliente']).first()
            if not cliente_existente:
                cliente = Cliente(**data)
                db.session.add(cliente)
                clientes_creados += 1
            else:
                print(f"⚠️  Cliente {data['codigo_cliente']} ya existe, omitiendo...")
        
        db.session.commit()
        print(f"✓ {clientes_creados} clientes creados exitosamente")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"✗ Error al crear clientes: {str(e)}")
        return False

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_clientes()