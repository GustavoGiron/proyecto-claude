export interface Producto {
    id?: number;
    codigo_producto: string;
    nombre_producto: string;
    unidad_medida: string;
    unidades_por_fardo_paquete: number;
    estado_producto: string;
}

export interface ProductoResponse {
    data: Producto;
}

export interface ApiResponse {
    error?: string;
}