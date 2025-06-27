// src/app/services/usuario/user.service.ts

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { User } from 'src/app/models/usuario/user.model';
import { EnvConfig } from '../../env-config';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private baseUrl = `${EnvConfig.apiUrl}/usuarios`;

  constructor(private http: HttpClient) {}

  // Obtener todos los usuarios
  getAll(): Observable<User[]> {
    return this.http.get<User[]>(`${this.baseUrl}/`);
  }

  // Obtener usuario por ID
  getById(id: number): Observable<User> {
    return this.http.get<User>(`${this.baseUrl}/${id}`);
  }

  // Crear nuevo usuario (requiere contraseña)
  create(user: Partial<User> & { password: string }): Observable<User> {
    return this.http.post<User>(`${this.baseUrl}/`, user);
  }

  // Actualizar usuario existente
  update(id: number, user: Partial<User>): Observable<User> {
    return this.http.put<User>(`${this.baseUrl}/${id}`, user);
  }

  // Eliminar usuario (desactiva el usuario, no borra físicamente)
  delete(id: number): Observable<{ success: boolean }> {
    return this.http.delete<{ success: boolean }>(`${this.baseUrl}/${id}`);
  }
}
