from flask import Blueprint, jsonify, request
from app.services.ingresos_service import IngresoMercanciaService, DetalleIngresoService
from app.dtos.ingresos_dto import (
    IngresoMercanciaSchema, CrearIngresoMercanciaSchema, 
    DetalleIngresoSchema, ConfirmarIngresoSchema
)
from app.utils.logger import handle_exceptions
from app.utils.auth_middleware import token_required, require_permission

ingresos_bp = Blueprint('ingresos_bp', __name__)

# Schemas
ingreso_schema = IngresoMercanciaSchema()
crear_ingreso_schema = CrearIngresoMercanciaSchema()
detalle_schema = DetalleIngresoSchema()
confirmar_schema = ConfirmarIngresoSchema()

# ===== ENDPOINTS DE INGRESOS DE MERCANCÍA =====

@ingresos_bp.route('/', methods=['GET'])
@token_required
@require_permission('Ingresos', 'read')
@handle_exceptions(servicio='IngresosMercancia', cod_mensaje=7001)
def get_ingresos(current_user):
    """
    Listar todos los ingresos de mercancía
    ---
    tags:
      - Ingresos de Mercancía
    parameters:
      - name: numero_contenedor
        in: query
        type: string
        description: Filtrar por número de contenedor
      - name: numero_duca
        in: query
        type: string
        description: Filtrar por número DUCA
      - name: fecha_desde
        in: query
        type: string
        format: date
        description: Fecha desde (YYYY-MM-DD)
      - name: fecha_hasta
        in: query
        type: string
        format: date
        description: Fecha hasta (YYYY-MM-DD)
    responses:
      200:
        description: Lista de ingresos de mercancía
        schema:
          type: array
          items:
            $ref: '#/definitions/IngresoMercancia'
    """
    numero_contenedor = request.args.get('numero_contenedor')
    numero_duca = request.args.get('numero_duca')
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    
    if any([numero_contenedor, numero_duca, fecha_desde, fecha_hasta]):
        ingresos = IngresoMercanciaService.search_ingresos(
            numero_contenedor=numero_contenedor,
            numero_duca=numero_duca,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta
        )
    else:
        ingresos = IngresoMercanciaService.get_all_ingresos()
    
    return jsonify(ingresos), 200

@ingresos_bp.route('/<int:ingreso_id>', methods=['GET'])
@token_required
@require_permission('Ingresos', 'read')
@handle_exceptions(servicio='IngresosMercancia', cod_mensaje=7002)
def get_ingreso_by_id(current_user, ingreso_id):
    """
    Obtener ingreso de mercancía por ID con sus detalles
    ---
    tags:
      - Ingresos de Mercancía
    parameters:
      - name: ingreso_id
        in: path
        type: integer
        required: true
        description: ID del ingreso de mercancía
    responses:
      200:
        description: Ingreso de mercancía encontrado
        schema:
          $ref: '#/definitions/IngresoMercancia'
      404:
        description: Ingreso no encontrado
    """
    ingreso = IngresoMercanciaService.get_ingreso_by_id(ingreso_id)
    if not ingreso:
        return jsonify({"error": "Ingreso de mercancía no encontrado"}), 404
    
    return jsonify(ingreso), 200

@ingresos_bp.route('/', methods=['POST'])
@token_required
@require_permission('Ingresos', 'create')
@handle_exceptions(servicio='IngresosMercancia', cod_mensaje=7003)
def create_ingreso(current_user):
    """
    Crear nuevo ingreso de mercancía con sus detalles
    ---
    tags:
      - Ingresos de Mercancía
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - fecha_ingreso
            - numero_contenedor
            - numero_duca
            - fecha_duca
            - detalles
          properties:
            fecha_ingreso:
              type: string
              format: date
              description: Fecha del ingreso
            numero_contenedor:
              type: string
              description: Número del contenedor
            numero_duca:
              type: string
              description: Número de la DUCA
            fecha_duca:
              type: string
              format: date
              description: Fecha de la DUCA
            numero_duca_rectificada:
              type: string
              description: Número de DUCA rectificada (opcional)
            fecha_duca_rectificada:
              type: string
              format: date
              description: Fecha de DUCA rectificada (opcional)
            observaciones:
              type: string
              description: Observaciones del ingreso
            usuario_creacion:
              type: string
              description: Usuario que crea el ingreso
            detalles:
              type: array
              items:
                type: object
                required:
                  - producto_id
                  - cantidad_fardos_paquetes
                  - unidades_por_fardo_paquete
                properties:
                  producto_id:
                    type: integer
                    description: ID del producto
                  cantidad_fardos_paquetes:
                    type: integer
                    description: Cantidad de fardos/paquetes
                  unidades_por_fardo_paquete:
                    type: integer
                    description: Unidades por fardo/paquete
    responses:
      201:
        description: Ingreso creado exitosamente
        schema:
          $ref: '#/definitions/IngresoMercancia'
      400:
        description: Error de validación
    """
    data = request.get_json()
    
    # Validar datos
    errors = crear_ingreso_schema.validate(data)
    if errors:
        return jsonify({"error": "Datos inválidos", "details": errors}), 400
    
    ingreso, error = IngresoMercanciaService.create_ingreso_completo(data)
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify(ingreso), 201

