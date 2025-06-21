from flask import Blueprint, jsonify, request
from app.services.ventas_service import VentaService, ComisionService
from app.dtos.ventas_dto import (
    VentaSchema, CrearVentaSchema, RegistrarSalidaSchema, 
    RegistrarPagoSchema, PagoSchema, ComisionSchema
)
from app.utils.logger import handle_exceptions

ventas_bp = Blueprint('ventas_bp', __name__)

# ENDPOINTS DE VENTAS

@ventas_bp.route('/', methods=['GET'])
@handle_exceptions(servicio='Ventas', cod_mensaje=6001)
def get_ventas():
    """
    Listar todas las ventas
    ---
    tags:
      - Ventas
    parameters:
      - name: numero_envio
        in: query
        type: string
        description: Filtrar por número de envío
      - name: cliente_nombre
        in: query
        type: string
        description: Filtrar por nombre de cliente
      - name: estado_venta
        in: query
        type: string
        enum: ['Vigente', 'Anulada']
        description: Filtrar por estado de venta
      - name: estado_cobro
        in: query
        type: string
        enum: ['Pendiente', 'Parcial', 'Pagada', 'Morosa']
        description: Filtrar por estado de cobro
    responses:
      200:
        description: Lista de ventas
        schema:
          type: array
          items:
            $ref: '#/definitions/Venta'
    """
    numero_envio = request.args.get('numero_envio')
    cliente_nombre = request.args.get('cliente_nombre')
    estado_venta = request.args.get('estado_venta')
    estado_cobro = request.args.get('estado_cobro')
    
    if any([numero_envio, cliente_nombre, estado_venta, estado_cobro]):
        ventas = VentaService.search_ventas(
            numero_envio=numero_envio,
            cliente_nombre=cliente_nombre,
            estado_venta=estado_venta,
            estado_cobro=estado_cobro
        )
    else:
        ventas = VentaService.get_all_ventas()
    
    return jsonify(ventas), 200

@ventas_bp.route('/<int:id>', methods=['GET'])
@handle_exceptions(servicio='Ventas', cod_mensaje=6002)
def get_venta(id):
    """
    Obtener venta por ID
    ---
    tags:
      - Ventas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID de la venta
    responses:
      200:
        description: Venta encontrada
        schema:
          $ref: '#/definitions/Venta'
      404:
        description: Venta no encontrada
    """
    venta = VentaService.get_venta_by_id(id)
    if not venta:
        return jsonify({"error": "Venta no encontrada"}), 404
    return jsonify(venta), 200

@ventas_bp.route('/numero-envio/<string:numero_envio>', methods=['GET'])
@handle_exceptions(servicio='Ventas', cod_mensaje=6002)
def get_venta_by_numero_envio(numero_envio):
    """
    Obtener venta por número de envío
    ---
    tags:
      - Ventas
    parameters:
      - name: numero_envio
        in: path
        type: string
        required: true
        description: Número de envío de la venta
    responses:
      200:
        description: Venta encontrada
        schema:
          $ref: '#/definitions/Venta'
      404:
        description: Venta no encontrada
    """
    venta = VentaService.get_venta_by_numero_envio(numero_envio)
    if not venta:
        return jsonify({"error": "Venta no encontrada"}), 404
    return jsonify(venta), 200

