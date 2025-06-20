from flask import Blueprint, jsonify, request
from app.services.clientes_service import ClienteService
from app.dtos.clientes_dto import ClienteSchema
from app.utils.validators import validate_telefono
from app.utils.logger import handle_exceptions

clientes_bp = Blueprint('clientes_bp', __name__)
schema      = ClienteSchema()
many_schema = ClienteSchema(many=True)

@clientes_bp.route('/', methods=['GET'])
@handle_exceptions(servicio='Clientes', cod_mensaje=1001)
def list_clientes():
    """
    Listar clientes
    ---
    tags:
      - Clientes
    responses:
      200:
        description: Lista de clientes
        schema:
          type: array
          items:
            $ref: '#/definitions/Cliente'
    """
    return many_schema.jsonify(ClienteService.list_all()), 200

@clientes_bp.route('/<string:codigo>', methods=['GET'])
@handle_exceptions(servicio='Clientes', cod_mensaje=1002)
def get_cliente(codigo):
    """
    Obtener cliente por código
    ---
    tags:
      - Clientes
    parameters:
      - name: codigo
        in: path
        type: string
        required: true
        description: Código único del cliente
    responses:
      200:
        schema:
          $ref: '#/definitions/Cliente'
      404:
        description: No encontrado
    """
    cli = ClienteService.get_by_codigo(codigo)
    if not cli:
        return jsonify({"error": "No encontrado"}), 404
    return schema.jsonify(cli), 200

@clientes_bp.route('/', methods=['POST'])
@handle_exceptions(servicio='Clientes', cod_mensaje=1003)
def create_cliente():
    """
    Crear cliente (numero_cliente y codigo_cliente generados automáticamente)
    ---
    tags:
      - Clientes
    parameters:
      - in: body
        name: body
        schema:
          $ref: '#/definitions/Cliente'
    responses:
      201:
        description: Cliente creado con código generado
        schema:
          $ref: '#/definitions/Cliente'
      400:
        description: Error validación
    """
    data = request.get_json()
    validate_telefono(data.get('telefono',''))
    nuevo = ClienteService.create(data)
    return schema.jsonify(nuevo), 201

@clientes_bp.route('/<string:codigo>', methods=['PUT'])
@handle_exceptions(servicio='Clientes', cod_mensaje=1004)
def update_cliente(codigo):
    """
    Actualizar cliente por código
    ---
    tags:
      - Clientes
    parameters:
      - name: codigo
        in: path
        type: string
        required: true
        description: Código único del cliente
      - in: body
        name: body
        schema:
          $ref: '#/definitions/Cliente'
    responses:
      200:
        schema:
          $ref: '#/definitions/Cliente'
      404:
        description: No encontrado
    """
    data = request.get_json()
    validate_telefono(data.get('telefono',''))
    cli = ClienteService.update_by_codigo(codigo, data)
    if not cli:
        return jsonify({"error": "No encontrado"}), 404
    return schema.jsonify(cli), 200

@clientes_bp.route('/<string:codigo>', methods=['DELETE'])
@handle_exceptions(servicio='Clientes', cod_mensaje=1005)
def delete_cliente(codigo):
    """
    Eliminar cliente (borrado físico) por código
    ---
    tags:
      - Clientes
    parameters:
      - name: codigo
        in: path
        type: string
        required: true
        description: Código único del cliente
    responses:
      204:
        description: Eliminado
      404:
        description: No encontrado
    """
    ok = ClienteService.delete_by_codigo(codigo)
    if not ok:
        return jsonify({"error": "No encontrado"}), 404
    return '', 204