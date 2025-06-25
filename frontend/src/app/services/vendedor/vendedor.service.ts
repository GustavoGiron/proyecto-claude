import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Vendedor, VendedorResponse, ApiResponse } from '../../models/vendedor/vendedor';
import { EnvConfig } from '../../env-config';

@Injectable({
  providedIn: 'root'
})
export class VendedorService {
  apiUrl = EnvConfig.apiUrl;

  constructor(private http: HttpClient) { }

  obtenerVendedor(codigo: string): Observable<Vendedor> {
    return this.http.get<Vendedor>(`${this.apiUrl}/vendedores/codigo/${codigo}`);
  }

  obtenerVendedorPorId(id: number): Observable<Vendedor> {
    return this.http.get<Vendedor>(`${this.apiUrl}/vendedores/${id}`);
  }

  crearVendedor(vendedor: Vendedor): Observable<ApiResponse> {
    return this.http.post<ApiResponse>(`${this.apiUrl}/vendedores/`, vendedor);
  }

  actualizarVendedor(codigo: string, vendedor: Vendedor): Observable<ApiResponse> {
    return this.http.put<ApiResponse>(`${this.apiUrl}/vendedores/codigo/${codigo}`, vendedor);
  }

  obtenerVendedores(): Observable<Vendedor[]> {
    return this.http.get<Vendedor[]>(`${this.apiUrl}/vendedores/`);
  }

  eliminarVendedor(codigo: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/vendedores/codigo/${codigo}`);
  }
}