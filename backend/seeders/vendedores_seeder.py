from app import create_app, db
from app.models.vendedores_model import Vendedor
from datetime import datetime

def seed_vendedores():
    """Crear 10 vendedores de prueba"""
    vendedores_data = [
        {
            "codigo_vendedor": "V001",
            "nombres": "Carlos Alberto",
            "apellidos": "Mendoza García",
            "telefono": "5501-2345",
            "direccion": "5ta Avenida 10-25 Zona 1",
            "porcentaje_comision": 5.0,
            "usuario_creacion": "admin"
        },
        {
            "codigo_vendedor": "V002",
            "nombres": "Ana María",
            "apellidos": "López Rodríguez",
            "telefono": "5502-3456",
            "direccion": "12 Calle 8-30 Zona 2",
            "porcentaje_comision": 6.0,
            "usuario_creacion": "admin"
        },
        {
            "codigo_vendedor": "V003",
            "nombres": "José Luis",
            "apellidos": "Martínez Pérez",
            "telefono": "5503-4567",
            "direccion": "Boulevard Vista Hermosa 15-40 Zona 3",
            "porcentaje_comision": 4.5,
            "usuario_creacion": "admin"
        },
        {
            "codigo_vendedor": "V004",
            "nombres": "María Elena",
            "apellidos": "González Hernández",
            "telefono": "5504-5678",
            "direccion": "3ra Calle 20-15 Zona 4",
            "porcentaje_comision": 5.5,
            "usuario_creacion": "admin"
        },
        {
            "codigo_vendedor": "V005",
            "nombres": "Roberto Carlos",
            "apellidos": "Ramírez Díaz",
            "telefono": "5505-6789",
            "direccion": "Avenida Central 25-50 Zona 5",
            "porcentaje_comision": 7.0,
            "usuario_creacion": "admin"
        },
        {
            "codigo_vendedor": "V006",
            "nombres": "Laura Patricia",
            "apellidos": "Sánchez Morales",
            "telefono": "5506-7890",
            "direccion": "6ta Avenida 30-20 Zona 6",
            "porcentaje_comision": 5.0,
            "usuario_creacion": "admin"
        },
        {
            "codigo_vendedor": "V007",
            "nombres": "Fernando José",
            "apellidos": "Castro Flores",
            "telefono": "5507-8901",
            "direccion": "Calzada Principal 35-60 Zona 7",
            "porcentaje_comision": 6.5,
            "usuario_creacion": "admin"
        },
        {
            "codigo_vendedor": "V008",
            "nombres": "Sandra Beatriz",
            "apellidos": "Vásquez López",
            "telefono": "5508-9012",
            "direccion": "8va Calle 40-30 Zona 8",
            "porcentaje_comision": 4.0,
            "usuario_creacion": "admin"
        },
        {
            "codigo_vendedor": "V009",
            "nombres": "Miguel Ángel",
            "apellidos": "Herrera Mendoza",
            "telefono": "5509-0123",
            "direccion": "Diagonal 12 45-70 Zona 9",
            "porcentaje_comision": 5.5,
            "usuario_creacion": "admin"
        },
        {
            "codigo_vendedor": "V010",
            "nombres": "Patricia Isabel",
            "apellidos": "Morales García",
            "telefono": "5510-1234",
            "direccion": "10ma Avenida 50-80 Zona 10",
            "porcentaje_comision": 6.0,
            "usuario_creacion": "admin"
        }
    ]
    
    try:
        vendedores_creados = 0
        for data in vendedores_data:
            # Verificar si el vendedor ya existe
            vendedor_existente = Vendedor.query.filter_by(codigo_vendedor=data['codigo_vendedor']).first()
            if not vendedor_existente:
                vendedor = Vendedor(**data)
                db.session.add(vendedor)
                vendedores_creados += 1
            else:
                print(f"⚠️  Vendedor {data['codigo_vendedor']} ya existe, omitiendo...")
        
        db.session.commit()
        print(f"✓ {vendedores_creados} vendedores creados exitosamente")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"✗ Error al crear vendedores: {str(e)}")
        return False

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_vendedores()