@ingresos_bp.route('/<int:ingreso_id>', methods=['PUT'])
@token_required
@require_permission('Ingresos', 'update')
@handle_exceptions(servicio='IngresosMercancia', cod_mensaje=7004)
def update_ingreso(current_user, ingreso_id):
    """
    Actualizar datos básicos del ingreso (sin detalles)
    ---
    tags:
      - Ingresos de Mercancía
    parameters:
      - name: ingreso_id
        in: path
        type: integer
        required: true
        description: ID del ingreso de mercancía
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
        schema:
          $ref: '#/definitions/IngresoMercancia'
      404:
        description: Ingreso no encontrado
      400:
        description: Error de validación
    """
    data = request.get_json()
    
    ingreso, error = IngresoMercanciaService.update_ingreso(ingreso_id, data)
    if error:
        return jsonify({"error": error}), 400 if "no encontrado" not in error else 404
    
    return jsonify(ingreso), 200

@ingresos_bp.route('/<int:ingreso_id>', methods=['DELETE'])
@token_required
@require_permission('Ingresos', 'delete')
@handle_exceptions(servicio='IngresosMercancia', cod_mensaje=7005)
def delete_ingreso(current_user, ingreso_id):
    """
    Eliminar ingreso de mercancía y sus detalles
    ---
    tags:
      - Ingresos de Mercancía
    parameters:
      - name: ingreso_id
        in: path
        type: integer
        required: true
        description: ID del ingreso de mercancía
    responses:
      204:
        description: Ingreso eliminado
      404:
        description: Ingreso no encontrado
    """
    success, error = IngresoMercanciaService.delete_ingreso(ingreso_id)
    if not success:
        return jsonify({"error": error}), 404 if "no encontrado" in error else 400
    
    return '', 204

@ingresos_bp.route('/<int:ingreso_id>/confirmar', methods=['POST'])
@token_required
@require_permission('Ingresos', 'update')
@handle_exceptions(servicio='IngresosMercancia', cod_mensaje=7006)
def confirmar_ingreso(current_user, ingreso_id):
    """
    Confirmar ingreso y aplicar cantidades al inventario
    ---
    tags:
      - Ingresos de Mercancía
    parameters:
      - name: ingreso_id
        in: path
        type: integer
        required: true
        description: ID del ingreso de mercancía
      - in: body
        name: body
        schema:
          type: object
          properties:
            usuario_confirmacion:
              type: string
              description: Usuario que confirma el ingreso
    responses:
      200:
        description: Ingreso confirmado y inventarios actualizados
        schema:
          type: object
          properties:
            message:
              type: string
      404:
        description: Ingreso no encontrado
      400:
        description: Error en la confirmación
    """
    data = request.get_json() or {}
    usuario_confirmacion = data.get('usuario_confirmacion', 'sistema')
    
    success, message = IngresoMercanciaService.confirmar_ingreso_a_inventario(
        ingreso_id, usuario_confirmacion
    )
    
    if not success:
        status_code = 404 if "no encontrado" in message else 400
        return jsonify({"error": message}), status_code
    
    return jsonify({"message": message}), 200

# ===== ENDPOINTS DE DETALLES =====