@ventas_bp.route('/', methods=['POST'])
@handle_exceptions(servicio='Ventas', cod_mensaje=6003)
def create_venta():
    """
    Crear nueva venta
    ---
    tags:
      - Ventas
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - cliente_id
            - vendedor_id
            - tipo_pago
            - detalles
          properties:
            fecha_venta:
              type: string
              format: date
              description: Fecha de la venta (por defecto hoy)
            cliente_id:
              type: integer
              description: ID del cliente
            vendedor_id:
              type: integer
              description: ID del vendedor
            tipo_pago:
              type: string
              enum: ['Contado', 'Credito']
              description: Tipo de pago
            dias_credito:
              type: integer
              description: Días de crédito (0 para contado)
            numero_factura_dte:
              type: string
              description: Número de factura DTE
            nombre_factura:
              type: string
              description: Nombre para la factura
            nit_cliente:
              type: string
              description: NIT del cliente
            nit_factura:
              type: string
              description: NIT para la factura
            detalles:
              type: array
              items:
                type: object
                required:
                  - producto_id
                  - cantidad
                  - precio_por_fardo_paquete
                properties:
                  producto_id:
                    type: integer
                  cantidad:
                    type: integer
                  precio_por_fardo_paquete:
                    type: number
                  observaciones:
                    type: string
    responses:
      201:
        description: Venta creada exitosamente
        schema:
          $ref: '#/definitions/Venta'
      400:
        description: Error en los datos
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400
    
    # Validar datos
    crear_venta_schema = CrearVentaSchema()
    errors = crear_venta_schema.validate(data)
    if errors:
        return jsonify({"error": "Datos inválidos", "details": errors}), 400
    
    usuario_creacion = request.headers.get('X-Usuario', 'sistema')
    venta, error = VentaService.create_venta(data, usuario_creacion)
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify(venta), 201

@ventas_bp.route('/<int:id>/anular', methods=['PUT'])
@handle_exceptions(servicio='Ventas', cod_mensaje=6004)
def anular_venta(id):
    """
    Anular una venta
    ---
    tags:
      - Ventas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID de la venta a anular
    responses:
      200:
        description: Venta anulada exitosamente
        schema:
          $ref: '#/definitions/Venta'
      400:
        description: Error al anular la venta
      404:
        description: Venta no encontrada
    """
    usuario_modificacion = request.headers.get('X-Usuario', 'sistema')
    venta, error = VentaService.anular_venta(id, usuario_modificacion)
    
    if error:
        if "no encontrada" in error.lower():
            return jsonify({"error": error}), 404
        return jsonify({"error": error}), 400
    
    return jsonify(venta), 200

# ENDPOINTS DE SALIDA DE BODEGA

@ventas_bp.route('/<int:id>/salida-bodega', methods=['PUT'])
@handle_exceptions(servicio='Ventas', cod_mensaje=6005)
def registrar_salida_bodega(id):
    """
    Registrar salida de bodega para una venta
    ---
    tags:
      - Ventas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID de la venta
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            fecha_salida_bodega:
              type: string
              format: date
              description: Fecha de salida de bodega (por defecto hoy)
    responses:
      200:
        description: Salida registrada exitosamente
        schema:
          $ref: '#/definitions/Venta'
      400:
        description: Error al registrar salida
      404:
        description: Venta no encontrada
    """
    data = request.get_json() or {}
    
    # Validar datos
    registrar_salida_schema = RegistrarSalidaSchema()
    errors = registrar_salida_schema.validate(data)
    if errors:
        return jsonify({"error": "Datos inválidos", "details": errors}), 400
    
    usuario_modificacion = request.headers.get('X-Usuario', 'sistema')
    fecha_salida = data.get('fecha_salida_bodega')
    
    venta, error = VentaService.registrar_salida_bodega(id, fecha_salida, usuario_modificacion)
    
    if error:
        if "no encontrada" in error.lower():
            return jsonify({"error": error}), 404
        return jsonify({"error": error}), 400
    
    return jsonify(venta), 200

# ENDPOINTS DE PAGOS

@ventas_bp.route('/<int:id>/pagos', methods=['POST'])
@handle_exceptions(servicio='Ventas', cod_mensaje=6006)
def registrar_pago(id):
    """
    Registrar pago para una venta
    ---
    tags:
      - Ventas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID de la venta
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - numero_recibo_caja
            - banco
            - numero_cuenta
            - monto_abono
          properties:
            numero_recibo_caja:
              type: string
              description: Número de recibo de caja
            fecha_pago:
              type: string
              format: date
              description: Fecha del pago (por defecto hoy)
            banco:
              type: string
              enum: ['Industrial', 'Banrural', 'G&T', 'BAM']
              description: Banco del pago
            numero_cuenta:
              type: string
              description: Número de cuenta
            numero_transferencia:
              type: string
              description: Número de transferencia o depósito
            monto_abono:
              type: number
              description: Monto del abono
    responses:
      201:
        description: Pago registrado exitosamente
        schema:
          $ref: '#/definitions/Pago'
      400:
        description: Error al registrar pago
      404:
        description: Venta no encontrada
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400
    
    # Validar datos
    registrar_pago_schema = RegistrarPagoSchema()
    errors = registrar_pago_schema.validate(data)
    if errors:
        return jsonify({"error": "Datos inválidos", "details": errors}), 400
    
    usuario_creacion = request.headers.get('X-Usuario', 'sistema')
    pago, error = VentaService.registrar_pago(id, data, usuario_creacion)
    
    if error:
        if "no encontrada" in error.lower():
            return jsonify({"error": error}), 404
        return jsonify({"error": error}), 400
    
    return jsonify(pago), 201

