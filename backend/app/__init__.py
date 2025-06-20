# backend/app/__init__.py

import os
from flask import Flask, jsonify
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

from .config import Config
from .utils.validators import ValidationError

# Instancias singleton
db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configurar CORS
    CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000'], 
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         allow_headers=['Content-Type', 'Authorization'])

    # Inicializa extensiones
    db.init_app(app)
    ma.init_app(app)

    # -------------------------------------------------
    # Configuración de Swagger / OpenAPI
    # -------------------------------------------------
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title":       "Imporcomgua API",
            "version":     "1.0.0",
            "description": "Documentación automática con Swagger"
        },
        # Evitamos doble slash en las rutas de Swagger UI
        "host":     "127.0.0.1:5000",
        "basePath": "",
        "schemes":  ["http"],
        "definitions": {
            "Cliente": {
                "type": "object",
                "properties": {
                    "id":                   {"type": "integer"},
                    "numero_cliente":       {"type": "integer"},
                    "codigo_cliente":       {"type": "string"},
                    "nombre_contacto":      {"type": "string"},
                    "nombre_negocio":       {"type": "string"},
                    "departamento_id":      {"type": "integer"},
                    "municipio_id":         {"type": "integer"},
                    "direccion":            {"type": "string"},
                    "nit":                  {"type": "string"},
                    "encargado_bodega":     {"type": "string"},
                    "telefono":             {"type": "string"},
                    "tipo_venta_autoriz":   {
                                              "type": "string",
                                              "enum": ["Credito","Contado","Ambas"]
                                            },
                    "observaciones":        {"type": "string"},
                    "usuario_creacion":     {"type": "string"},
                    "usuario_modificacion": {"type": "string"},
                    "fecha_creacion":       {"type": "string", "format":"date-time"},
                    "fecha_modificacion":   {"type": "string", "format":"date-time"},
                    "estado":               {"type": "boolean"}
                },
                "required": [
                    "nombre_contacto",
                    "departamento_id",
                    "municipio_id",
                    "tipo_venta_autoriz"
                ]
            },
            "Departamento": {
                "type": "object",
                "properties": {
                    "id":     {"type": "integer"},
                    "codigo": {"type": "string"},
                    "nombre": {"type": "string"}
                }
            },
            "Municipio": {
                "type": "object",
                "properties": {
                    "id":               {"type": "integer"},
                    "departamento_id":  {"type": "integer"},
                    "nombre":           {"type": "string"}
                }
            }
        }
    }

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint":    "apispec",
                "route":       "/apispec.json",
                "rule_filter":  lambda rule: True,
                "model_filter": lambda tag: True
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui":       True,
        "specs_route":      "/docs/"
    }

    Swagger(app, template=swagger_template, config=swagger_config)
    # -------------------------------------------------

    # Manejador global de ValidationError
    @app.errorhandler(ValidationError)
    def handle_validation_error(err: ValidationError):
        return jsonify({"code": err.code, "message": err.message}), 400

    # Registrar blueprints
    from app.api import (
        clientes_bp,
        departamentos_bp,
        productos_bp,
        inventario_bp
    )

    app.register_blueprint(clientes_bp,      url_prefix='/api/clientes')
    app.register_blueprint(departamentos_bp, url_prefix='/api/departamentos')
    app.register_blueprint(productos_bp,     url_prefix='/api/productos')
    app.register_blueprint(inventario_bp,    url_prefix='/api/inventario')

    return app

# Entry point
from app import create_app
app = create_app()

if __name__ == "__main__":
    # Asumimos que las migraciones ya crearon las tablas
    app.run(debug=True, port=5000)