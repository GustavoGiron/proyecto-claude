from flask import Blueprint, jsonify, request
from app.services.vendedores_service import VendedorService
from app.dtos.vendedores_dto import VendedorSchema
from app.utils.logger import handle_exceptions
from app.utils.auth_middleware import token_required, require_permission

vendedores_bp = Blueprint('vendedores_bp', __name__)
vendedor_schema = VendedorSchema()
vendedores_schema = VendedorSchema(many=True)

@vendedores_bp.route('/', methods=['GET'])
@token_required
@require_permission('Vendedores', 'read')
@handle_exceptions(servicio='Vendedores', cod_mensaje=5001)
def get_vendedores(current_user):
    """
    Listar todos los vendedores
    ---
    tags:
      - Vendedores
    parameters:
      - name: nombres
        in: query
        type: string
        description: Filtrar por nombres del vendedor
      - name: apellidos
        in: query
        type: string
        description: Filtrar por apellidos del vendedor
      - name: codigo
        in: query
        type: string
        description: Filtrar por código del vendedor
    responses:
      200:
        description: Lista de vendedores
        schema:
          type: array
          items:
            $ref: '#/definitions/Vendedor'
    """
    nombres = request.args.get('nombres')
    apellidos = request.args.get('apellidos') 
    codigo = request.args.get('codigo')

    if nombres or apellidos or codigo:
        vendedores = VendedorService.search_vendedores(nombres=nombres, apellidos=apellidos, codigo=codigo)
    else:
        vendedores = VendedorService.get_all_vendedores()
    
    return jsonify(vendedores), 200

@vendedores_bp.route('/<int:id>', methods=['GET'])
@token_required
@require_permission('Vendedores', 'read')
@handle_exceptions(servicio='Vendedores', cod_mensaje=5002)
def get_vendedor(current_user, id):
    """
    Obtener vendedor por ID
    ---
    tags:
      - Vendedores
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del vendedor
    responses:
      200:
        description: Vendedor encontrado
        schema:
          $ref: '#/definitions/Vendedor'
      404:
        description: Vendedor no encontrado
        schema:
          type: object
          properties:
            error:
              type: string
    """
    vendedor = VendedorService.get_vendedor_by_id(id)
    if not vendedor:
        return jsonify({"error": "Vendedor no encontrado"}), 404
    return jsonify(vendedor), 200

@vendedores_bp.route('/codigo/<string:codigo>', methods=['GET'])
@token_required
@require_permission('Vendedores', 'read')
@handle_exceptions(servicio='Vendedores', cod_mensaje=5002)
def get_vendedor_by_codigo(current_user, codigo):
    """
    Obtener vendedor por código
    ---
    tags:
      - Vendedores
    parameters:
      - name: codigo
        in: path
        type: string
        required: true
        description: Código del vendedor
    responses:
      200:
        description: Vendedor encontrado
        schema:
          $ref: '#/definitions/Vendedor'
      404:
        description: Vendedor no encontrado
        schema:
          type: object
          properties:
            error:
              type: string
    """
    vendedor = VendedorService.get_vendedor_by_codigo(codigo)
    if not vendedor:
        return jsonify({"error": "Vendedor no encontrado"}), 404
    return jsonify(vendedor), 200

