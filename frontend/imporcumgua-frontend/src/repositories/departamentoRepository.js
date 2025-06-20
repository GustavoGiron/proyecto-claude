import { httpClient } from '../services/httpClient';

export class DepartamentoRepository {
  static async getDepartamentos() {
    return httpClient.get('/api/departamentos/');
  }

  static async getDepartamentoById(id) {
    return httpClient.get(`/api/departamentos/${id}`);
  }

  static async getMunicipiosByDepartamento(departamentoId) {
    return httpClient.get(`/api/departamentos/${departamentoId}/municipios`);
  }
}