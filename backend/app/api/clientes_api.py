from flask import Blueprint, jsonify, request
from app.services.clientes_service import ClienteService
from app.dtos.clientes_dto import ClienteSchema
from app.utils.validators import validate_telefono
from app.utils.logger import handle_exceptions
from app.utils.auth_middleware import token_required, require_permission

clientes_bp = Blueprint('clientes_bp', __name__)
schema      = ClienteSchema()
many_schema = ClienteSchema(many=True)

@clientes_bp.route('/', methods=['GET'])
@token_required
@require_permission('Clientes', 'read')
@handle_exceptions(servicio='Clientes', cod_mensaje=1001)
def list_clientes(current_user):
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

@clientes_bp.route('/buscar/nombre/<string:nombre_contacto>', methods=['GET'])
@handle_exceptions(servicio='Clientes', cod_mensaje=1002)
def buscar_por_nombre_contacto(nombre_contacto):
    """
    Buscar clientes por nombre de contacto
    ---
    tags:
      - Clientes
    parameters:
      - name: nombre_contacto
        in: path
        type: string
        required: true
        description: Nombre de contacto a buscar (búsqueda parcial)
    responses:
      200:
        description: Lista de clientes encontrados
        schema:
          type: array
          items:
            $ref: '#/definitions/Cliente'
      404:
        description: No se encontraron clientes
    """
    clientes = ClienteService.get_by_nombre_contacto(nombre_contacto)
    if not clientes:
        return jsonify({"mensaje": "No se encontraron clientes con ese nombre de contacto"}), 404
    return many_schema.jsonify(clientes), 200

@clientes_bp.route('/<int:id>', methods=['GET'])
@handle_exceptions(servicio='Clientes', cod_mensaje=1002)
def get_cliente_by_id(id):
    """
    Obtener cliente por ID
    ---
    tags:
      - Clientes
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID único del cliente
    responses:
      200:
        schema:
          $ref: '#/definitions/Cliente'
      404:
        description: No encontrado
    """
    cli = ClienteService.get_by_id(id)
    if not cli:
        return jsonify({"error": "Cliente no encontrado"}), 404
    return schema.jsonify(cli), 200

@clientes_bp.route('/<string:codigo>', methods=['GET'])
@token_required
@require_permission('Clientes', 'read')
@handle_exceptions(servicio='Clientes', cod_mensaje=1002)
def get_cliente(current_user, codigo):
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
@token_required
@require_permission('Clientes', 'create')
@handle_exceptions(servicio='Clientes', cod_mensaje=1003)
def create_cliente(current_user):
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
@token_required
@require_permission('Clientes', 'update')
@handle_exceptions(servicio='Clientes', cod_mensaje=1004)
def update_cliente(current_user, codigo):
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
@token_required
@require_permission('Clientes', 'delete')
@handle_exceptions(servicio='Clientes', cod_mensaje=1005)
def delete_cliente(current_user, codigo):
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