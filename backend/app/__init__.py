# backend/app/__init__.py

import os
from flask import Flask, jsonify
from flasgger import Swagger
from flask_marshmallow import Marshmallow
from flask_cors import CORS

from .config import Config
from .utils.validators import ValidationError
from .utils.emailalert import enviar_alerta_stock_bajo
from .database import db

# Instancias singleton
ma = Marshmallow()

def create_app(testing=False):
    app = Flask(__name__)

    if testing:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URI')
        app.config['WTF_CSRF_ENABLED'] = False  
    else:  
        app.config.from_object(Config)

    
    app.config['ENV']   = os.getenv('FLASK_ENV', 'production')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'

    # Configurar CORS
    CORS(app,
     origins=[
         "http://34.57.96.87",
         "http://127.0.0.1:4200",
         "http://127.0.0.1:3000",
         "http://localhost:4200",
         "http://localhost:3000"
     ],
     supports_credentials=True,
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"])
    # CORS(app, origins=['*'],
    #      methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    #      allow_headers=['Content-Type', 'Authorization'])

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
        "host":     os.getenv("SWAGGER_HOST", "localhost"),
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
            },"Vendedor": {
                "type": "object",
                "properties": {
                    "id":                   {"type": "integer", "description": "ID único del vendedor"},
                    "codigo_vendedor":      {"type": "string", "description": "Código automático del vendedor (ej: V001, V002)"},
                    "nombres":              {"type": "string", "maxLength": 100, "description": "Nombres del vendedor"},
                    "apellidos":            {"type": "string", "maxLength": 100, "description": "Apellidos del vendedor"},
                    "nombre_completo":      {"type": "string", "description": "Nombres y apellidos concatenados"},
                    "telefono":             {"type": "string", "maxLength": 20, "description": "Teléfono del vendedor (formato: 0000-0000)"},
                    "direccion":            {"type": "string", "description": "Dirección del vendedor"},
                    "porcentaje_comision":  {
                                              "type": "number", 
                                              "minimum": 0, 
                                              "maximum": 100,
                                              "description": "Porcentaje de comisión (0-100)"
                                            },
                    "fecha_modificacion":   {"type": "string", "format": "date-time", "description": "Fecha de última modificación"},
                    "usuario_creacion":     {"type": "string", "maxLength": 50, "description": "Usuario que creó el registro"},
                    "usuario_modificacion": {"type": "string", "maxLength": 50, "description": "Usuario que modificó el registro"}
                },
                "required": [
                    "nombres",
                    "apellidos",
                    "porcentaje_comision"
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
            },
            "Venta": {
                "type": "object",
                "properties": {
                    "id":                   {"type": "integer"},
                    "fecha_venta":          {"type": "string", "format": "date"},
                    "fecha_salida_bodega":  {"type": "string", "format": "date"},
                    "cliente_id":           {"type": "integer"},
                    "nit_cliente":          {"type": "string"},
                    "numero_envio":         {"type": "string"},
                    "tipo_pago":            {"type": "string", "enum": ["Contado", "Credito"]},
                    "dias_credito":         {"type": "integer"},
                    #"fecha_vencimiento":    {"type": "string", "format": "date"},
                    "vendedor_id":          {"type": "integer"},
                    "numero_factura_dte":   {"type": "string"},
                    "nombre_factura":       {"type": "string"},
                    "nit_factura":          {"type": "string"},
                    "subtotal_venta":       {"type": "number"},
                    "iva_venta":            {"type": "number"},
                    "total_venta":          {"type": "number"},
                    "estado_venta":         {"type": "string", "enum": ["Vigente", "Anulada"]},
                    "estado_cobro":         {"type": "string", "enum": ["Pendiente", "Parcial", "Pagada", "Morosa"]},
                    "estado_entrega":       {"type": "string", "enum": ["Pendiente", "Entregado"]},
                    "fecha_pago_completo":  {"type": "string", "format": "date"},
                    "saldo_pendiente":      {"type": "number"},
                    "fecha_modificacion":   {"type": "string", "format": "date-time"},
                    "usuario_creacion":     {"type": "string"},
                    "usuario_modificacion": {"type": "string"}
                }
            },
            "DetalleVenta": {
                "type": "object",
                "properties": {
                    "id":                       {"type": "integer"},
                    "venta_id":                 {"type": "integer"},
                    "producto_id":              {"type": "integer"},
                    "cantidad":                 {"type": "integer"},
                    "cantidad_unidades":        {"type": "integer"},
                    "precio_por_fardo_paquete": {"type": "number"},
                    "subtotal_linea":           {"type": "number"},
                    "iva_linea":                {"type": "number"},
                    "total_linea":              {"type": "number"},
                    "estado_linea":             {"type": "string", "enum": ["Pendiente", "Entregado"]},
                    "observaciones":            {"type": "string"},
                    "usuario_creacion":         {"type": "string"}
                }
            },
            "Pago": {
                "type": "object",
                "properties": {
                    "id":                   {"type": "integer"},
                    "venta_id":             {"type": "integer"},
                    "numero_recibo_caja":   {"type": "string"},
                    "fecha_pago":           {"type": "string", "format": "date"},
                    "banco":                {"type": "string", "enum": ["Industrial", "Banrural", "G&T", "BAM"]},
                    "numero_cuenta":        {"type": "string"},
                    "numero_transferencia": {"type": "string"},
                    "monto_abono":          {"type": "number"},
                    "saldo_anterior":       {"type": "number"},
                    "saldo_actual":         {"type": "number"},
                    "fecha_creacion":       {"type": "string", "format": "date-time"},
                    "usuario_creacion":     {"type": "string"}
                }
            },
            "Comision": {
                "type": "object",
                "properties": {
                    "id":                   {"type": "integer"},
                    "venta_id":             {"type": "integer"},
                    "vendedor_id":          {"type": "integer"},
                    "total_neto_venta":     {"type": "number"},
                    "porcentaje_aplicado":  {"type": "number"},
                    "monto_comision":       {"type": "number"},
                    "estado_comision":      {"type": "string", "enum": ["Pendiente", "Pagada"]},
                    "fecha_generacion":     {"type": "string", "format": "date-time"},
                    "fecha_pago":           {"type": "string", "format": "date"},
                    "usuario_pago":         {"type": "string"},
                    "observaciones":        {"type": "string"}
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
        inventario_bp,
        vendedores_bp,
        ventas_bp,
        ingresos_bp,
        usuarios_bp
    )
    from app.api.auth_api import auth_bp

    app.register_blueprint(auth_bp,          url_prefix='/api/auth')
    app.register_blueprint(clientes_bp,      url_prefix='/api/clientes')
    app.register_blueprint(departamentos_bp, url_prefix='/api/departamentos')
    app.register_blueprint(productos_bp,     url_prefix='/api/productos')
    app.register_blueprint(inventario_bp,    url_prefix='/api/inventario')
    app.register_blueprint(vendedores_bp,    url_prefix='/api/vendedores')
    app.register_blueprint(ventas_bp,        url_prefix='/api/ventas')
    app.register_blueprint(ingresos_bp,      url_prefix='/api/ingresos')
    app.register_blueprint(usuarios_bp,     url_prefix='/api/usuarios')

    return app