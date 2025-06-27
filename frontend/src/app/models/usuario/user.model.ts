export interface User {
    id: number;
    username: string;
    email: string;
    nombre: string;
    apellido: string;
    is_active: boolean;
    fecha_creacion?: string;
    ultima_sesion?: string;
    role?: string; // nombre del rol
    password?: string; // opcional, para crear o actualizar
}