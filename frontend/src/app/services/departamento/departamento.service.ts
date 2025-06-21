import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Departamento, DepartamentoResponse, Municipio } from '../../models/departamento/departamento';

@Injectable({
  providedIn: 'root'
})
export class DepartamentoService {
  private API_URL = 'http://localhost:5000/api';

  constructor(private http: HttpClient) { }

  obtenerDepartamento(id: string): Observable<DepartamentoResponse> {
    return this.http.get<DepartamentoResponse>(`${this.API_URL}/departamentos/${id}`);
  }

  obtenerDepartamentos(): Observable<Departamento[]> {
    return this.http.get<Departamento[]>(`${this.API_URL}/departamentos/`);
  }

  obtenerMunicipiosPorDepartamento(departamentoId: number): Observable<Municipio[]> {
    return this.http.get<Municipio[]>(`${this.API_URL}/departamentos/${departamentoId}/municipios`);
  }
}