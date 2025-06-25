#!/usr/bin/env python3
"""
Script principal para ejecutar todos los seeders
Uso: python seeders/run_seeders.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from seeders.clientes_seeder import seed_clientes
from seeders.productos_seeder import seed_productos
from seeders.vendedores_seeder import seed_vendedores

def run_all_seeders():
    """Ejecutar todos los seeders en orden"""
    app = create_app()
    
    with app.app_context():
        print("🌱 Iniciando proceso de seeding...")
        print("-" * 50)
        
        # Seeders a ejecutar
        seeders = [
            ("Clientes", seed_clientes),
            ("Productos", seed_productos),
            ("Vendedores", seed_vendedores)
        ]
        
        success_count = 0
        
        for name, seeder_func in seeders:
            print(f"\n📌 Ejecutando seeder: {name}")
            if seeder_func():
                success_count += 1
            else:
                print(f"⚠️  Advertencia: El seeder {name} falló")
        
        print("\n" + "-" * 50)
        print(f"✅ Proceso completado: {success_count}/{len(seeders)} seeders ejecutados exitosamente")
        
        if success_count < len(seeders):
            print("⚠️  Algunos seeders fallaron. Revisa los mensajes de error arriba.")
            return False
        
        return True

if __name__ == "__main__":
    # Verificar que existan departamentos y municipios
    app = create_app()
    with app.app_context():
        from app.models.departamentos_model import Departamento
        from app.models.municipios_model import Municipio
        
        dept_count = Departamento.query.count()
        muni_count = Municipio.query.count()
        
        if dept_count == 0 or muni_count == 0:
            print("❌ Error: Debes crear departamentos y municipios antes de ejecutar estos seeders.")
            print(f"   Departamentos encontrados: {dept_count}")
            print(f"   Municipios encontrados: {muni_count}")
            print("\n💡 Asegúrate de tener al menos un departamento con ID=1 y un municipio con ID=1")
            sys.exit(1)
        
        # Ejecutar seeders
        success = run_all_seeders()
        sys.exit(0 if success else 1)