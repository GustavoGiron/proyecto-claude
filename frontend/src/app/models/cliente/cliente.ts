export interface Cliente {
    id?: number;
    codigo_cliente: string;
    nombre_contacto: string;
    nombre_negocio: string;
    departamento_id: number;
    municipio_id: number;
    direccion: string;
    nit: string;
    encargado_bodega: string;
    telefono: string;
    tipo_venta_autoriz: string;
    observaciones: string;
}

export interface ClienteResponse {
    data: Cliente;
}

export interface ApiResponse {
    error?: string;
}