import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Inventario, IngresoMercancia, DetalleIngreso, InventarioStock } from '../../models/inventario/inventario';
import { EnvConfig } from '../../env-config';

@Injectable({
  providedIn: 'root'
})
export class InventarioService {
  apiUrl = EnvConfig.apiUrl;

  constructor(private http: HttpClient) { }

  // Legacy method - keeping for backward compatibility
  crearInventario(inventario: Inventario): Observable<Inventario> {
    return this.http.post<Inventario>(`${this.apiUrl}/inventario/`, inventario);
  }

  // Get current inventory stock
  getInventarioStock(): Observable<InventarioStock[]> {
    return this.http.get<InventarioStock[]>(`${this.apiUrl}/inventario/`);
  }

  // New methods for Ingresos de Mercancía
  getIngresos(filters?: {
    numero_contenedor?: string;
    numero_duca?: string;
    fecha_desde?: string;
    fecha_hasta?: string;
  }): Observable<IngresoMercancia[]> {
    let params = new HttpParams();
    if (filters) {
      if (filters.numero_contenedor) params = params.set('numero_contenedor', filters.numero_contenedor);
      if (filters.numero_duca) params = params.set('numero_duca', filters.numero_duca);
      if (filters.fecha_desde) params = params.set('fecha_desde', filters.fecha_desde);
      if (filters.fecha_hasta) params = params.set('fecha_hasta', filters.fecha_hasta);
    }
    return this.http.get<IngresoMercancia[]>(`${this.apiUrl}/ingresos/`, { params });
  }

  getIngresoById(id: number): Observable<IngresoMercancia> {
    return this.http.get<IngresoMercancia>(`${this.apiUrl}/ingresos/${id}`);
  }

  crearIngreso(ingreso: IngresoMercancia): Observable<IngresoMercancia> {
    return this.http.post<IngresoMercancia>(`${this.apiUrl}/ingresos/`, ingreso);
  }

  actualizarIngreso(id: number, ingreso: Partial<IngresoMercancia>): Observable<IngresoMercancia> {
    return this.http.put<IngresoMercancia>(`${this.apiUrl}/ingresos/${id}`, ingreso);
  }

  eliminarIngreso(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/ingresos/${id}`);
  }

  confirmarIngreso(id: number, usuarioConfirmacion?: string): Observable<{message: string}> {
    const body = usuarioConfirmacion ? { usuario_confirmacion: usuarioConfirmacion } : {};
    return this.http.post<{message: string}>(`${this.apiUrl}/ingresos/${id}/confirmar`, body);
  }

  // Métodos para detalles
  getDetallesIngreso(ingresoId: number): Observable<DetalleIngreso[]> {
    return this.http.get<DetalleIngreso[]>(`${this.apiUrl}/ingresos/${ingresoId}/detalles`);
  }

  agregarDetalleIngreso(ingresoId: number, detalle: DetalleIngreso): Observable<DetalleIngreso> {
    return this.http.post<DetalleIngreso>(`${this.apiUrl}/ingresos/${ingresoId}/detalles`, detalle);
  }

  actualizarDetalle(detalleId: number, detalle: Partial<DetalleIngreso>): Observable<DetalleIngreso> {
    return this.http.put<DetalleIngreso>(`${this.apiUrl}/ingresos/detalles/${detalleId}`, detalle);
  }

  eliminarDetalle(detalleId: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/ingresos/detalles/${detalleId}`);
  }

  getTotalesIngreso(ingresoId: number): Observable<{
    total_productos_diferentes: number;
    total_fardos_paquetes: number;
    total_unidades: number;
    detalles: DetalleIngreso[];
  }> {
    return this.http.get<{
      total_productos_diferentes: number;
      total_fardos_paquetes: number;
      total_unidades: number;
      detalles: DetalleIngreso[];
    }>(`${this.apiUrl}/ingresos/${ingresoId}/totales`);
  }
}