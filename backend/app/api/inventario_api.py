# backend/app/api/inventario_api.py
from flask import Blueprint, jsonify, request
from app.services.inventario_service import InventarioService, IngresoMercanciaService
from app.utils.logger import handle_exceptions

inventario_bp = Blueprint('inventario_bp', __name__)

# INVENTARIO ENDPOINTS
@inventario_bp.route('/', methods=['GET'])
@handle_exceptions(servicio='Inventario', cod_mensaje=3001)
def get_inventarios():
    """
    Listar inventarios
    ---
    tags:
      - Inventario
    responses:
      200:
        description: Lista de inventarios
        schema:
          type: array
          items:
            $ref: '#/definitions/Inventario'
    """
    inventarios = InventarioService.get_all_inventario()
    return jsonify(inventarios), 200

@inventario_bp.route('/<int:id>', methods=['GET'])
@handle_exceptions(servicio='Inventario', cod_mensaje=3002)
def get_inventario(id):
    """
    Obtener inventario por ID
    ---
    tags:
      - Inventario
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del inventario
    responses:
      200:
        description: Inventario encontrado
        schema:
          $ref: '#/definitions/Inventario'
      404:
        description: Inventario no encontrado
    """
    inventario = InventarioService.get_inventario_by_id(id)
    if not inventario:
        return jsonify({"error": "Inventario no encontrado"}), 404
    return jsonify(inventario), 200

@inventario_bp.route('/producto/<int:producto_id>', methods=['GET'])
@handle_exceptions(servicio='Inventario', cod_mensaje=3002)
def get_inventario_by_producto(producto_id):
    """
    Obtener inventario por ID de producto
    ---
    tags:
      - Inventario
    parameters:
      - name: producto_id
        in: path
        type: integer
        required: true
        description: ID del producto
    responses:
      200:
        description: Inventario encontrado
        schema:
          $ref: '#/definitions/Inventario'
      404:
        description: Inventario no encontrado
    """
    inventario = InventarioService.get_inventario_by_producto_id(producto_id)
    if not inventario:
        return jsonify({"error": "Inventario no encontrado"}), 404
    return jsonify(inventario), 200

@inventario_bp.route('/', methods=['POST'])
@handle_exceptions(servicio='Inventario', cod_mensaje=3003)
def create_inventario():
    """
    Crear inventario
    ---
    tags:
      - Inventario
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - producto_id
          properties:
            producto_id:
              type: integer
              description: ID del producto
            stock_disponible:
              type: integer
              default: 0
              description: Stock disponible
            stock_apartado:
              type: integer
              default: 0
              description: Stock apartado
    responses:
      201:
        description: Inventario creado
        schema:
          $ref: '#/definitions/Inventario'
      400:
        description: Error en los datos
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400
    
    usuario_creacion = request.headers.get('X-Usuario', 'sistema')
    inventario, error = InventarioService.create_inventario(data, usuario_creacion)
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify(inventario), 201

@inventario_bp.route('/<int:id>', methods=['PUT'])
@handle_exceptions(servicio='Inventario', cod_mensaje=3004)
def update_inventario(id):
    """
    Actualizar inventario
    ---
    tags:
      - Inventario
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del inventario
      - in: body
        name: body
        schema:
          type: object
          properties:
            stock_disponible:
              type: integer
            stock_apartado:
              type: integer
    responses:
      200:
        description: Inventario actualizado
        schema:
          $ref: '#/definitions/Inventario'
      400:
        description: Error en los datos
      404:
        description: Inventario no encontrado
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400
    
    usuario_modificacion = request.headers.get('X-Usuario', 'sistema')
    inventario, error = InventarioService.update_inventario(id, data, usuario_modificacion)
    
    if error:
        if "no encontrado" in error.lower():
            return jsonify({"error": error}), 404
        return jsonify({"error": error}), 400
    
    return jsonify(inventario), 200

@inventario_bp.route('/<int:id>', methods=['DELETE'])
@handle_exceptions(servicio='Inventario', cod_mensaje=3005)
def delete_inventario(id):
    """
    Eliminar inventario
    ---
    tags:
      - Inventario
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del inventario
    responses:
      200:
        description: Inventario eliminado
      404:
        description: Inventario no encontrado
    """
    success, error = InventarioService.delete_inventario(id)
    
    if not success:
        if "no encontrado" in error.lower():
            return jsonify({"error": error}), 404
        return jsonify({"error": error}), 400
    
    return jsonify({"message": "Inventario eliminado exitosamente"}), 200

