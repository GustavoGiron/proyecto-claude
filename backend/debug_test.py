#!/usr/bin/env python3

import sys
import traceback

try:
    from app import create_app
    print("✓ App creation successful")
    
    app = create_app()
    print("✓ App instance created")
    
    with app.app_context():
        print("✓ App context entered")
        
        from app.models.productos_model import Producto
        print("✓ Producto model imported")
        
        from app.models.inventario_model import Inventario
        print("✓ Inventario model imported")
        
        # Test basic query
        productos = Producto.query.all()
        print(f"✓ Found {len(productos)} productos")
        
        inventarios = Inventario.query.all()
        print(f"✓ Found {len(inventarios)} inventarios")
        
        print("✓ All models working correctly")
        
except Exception as e:
    print(f"✗ Error: {e}")
    print(f"✗ Exception type: {type(e).__name__}")
    print("✗ Full traceback:")
    traceback.print_exc()