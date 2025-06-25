import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Cliente } from '../../models/cliente/cliente';
import { EnvConfig } from '../../env-config';

@Injectable({
  providedIn: 'root'
})
export class ClienteService {
  apiUrl = EnvConfig.apiUrl;

  constructor(private http: HttpClient) { }

  obtenerCliente(codigo: string): Observable<Cliente> {
    return this.http.get<Cliente>(`${this.apiUrl}/clientes/${codigo}`);
  }

  crearCliente(cliente: Cliente): Observable<Cliente> {
    return this.http.post<Cliente>(`${this.apiUrl}/clientes/`, cliente);
  }

  actualizarCliente(codigo: string, cliente: Cliente): Observable<Cliente> {
    return this.http.put<Cliente>(`${this.apiUrl}/clientes/${codigo}`, cliente);
  }

  obtenerClientes(): Observable<Cliente[]> {
    return this.http.get<Cliente[]>(`${this.apiUrl}/clientes/`);
  }

  eliminarCliente(codigo: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/clientes/${codigo}`);
  }
}