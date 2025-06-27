# backend/app/api/productos_api.py
from flask import Blueprint, jsonify, request
from app.services.productos_service import ProductoService
from app.dtos.productos_dto import ProductoSchema
from app.utils.logger import handle_exceptions
from app.utils.auth_middleware import token_required, require_permission

productos_bp = Blueprint('productos_bp', __name__)
producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)

@productos_bp.route('/', methods=['GET'])
@token_required
@require_permission('Productos', 'read')
@handle_exceptions(servicio='Productos', cod_mensaje=2001)
def get_productos(current_user):
    """
    Listar todos los productos
    ---
    tags:
      - Productos
    parameters:
      - name: nombre
        in: query
        type: string
        description: Filtrar por nombre de producto
      - name: codigo
        in: query
        type: string
        description: Filtrar por código de producto
    responses:
      200:
        description: Lista de productos
        schema:
          type: array
          items:
            $ref: '#/definitions/Producto'
    """
    nombre = request.args.get('nombre')
    codigo = request.args.get('codigo')

    if nombre or codigo:
        productos = ProductoService.search_productos(nombre=nombre, codigo=codigo)
    else:
        productos = ProductoService.get_all_productos()
    
    return jsonify(productos), 200

@productos_bp.route('/<int:id>', methods=['GET'])
@token_required
@require_permission('Productos', 'read')
@handle_exceptions(servicio='Productos', cod_mensaje=2002)
def get_producto(current_user, id):
    """
    Obtener producto por ID
    ---
    tags:
      - Productos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del producto
    responses:
      200:
        description: Producto encontrado
        schema:
          $ref: '#/definitions/Producto'
      404:
        description: Producto no encontrado
        schema:
          type: object
          properties:
            error:
              type: string
    """
    producto = ProductoService.get_producto_by_id(id)
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify(producto), 200

@productos_bp.route('/codigo/<string:codigo>', methods=['GET'])
@token_required
@require_permission('Productos', 'read')
@handle_exceptions(servicio='Productos', cod_mensaje=2002)
def get_producto_by_codigo(current_user, codigo):
    """
    Obtener producto por código
    ---
    tags:
      - Productos
    parameters:
      - name: codigo
        in: path
        type: string
        required: true
        description: Código del producto
    responses:
      200:
        description: Producto encontrado
        schema:
          $ref: '#/definitions/Producto'
      404:
        description: Producto no encontrado
        schema:
          type: object
          properties:
            error:
              type: string
    """
    producto = ProductoService.get_producto_by_codigo(codigo)
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify(producto), 200

@productos_bp.route('/', methods=['POST'])
@token_required
@require_permission('Productos', 'create')
@handle_exceptions(servicio='Productos', cod_mensaje=2003)
def create_producto(current_user):
    """
    Crear nuevo producto
    ---
    tags:
      - Productos
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - codigo_producto
            - nombre_producto
            - unidad_medida
          properties:
            codigo_producto:
              type: string
              maxLength: 50
              description: Código único del producto
            nombre_producto:
              type: string
              maxLength: 200
              description: Nombre del producto
            unidad_medida:
              type: string
              enum: ['Unidad', 'Fardo', 'Paquete']
              description: Unidad de medida del producto
            unidades_por_fardo_paquete:
              type: integer
              default: 1
              description: Cantidad de unidades por fardo o paquete
            stock_minimo:
              type: integer
              default: 0
              description: Stock mínimo del producto
            usuario_creacion:
              type: string
              maxLength: 50
              description: Usuario que crea el producto
    responses:
      201:
        description: Producto creado exitosamente
        schema:
          $ref: '#/definitions/Producto'
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
    producto, error = ProductoService.create_producto(data, usuario_creacion)
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify(producto), 201

@productos_bp.route('/<int:id>', methods=['PUT'])
@token_required
@require_permission('Productos', 'update')
@handle_exceptions(servicio='Productos', cod_mensaje=2004)
def update_producto(current_user, id):
    """
    Actualizar producto existente
    ---
    tags:
      - Productos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del producto a actualizar
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            codigo_producto:
              type: string
              maxLength: 50
              description: Código único del producto
            nombre_producto:
              type: string
              maxLength: 200
              description: Nombre del producto
            unidad_medida:
              type: string
              enum: ['Unidad', 'Fardo', 'Paquete']
              description: Unidad de medida del producto
            unidades_por_fardo_paquete:
              type: integer
              description: Cantidad de unidades por fardo o paquete
            stock_minimo:
              type: integer
              description: Stock mínimo del producto
            usuario_modificacion:
              type: string
              maxLength: 50
              description: Usuario que modifica el producto
    responses:
      200:
        description: Producto actualizado exitosamente
        schema:
          $ref: '#/definitions/Producto'
      400:
        description: Error en los datos de entrada
        schema:
          type: object
          properties:
            error:
              type: string
      404:
        description: Producto no encontrado
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
    producto, error = ProductoService.update_producto(id, data, usuario_modificacion)
    
    if error:
        if "no encontrado" in error.lower():
            return jsonify({"error": error}), 404
        return jsonify({"error": error}), 400
    
    return jsonify(producto), 200

@productos_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@require_permission('Productos', 'delete')
@handle_exceptions(servicio='Productos', cod_mensaje=2005)
def delete_producto(current_user, id):
    """
    Eliminar producto
    ---
    tags:
      - Productos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del producto a eliminar
    responses:
      200:
        description: Producto eliminado exitosamente
        schema:
          type: object
          properties:
            message:
              type: string
      404:
        description: Producto no encontrado
        schema:
          type: object
          properties:
            error:
              type: string
    """
    success, error = ProductoService.delete_producto(id)
    
    if not success:
        if "no encontrado" in error.lower():
            return jsonify({"error": error}), 404
        return jsonify({"error": error}), 400
    
    return jsonify({"message": "Producto eliminado exitosamente"}), 200

@productos_bp.route('/activos', methods=['GET'])
@token_required
@require_permission('Productos', 'read')
@handle_exceptions(servicio='Productos', cod_mensaje=2006)
def get_productos_activos(current_user):
    """
    Obtener productos activos
    ---
    tags:
      - Productos
    responses:
      200:
        description: Lista de productos activos
        schema:
          type: array
          items:
            $ref: '#/definitions/Producto'
    """
    productos = ProductoService.get_all_productos_activos()
    return jsonify(productos), 200