@inventario_bp.route('/stock-bajo-minimo', methods=['GET'])
@handle_exceptions(servicio='Inventario', cod_mensaje=3006)
def get_stock_bajo_minimo():
    """
    Obtener productos con stock bajo mínimo
    ---
    tags:
      - Inventario
    responses:
      200:
        description: Lista de productos con stock bajo mínimo
        schema:
          type: array
          items:
            $ref: '#/definitions/Inventario'
    """
    inventarios = InventarioService.get_stock_bajo_minimo()
    return jsonify(inventarios), 200

# MOVIMIENTOS DE INVENTARIO ENDPOINTS
@inventario_bp.route('/movimientos', methods=['GET'])
@handle_exceptions(servicio='Inventario', cod_mensaje=3007)
def get_movimientos():
    """
    Listar movimientos de inventario
    ---
    tags:
      - Inventario
    parameters:
      - name: producto_id
        in: query
        type: integer
        description: Filtrar por ID de producto
      - name: tipo_movimiento
        in: query
        type: string
        enum: ['Ingreso', 'Salida', 'Ajuste', 'Apartado', 'Liberado']
        description: Filtrar por tipo de movimiento
      - name: fecha_inicio
        in: query
        type: string
        format: date-time
        description: Fecha inicio del rango
      - name: fecha_fin
        in: query
        type: string
        format: date-time
        description: Fecha fin del rango
    responses:
      200:
        description: Lista de movimientos
        schema:
          type: array
          items:
            $ref: '#/definitions/MovimientoInventario'
    """
    producto_id = request.args.get('producto_id')
    tipo_movimiento = request.args.get('tipo_movimiento')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    
    if producto_id:
        movimientos = InventarioService.get_movimientos_by_producto(int(producto_id))
    elif tipo_movimiento:
        movimientos = InventarioService.get_movimientos_by_tipo(tipo_movimiento)
    elif fecha_inicio and fecha_fin:
        movimientos = InventarioService.get_movimientos_by_fecha_rango(fecha_inicio, fecha_fin)
    else:
        movimientos = InventarioService.get_all_movimientos()
    
    if movimientos is None:
        return jsonify({"error": "Error en el formato de fechas"}), 400
    
    return jsonify(movimientos), 200

@inventario_bp.route('/movimientos', methods=['POST'])
@handle_exceptions(servicio='Inventario', cod_mensaje=3008)
def create_movimiento():
    """
    Registrar movimiento de inventario
    ---
    tags:
      - Inventario
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - producto_id
            - tipo_movimiento
            - cantidad
          properties:
            producto_id:
              type: integer
              description: ID del producto
            tipo_movimiento:
              type: string
              enum: ['Ingreso', 'Salida', 'Ajuste', 'Apartado', 'Liberado']
              description: Tipo de movimiento
            cantidad:
              type: integer
              description: Cantidad del movimiento
            referencia:
              type: string
              description: Referencia del movimiento
            motivo:
              type: string
              description: Motivo del movimiento
    responses:
      201:
        description: Movimiento registrado
        schema:
          $ref: '#/definitions/MovimientoInventario'
      400:
        description: Error en los datos
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400
    
    required_fields = ['producto_id', 'tipo_movimiento', 'cantidad']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Campo requerido: {field}"}), 400
    
    usuario = request.headers.get('X-Usuario', 'sistema')
    
    movimiento, error = InventarioService.registrar_movimiento_inventario(
        data['producto_id'],
        data['tipo_movimiento'],
        data['cantidad'],
        data.get('referencia'),
        data.get('motivo'),
        usuario
    )
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify(movimiento), 201

# INGRESOS DE MERCANCIA ENDPOINTS
@inventario_bp.route('/ingresos', methods=['GET'])
@handle_exceptions(servicio='Inventario', cod_mensaje=3009)
def get_ingresos():
    """
    Listar ingresos de mercancía
    ---
    tags:
      - Inventario
    responses:
      200:
        description: Lista de ingresos
        schema:
          type: array
          items:
            $ref: '#/definitions/IngresoMercancia'
    """
    ingresos = IngresoMercanciaService.get_all_ingresos()
    return jsonify(ingresos), 200

@inventario_bp.route('/ingresos/<int:id>', methods=['GET'])
@handle_exceptions(servicio='Inventario', cod_mensaje=3010)
def get_ingreso(id):
    """
    Obtener ingreso de mercancía por ID
    ---
    tags:
      - Inventario
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del ingreso
    responses:
      200:
        description: Ingreso encontrado
        schema:
          $ref: '#/definitions/IngresoMercancia'
      404:
        description: Ingreso no encontrado
    """
    ingreso = IngresoMercanciaService.get_ingreso_by_id(id)
    if not ingreso:
        return jsonify({"error": "Ingreso no encontrado"}), 404
    return jsonify(ingreso), 200

@inventario_bp.route('/ingresos', methods=['POST'])
@handle_exceptions(servicio='Inventario', cod_mensaje=3011)
def create_ingreso():
    """
    Crear ingreso de mercancía
    ---
    tags:
      - Inventario
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - fecha_ingreso
            - numero_contenedor
            - numero_duca
            - fecha_duca
          properties:
            fecha_ingreso:
              type: string
              format: date
            numero_contenedor:
              type: string
            numero_duca:
              type: string
            fecha_duca:
              type: string
              format: date
            numero_duca_rectificada:
              type: string
            fecha_duca_rectificada:
              type: string
              format: date
            observaciones:
              type: string
    responses:
      201:
        description: Ingreso creado
        schema:
          $ref: '#/definitions/IngresoMercancia'
      400:
        description: Error en los datos
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400
    
    usuario_creacion = request.headers.get('X-Usuario', 'sistema')
    ingreso, error = IngresoMercanciaService.create_ingreso(data, usuario_creacion)
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify(ingreso), 201

