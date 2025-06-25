export interface Venta {
    id?: number;
    fecha_venta: string;
    fecha_salida_bodega: string;
    numero_envio: string;
    cliente_id: number;
    nit_cliente: string;
    tipo_pago: string;
    dias_credito: number;
    vendedor_id: number;
    nombre_vendedor?: string;
    numero_factura_dte: string;
    nombre_factura: string;
    nit_factura: string;
    observaciones: string;
    total_venta: number;
    productos: [];
    detalles: DetalleVenta[];
    estado_cobro?: string;
    estado_entrega?: string;
    estado_venta?: string;
    fecha_modificacion?: string;
    fecha_pago_completo?: string;
    iva_venta?: number;
    pagos?: Pago[];
    saldo_pendiente?: number;
    subtotal_venta?: number;
}

export interface VentaResponse {
    id: number;
    fecha_venta: string;
    cliente_id: number;
    vendedor_id: number;
    tipo_pago: string;
    dias_credito: number;
    numero_factura_dte: string;
    nombre_factura: string;
    nit_factura: string;
    detalles: DetalleVenta[];
}
export interface VentaRequest {
    cliente_id: number;
    vendedor_id: number;
    tipo_pago: 'Contado' | 'Credito';
    dias_credito: number;
    fecha_venta?: string;
    numero_factura_dte?: string;
    nombre_factura?: string;
    nit_cliente?: string;
    nit_factura?: string;
    detalles: DetalleVenta[];
}

export interface DetalleVenta {
    id?: number;
    producto_id: number;
    nombre_producto?: string;
    cantidad: number;
    precio_por_fardo_paquete: number;
    cantidad_unidades?: number;
    estado_linea?: number;
    iva_linea?: number;
    observaciones?: string;
    subtotal_linea?: number;
    total_linea?: number;
    usuario_creacion?: string;
    venta_id?: number;
}

export interface ApiResponse {
    error?: string;
}

export interface Pago {
    numero_recibo_caja: string;
    fecha_pago: string;
    banco: string;
    numero_cuenta: string;
    numero_transferencia: string;
    monto_abono: number;
}