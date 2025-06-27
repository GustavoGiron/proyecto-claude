import { User } from './user';

export { User } from './user';

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  user: User;
}

export interface RefreshTokenRequest {
  refresh_token: string;
}

export interface RefreshTokenResponse {
  access_token: string;
}

export interface UserResponse {
  user: User;
}

export interface Module {
  id: number;
  nombre: string;
  ruta: string;
  icono: string;
}

export interface Permission {
  module: string;
  action: string;
  permission: string;
}

export interface PermissionsResponse {
  role: string;
  modules: Module[];
  permissions: Permission[];
}