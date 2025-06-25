import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Departamento, DepartamentoResponse, Municipio } from '../../models/departamento/departamento';
import { EnvConfig } from '../../env-config';

@Injectable({
  providedIn: 'root'
})
export class DepartamentoService {
  apiUrl = EnvConfig.apiUrl;

  constructor(private http: HttpClient) { }

  obtenerDepartamento(id: string): Observable<DepartamentoResponse> {
    return this.http.get<DepartamentoResponse>(`${this.apiUrl}/departamentos/${id}`);
  }

  obtenerDepartamentos(): Observable<Departamento[]> {
    return this.http.get<Departamento[]>(`${this.apiUrl}/departamentos/`);
  }

  obtenerMunicipiosPorDepartamento(departamentoId: number): Observable<Municipio[]> {
    return this.http.get<Municipio[]>(`${this.apiUrl}/departamentos/${departamentoId}/municipios`);
  }
}