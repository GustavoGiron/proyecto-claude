import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Venta, VentaRequest, VentaResponse, ApiResponse } from '../../models/venta/venta';
import { EnvConfig } from '../../env-config';

@Injectable({
  providedIn: 'root'
})
export class VentaService {
  apiUrl = EnvConfig.apiUrl;

  constructor(private http: HttpClient) { }

  crearVenta(venta: VentaRequest): Observable<VentaResponse> {
    return this.http.post<VentaResponse>(`${this.apiUrl}/ventas/`, venta);
  }

  obtenerVenta(numero_envio: string): Observable<Venta> {
    return this.http.get<Venta>(`${this.apiUrl}/ventas/numero-envio/${numero_envio}`);
  }

  obtenerVentasPorCliente(nombre_cliente: string): Observable<Venta[]> {
    return this.http.get<Venta[]>(`${this.apiUrl}/ventas/cliente/${nombre_cliente}`);
  }

  registrarSalidaBodega(id: number, venta: Venta): Observable<ApiResponse> {
    return this.http.put<ApiResponse>(`${this.apiUrl}/ventas/${id}/salida-bodega`, venta);
  }

  registrarPago(id: number, venta: Venta): Observable<ApiResponse> {
    return this.http.post<ApiResponse>(`${this.apiUrl}/ventas/${id}/pagos`, venta);
  }

}