# ENDPOINTS DE REPORTES Y CONSULTAS

@ventas_bp.route('/pendientes-cobro', methods=['GET'])
@handle_exceptions(servicio='Ventas', cod_mensaje=6007)
def get_ventas_pendientes_cobro():
    """
    Obtener ventas pendientes de cobro
    ---
    tags:
      - Ventas
    responses:
      200:
        description: Lista de ventas pendientes de cobro
        schema:
          type: array
          items:
            $ref: '#/definitions/Venta'
    """
    ventas = VentaService.get_ventas_pendientes_cobro()
    return jsonify(ventas), 200

@ventas_bp.route('/pendientes-entrega', methods=['GET'])
@handle_exceptions(servicio='Ventas', cod_mensaje=6008)
def get_ventas_pendientes_entrega():
    """
    Obtener ventas pendientes de entrega
    ---
    tags:
      - Ventas
    responses:
      200:
        description: Lista de ventas pendientes de entrega
        schema:
          type: array
          items:
            $ref: '#/definitions/Venta'
    """
    ventas = VentaService.get_ventas_pendientes_entrega()
    return jsonify(ventas), 200

# ENDPOINTS DE COMISIONES

@ventas_bp.route('/comisiones/vendedor/<int:vendedor_id>', methods=['GET'])
@handle_exceptions(servicio='Ventas', cod_mensaje=6009)
def get_comisiones_vendedor(vendedor_id):
    """
    Obtener comisiones de un vendedor
    ---
    tags:
      - Comisiones
    parameters:
      - name: vendedor_id
        in: path
        type: integer
        required: true
        description: ID del vendedor
    responses:
      200:
        description: Lista de comisiones del vendedor
        schema:
          type: array
          items:
            $ref: '#/definitions/Comision'
    """
    comisiones = ComisionService.get_comisiones_by_vendedor(vendedor_id)
    return jsonify(comisiones), 200

@ventas_bp.route('/comisiones/pendientes', methods=['GET'])
@handle_exceptions(servicio='Ventas', cod_mensaje=6010)
def get_comisiones_pendientes():
    """
    Obtener comisiones pendientes de pago
    ---
    tags:
      - Comisiones
    responses:
      200:
        description: Lista de comisiones pendientes
        schema:
          type: array
          items:
            $ref: '#/definitions/Comision'
    """
    comisiones = ComisionService.get_comisiones_pendientes()
    return jsonify(comisiones), 200

@ventas_bp.route('/comisiones/<int:comision_id>/pagar', methods=['PUT'])
@handle_exceptions(servicio='Ventas', cod_mensaje=6011)
def marcar_comision_pagada(comision_id):
    """
    Marcar comisión como pagada
    ---
    tags:
      - Comisiones
    parameters:
      - name: comision_id
        in: path
        type: integer
        required: true
        description: ID de la comisión
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - fecha_pago
          properties:
            fecha_pago:
              type: string
              format: date
              description: Fecha del pago de la comisión
    responses:
      200:
        description: Comisión marcada como pagada
        schema:
          $ref: '#/definitions/Comision'
      400:
        description: Error en los datos
      404:
        description: Comisión no encontrada
    """
    data = request.get_json()
    if not data or not data.get('fecha_pago'):
        return jsonify({"error": "La fecha de pago es requerida"}), 400
    
    usuario_pago = request.headers.get('X-Usuario', 'sistema')
    comision, error = ComisionService.marcar_comision_pagada(
        comision_id, 
        data['fecha_pago'], 
        usuario_pago
    )
    
    if error:
        if "no encontrada" in error.lower():
            return jsonify({"error": error}), 404
        return jsonify({"error": error}), 400
    
    return jsonify(comision), 200