@ingresos_bp.route('/<int:ingreso_id>/detalles', methods=['GET'])
@token_required
@require_permission('Ingresos', 'read')
@handle_exceptions(servicio='IngresosMercancia', cod_mensaje=7007)
def get_detalles_ingreso(current_user, ingreso_id):
    """
    Obtener detalles de un ingreso específico
    ---
    tags:
      - Detalles de Ingreso
    parameters:
      - name: ingreso_id
        in: path
        type: integer
        required: true
        description: ID del ingreso de mercancía
    responses:
      200:
        description: Detalles del ingreso
        schema:
          type: array
          items:
            $ref: '#/definitions/DetalleIngreso'
    """
    detalles = DetalleIngresoService.get_detalles_by_ingreso(ingreso_id)
    return jsonify(detalles), 200

@ingresos_bp.route('/<int:ingreso_id>/detalles', methods=['POST'])
@token_required
@require_permission('Ingresos', 'create')
@handle_exceptions(servicio='IngresosMercancia', cod_mensaje=7008)
def add_detalle_to_ingreso(current_user, ingreso_id):
    """
    Agregar detalle a un ingreso existente
    ---
    tags:
      - Detalles de Ingreso
    parameters:
      - name: ingreso_id
        in: path
        type: integer
        required: true
        description: ID del ingreso de mercancía
      - in: body
        name: body
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
            usuario_creacion:
              type: string
    responses:
      201:
        description: Detalle agregado
        schema:
          $ref: '#/definitions/DetalleIngreso'
      400:
        description: Error de validación
    """
    data = request.get_json()
    
    errors = detalle_schema.validate(data, partial=True)
    if errors:
        return jsonify({"error": "Datos inválidos", "details": errors}), 400
    
    detalle, error = DetalleIngresoService.add_detalle_to_ingreso(ingreso_id, data)
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify(detalle), 201

@ingresos_bp.route('/<int:ingreso_id>/totales', methods=['GET'])
@token_required
@require_permission('Ingresos', 'read')
@handle_exceptions(servicio='IngresosMercancia', cod_mensaje=7009)
def get_totales_ingreso(current_user, ingreso_id):
    """
    Obtener totales calculados del ingreso
    ---
    tags:
      - Ingresos de Mercancía
    parameters:
      - name: ingreso_id
        in: path
        type: integer
        required: true
        description: ID del ingreso de mercancía
    responses:
      200:
        description: Totales del ingreso
        schema:
          type: object
          properties:
            total_productos_diferentes:
              type: integer
            total_fardos_paquetes:
              type: integer
            total_unidades:
              type: integer
            detalles:
              type: array
              items:
                $ref: '#/definitions/DetalleIngreso'
    """
    totales = DetalleIngresoService.calculate_totales_ingreso(ingreso_id)
    return jsonify(totales), 200

@ingresos_bp.route('/detalles/<int:detalle_id>', methods=['PUT'])
@token_required
@require_permission('Ingresos', 'update')
@handle_exceptions(servicio='IngresosMercancia', cod_mensaje=7010)
def update_detalle(current_user, detalle_id):
    """
    Actualizar un detalle específico
    ---
    tags:
      - Detalles de Ingreso
    parameters:
      - name: detalle_id
        in: path
        type: integer
        required: true
        description: ID del detalle
      - in: body
        name: body
        schema:
          type: object
          properties:
            cantidad_fardos_paquetes:
              type: integer
            unidades_por_fardo_paquete:
              type: integer
    responses:
      200:
        description: Detalle actualizado
        schema:
          $ref: '#/definitions/DetalleIngreso'
      404:
        description: Detalle no encontrado
    """
    data = request.get_json()
    
    detalle, error = DetalleIngresoService.update_detalle(detalle_id, data)
    if error:
        return jsonify({"error": error}), 404 if "no encontrado" in error else 400
    
    return jsonify(detalle), 200

@ingresos_bp.route('/detalles/<int:detalle_id>', methods=['DELETE'])
@token_required
@require_permission('Ingresos', 'delete')
@handle_exceptions(servicio='IngresosMercancia', cod_mensaje=7011)
def delete_detalle(current_user, detalle_id):
    """
    Eliminar un detalle específico
    ---
    tags:
      - Detalles de Ingreso
    parameters:
      - name: detalle_id
        in: path
        type: integer
        required: true
        description: ID del detalle
    responses:
      204:
        description: Detalle eliminado
      404:
        description: Detalle no encontrado
    """
    success, error = DetalleIngresoService.delete_detalle(detalle_id)
    if not success:
        return jsonify({"error": error}), 404 if "no encontrado" in error else 400
    
    return '', 204