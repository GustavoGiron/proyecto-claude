import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Cliente } from '../../models/cliente/cliente';

@Injectable({
  providedIn: 'root'
})
export class ClienteService {
  private API_URL = 'http://localhost:5000/api';

  constructor(private http: HttpClient) { }

  obtenerCliente(codigo: string): Observable<Cliente> {
    return this.http.get<Cliente>(`${this.API_URL}/clientes/${codigo}`);
  }

  crearCliente(cliente: Cliente): Observable<Cliente> {
    return this.http.post<Cliente>(`${this.API_URL}/clientes/`, cliente);
  }

  actualizarCliente(codigo: string, cliente: Cliente): Observable<Cliente> {
    return this.http.put<Cliente>(`${this.API_URL}/clientes/${codigo}`, cliente);
  }

  obtenerClientes(): Observable<Cliente[]> {
    return this.http.get<Cliente[]>(`${this.API_URL}/clientes/`);
  }

  eliminarCliente(codigo: string): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/clientes/${codigo}`);
  }
}