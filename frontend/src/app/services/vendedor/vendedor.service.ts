import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Vendedor, VendedorResponse, ApiResponse } from '../../models/vendedor/vendedor';

@Injectable({
  providedIn: 'root'
})
export class VendedorService {
  private API_URL = 'http://localhost:5000/api';

  constructor(private http: HttpClient) { }

  obtenerVendedor(codigo: string): Observable<Vendedor> {
    return this.http.get<Vendedor>(`${this.API_URL}/vendedores/codigo/${codigo}`);
  }

  crearVendedor(vendedor: Vendedor): Observable<ApiResponse> {
    return this.http.post<ApiResponse>(`${this.API_URL}/vendedores/`, vendedor);
  }

  actualizarVendedor(codigo: string, vendedor: Vendedor): Observable<ApiResponse> {
    return this.http.put<ApiResponse>(`${this.API_URL}/vendedores/codigo/${codigo}`, vendedor);
  }

  obtenerVendedores(): Observable<Vendedor[]> {
    return this.http.get<Vendedor[]>(`${this.API_URL}/vendedores/`);
  }

  eliminarVendedor(codigo: string): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/vendedores/codigo/${codigo}`);
  }
}