@inventario_bp.route('/ingresos/<int:id>', methods=['PUT'])
@handle_exceptions(servicio='Inventario', cod_mensaje=3012)
def update_ingreso(id):
    """
    Actualizar ingreso de mercancía
    ---
    tags:
      - Inventario
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          properties:
            fecha_ingreso:
              type: string
              format: date
            numero_contenedor:
              type: string
            numero_duca:
              type: string
            fecha_duca:
              type: string
              format: date
            numero_duca_rectificada:
              type: string
            fecha_duca_rectificada:
              type: string
              format: date
            observaciones:
              type: string
    responses:
      200:
        description: Ingreso actualizado
      400:
        description: Error en los datos
      404:
        description: Ingreso no encontrado
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400
    
    ingreso, error = IngresoMercanciaService.update_ingreso(id, data)
    
    if error:
        if "no encontrado" in error.lower():
            return jsonify({"error": error}), 404
        return jsonify({"error": error}), 400
    
    return jsonify(ingreso), 200

@inventario_bp.route('/ingresos/<int:id>', methods=['DELETE'])
@handle_exceptions(servicio='Inventario', cod_mensaje=3013)
def delete_ingreso(id):
    """
    Eliminar ingreso de mercancía
    ---
    tags:
      - Inventario
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Ingreso eliminado
      404:
        description: Ingreso no encontrado
    """
    success, error = IngresoMercanciaService.delete_ingreso(id)
    
    if not success:
        if "no encontrado" in error.lower():
            return jsonify({"error": error}), 404
        return jsonify({"error": error}), 400
    
    return jsonify({"message": "Ingreso eliminado exitosamente"}), 200

@inventario_bp.route('/ingresos/<int:ingreso_id>/detalles', methods=['POST'])
@handle_exceptions(servicio='Inventario', cod_mensaje=3014)
def add_detalle_ingreso(ingreso_id):
    """
    Agregar detalle a ingreso de mercancía
    ---
    tags:
      - Inventario
    parameters:
      - name: ingreso_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - producto_id
            - cantidad_fardos_paquetes
            - unidades_por_fardo_paquete
          properties:
            producto_id:
              type: integer
            cantidad_fardos_paquetes:
              type: integer
            unidades_por_fardo_paquete:
              type: integer
    responses:
      201:
        description: Detalle agregado
      400:
        description: Error en los datos
      404:
        description: Ingreso no encontrado
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400
    
    usuario_creacion = request.headers.get('X-Usuario', 'sistema')
    detalle, error = IngresoMercanciaService.add_detalle_ingreso(ingreso_id, data, usuario_creacion)
    
    if error:
        if "no encontrado" in error.lower():
            return jsonify({"error": error}), 404
        return jsonify({"error": error}), 400
    
    return jsonify(detalle), 201