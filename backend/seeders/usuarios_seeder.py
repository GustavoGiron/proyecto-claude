#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from app.config import Config
from app.database import db
from app.models.usuarios_model import Usuario
from app.models.roles_model import Role


def seed_usuarios():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    with app.app_context():
        try:
            # Verificar si ya existen usuarios
            if Usuario.query.count() > 0:
                print("Ya existen usuarios en la base de datos")
                return
            
            # Obtener los roles
            role_general = Role.query.filter_by(nombre='Gerencia General').first()
            role_ventas = Role.query.filter_by(nombre='Gerencia de Ventas y Finanzas').first()
            role_inventario = Role.query.filter_by(nombre='Gerencia de Inventario').first()
            
            if not all([role_general, role_ventas, role_inventario]):
                print("Error: No se encontraron todos los roles necesarios")
                return
            
            # Crear usuarios de prueba
            usuarios = [
                {
                    'username': 'admin',
                    'email': 'admin@imporcomgua.com',
                    'password': 'admin123',
                    'nombre': 'Administrador',
                    'apellido': 'General',
                    'role_id': role_general.id
                },
                {
                    'username': 'gerente_ventas',
                    'email': 'ventas@imporcomgua.com',
                    'password': 'ventas123',
                    'nombre': 'Juan',
                    'apellido': 'Pérez',
                    'role_id': role_ventas.id
                },
                {
                    'username': 'gerente_inventario',
                    'email': 'inventario@imporcomgua.com',
                    'password': 'inventario123',
                    'nombre': 'María',
                    'apellido': 'González',
                    'role_id': role_inventario.id
                }
            ]
            
            for user_data in usuarios:
                usuario = Usuario(
                    username=user_data['username'],
                    email=user_data['email'],
                    nombre=user_data['nombre'],
                    apellido=user_data['apellido'],
                    role_id=user_data['role_id']
                )
                usuario.set_password(user_data['password'])
                db.session.add(usuario)
                print(f"✅ Usuario creado: {usuario.username}")
            
            db.session.commit()
            print("\n✅ Seeder de usuarios ejecutado exitosamente")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al ejecutar seeder: {str(e)}")


if __name__ == "__main__":
    seed_usuarios()