@vendedores_bp.route('/', methods=['POST'])
@token_required
@require_permission('Vendedores', 'create')
@handle_exceptions(servicio='Vendedores', cod_mensaje=5003)
def create_vendedor(current_user):
    """
    Crear nuevo vendedor
    ---
    tags:
      - Vendedores
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - nombres
            - apellidos
            - porcentaje_comision
          properties:
            nombres:
              type: string
              maxLength: 100
              description: Nombres del vendedor
            apellidos:
              type: string
              maxLength: 100
              description: Apellidos del vendedor
            telefono:
              type: string
              maxLength: 20
              description: Teléfono del vendedor (formato 0000-0000)
            direccion:
              type: string
              description: Dirección del vendedor
            porcentaje_comision:
              type: number
              minimum: 0
              maximum: 100
              description: Porcentaje de comisión (0-100)
            usuario_creacion:
              type: string
              maxLength: 50
              description: Usuario que crea el vendedor
    responses:
      201:
        description: Vendedor creado exitosamente
        schema:
          $ref: '#/definitions/Vendedor'
      400:
        description: Error en los datos de entrada
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400
    
    usuario_creacion = current_user.username
    vendedor, error = VendedorService.create_vendedor(data, usuario_creacion)
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify(vendedor), 201

@vendedores_bp.route('/<int:id>', methods=['PUT'])
@token_required
@require_permission('Vendedores', 'update')
@handle_exceptions(servicio='Vendedores', cod_mensaje=5004)
def update_vendedor(current_user, id):
    """
    Actualizar vendedor existente
    ---
    tags:
      - Vendedores
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del vendedor a actualizar
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nombres:
              type: string
              maxLength: 100
              description: Nombres del vendedor
            apellidos:
              type: string
              maxLength: 100
              description: Apellidos del vendedor
            telefono:
              type: string
              maxLength: 20
              description: Teléfono del vendedor
            direccion:
              type: string
              description: Dirección del vendedor
            porcentaje_comision:
              type: number
              minimum: 0
              maximum: 100
              description: Porcentaje de comisión (0-100)
            usuario_modificacion:
              type: string
              maxLength: 50
              description: Usuario que modifica el vendedor
    responses:
      200:
        description: Vendedor actualizado exitosamente
        schema:
          $ref: '#/definitions/Vendedor'
      400:
        description: Error en los datos de entrada
        schema:
          type: object
          properties:
            error:
              type: string
      404:
        description: Vendedor no encontrado
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400
    
    usuario_modificacion = current_user.username
    vendedor, error = VendedorService.update_vendedor(id, data, usuario_modificacion)
    
    if error:
        if "no encontrado" in error.lower():
            return jsonify({"error": error}), 404
        return jsonify({"error": error}), 400
    
    return jsonify(vendedor), 200

@vendedores_bp.route('/codigo/<string:codigo>', methods=['PUT'])
@token_required
@require_permission('Vendedores', 'update')
@handle_exceptions(servicio='Vendedores', cod_mensaje=5004)
def update_vendedor_by_codigo(current_user, codigo):
    """
    Actualizar vendedor por código
    ---
    tags:
      - Vendedores
    parameters:
      - name: codigo
        in: path
        type: string
        required: true
        description: Código del vendedor a actualizar
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nombres:
              type: string
              maxLength: 100
            apellidos:
              type: string
              maxLength: 100
            telefono:
              type: string
              maxLength: 20
            direccion:
              type: string
            porcentaje_comision:
              type: number
              minimum: 0
              maximum: 100
    responses:
      200:
        description: Vendedor actualizado exitosamente
        schema:
          $ref: '#/definitions/Vendedor'
      400:
        description: Error en los datos de entrada
      404:
        description: Vendedor no encontrado
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400
    
    usuario_modificacion = current_user.username
    vendedor, error = VendedorService.update_vendedor_by_codigo(codigo, data, usuario_modificacion)
    
    if error:
        if "no encontrado" in error.lower():
            return jsonify({"error": error}), 404
        return jsonify({"error": error}), 400
    
    return jsonify(vendedor), 200

@vendedores_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@require_permission('Vendedores', 'delete')
@handle_exceptions(servicio='Vendedores', cod_mensaje=5005)
def delete_vendedor(current_user, id):
    """
    Eliminar vendedor
    ---
    tags:
      - Vendedores
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del vendedor a eliminar
    responses:
      200:
        description: Vendedor eliminado exitosamente
        schema:
          type: object
          properties:
            message:
              type: string
      404:
        description: Vendedor no encontrado
        schema:
          type: object
          properties:
            error:
              type: string
    """
    success, error = VendedorService.delete_vendedor(id)
    
    if not success:
        if "no encontrado" in error.lower():
            return jsonify({"error": error}), 404
        return jsonify({"error": error}), 400
    
    return jsonify({"message": "Vendedor eliminado exitosamente"}), 200

@vendedores_bp.route('/codigo/<string:codigo>', methods=['DELETE'])
@token_required
@require_permission('Vendedores', 'delete')
@handle_exceptions(servicio='Vendedores', cod_mensaje=5005)
def delete_vendedor_by_codigo(current_user, codigo):
    """
    Eliminar vendedor por código
    ---
    tags:
      - Vendedores
    parameters:
      - name: codigo
        in: path
        type: string
        required: true
        description: Código del vendedor a eliminar
    responses:
      200:
        description: Vendedor eliminado exitosamente
        schema:
          type: object
          properties:
            message:
              type: string
      404:
        description: Vendedor no encontrado
        schema:
          type: object
          properties:
            error:
              type: string
    """
    success, error = VendedorService.delete_vendedor_by_codigo(codigo)
    
    if not success:
        if "no encontrado" in error.lower():
            return jsonify({"error": error}), 404
        return jsonify({"error": error}), 400
    
    return jsonify({"message": "Vendedor eliminado exitosamente"}), 200