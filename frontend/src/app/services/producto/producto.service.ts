import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Producto, ProductoResponse, ApiResponse } from '../../models/producto/producto';
import { EnvConfig } from '../../env-config';

@Injectable({
  providedIn: 'root'
})
export class ProductoService {
  apiUrl = EnvConfig.apiUrl;

  constructor(private http: HttpClient) { }

  obtenerProducto(codigo: number): Observable<Producto> {
    return this.http.get<Producto>(`${this.apiUrl}/productos/${codigo}`);
  }

  crearProducto(producto: Producto): Observable<ApiResponse> {
    return this.http.post<ApiResponse>(`${this.apiUrl}/productos/`, producto);
  }

  actualizarProducto(id: number, producto: Producto): Observable<Producto> {
    return this.http.put<Producto>(`${this.apiUrl}/productos/${id}`, producto);
  }

  obtenerProductos(): Observable<Producto[]> {
    return this.http.get<Producto[]>(`${this.apiUrl}/productos/`);
  }

  eliminarProducto(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/productos/${id}`);
  }

  obtenerProductoActivo(): Observable<Producto[]> {
    return this.http.get<Producto[]>(`${this.apiUrl}/productos/activos`);
  }
}
