export interface Vendedor {
    id?: number;
    codigo_vendedor: string;
    nombres: string;
    apellidos: string;
    telefono: string;
    porcentaje_comision: number;
    direccion: string;
}

export interface VendedorResponse {
    data: Vendedor;
}

export interface ApiResponse {
    error?: string;
}