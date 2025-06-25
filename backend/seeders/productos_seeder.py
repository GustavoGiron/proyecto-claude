from app import create_app, db
from app.models.productos_model import Producto
from datetime import datetime

def seed_productos():
    """Crear 10 productos de prueba"""
    productos_data = [
        {
            "codigo_producto": "CEMT-001",
            "nombre_producto": "Cemento Portland Tipo I - Bolsa 42.5kg",
            "unidad_medida": "Unidad",
            "unidades_por_fardo_paquete": 1,
            "stock_minimo": 100,
            "usuario_creacion": "admin"
        },
        {
            "codigo_producto": "HIER-001",
            "nombre_producto": "Hierro Corrugado 3/8\" - Varilla 6m",
            "unidad_medida": "Unidad",
            "unidades_por_fardo_paquete": 1,
            "stock_minimo": 200,
            "usuario_creacion": "admin"
        },
        {
            "codigo_producto": "HIER-002",
            "nombre_producto": "Hierro Corrugado 1/2\" - Varilla 6m",
            "unidad_medida": "Unidad",
            "unidades_por_fardo_paquete": 1,
            "stock_minimo": 150,
            "usuario_creacion": "admin"
        },
        {
            "codigo_producto": "CLAV-001",
            "nombre_producto": "Clavos de Acero 2\" - Caja 5lb",
            "unidad_medida": "Paquete",
            "unidades_por_fardo_paquete": 12,
            "stock_minimo": 50,
            "usuario_creacion": "admin"
        },
        {
            "codigo_producto": "CLAV-002",
            "nombre_producto": "Clavos de Acero 3\" - Caja 5lb",
            "unidad_medida": "Paquete",
            "unidades_por_fardo_paquete": 12,
            "stock_minimo": 40,
            "usuario_creacion": "admin"
        },
        {
            "codigo_producto": "PINT-001",
            "nombre_producto": "Pintura Látex Blanca - Galón",
            "unidad_medida": "Unidad",
            "unidades_por_fardo_paquete": 1,
            "stock_minimo": 30,
            "usuario_creacion": "admin"
        },
        {
            "codigo_producto": "PINT-002",
            "nombre_producto": "Pintura Anticorrosiva Roja - Galón",
            "unidad_medida": "Unidad",
            "unidades_por_fardo_paquete": 1,
            "stock_minimo": 25,
            "usuario_creacion": "admin"
        },
        {
            "codigo_producto": "TUBE-001",
            "nombre_producto": "Tubo PVC 1/2\" - 6 metros",
            "unidad_medida": "Unidad",
            "unidades_por_fardo_paquete": 1,
            "stock_minimo": 100,
            "usuario_creacion": "admin"
        },
        {
            "codigo_producto": "TUBE-002",
            "nombre_producto": "Tubo PVC 3/4\" - 6 metros",
            "unidad_medida": "Unidad",
            "unidades_por_fardo_paquete": 1,
            "stock_minimo": 80,
            "usuario_creacion": "admin"
        },
        {
            "codigo_producto": "ELEC-001",
            "nombre_producto": "Cable Eléctrico THHN #12 - Rollo 100m",
            "unidad_medida": "Fardo",
            "unidades_por_fardo_paquete": 10,
            "stock_minimo": 20,
            "usuario_creacion": "admin"
        }
    ]
    
    try:
        productos_creados = 0
        for data in productos_data:
            # Verificar si el producto ya existe
            producto_existente = Producto.query.filter_by(codigo_producto=data['codigo_producto']).first()
            if not producto_existente:
                producto = Producto(**data)
                db.session.add(producto)
                productos_creados += 1
            else:
                print(f"⚠️  Producto {data['codigo_producto']} ya existe, omitiendo...")
        
        db.session.commit()
        print(f"✓ {productos_creados} productos creados exitosamente")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"✗ Error al crear productos: {str(e)}")
        return False

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_productos()