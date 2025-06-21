export interface Departamento {
    id: number;
    codigo: string;
    nombre: string;
}

export interface Municipio {
    id: number;
    codigo: string;
    nombre: string;
    departamento_id: number;
}


export interface DepartamentoResponse {
    data: Departamento;
}

export interface ApiResponse {
    error?: string;
}