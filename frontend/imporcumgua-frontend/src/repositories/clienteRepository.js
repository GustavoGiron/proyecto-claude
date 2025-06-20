import { httpClient } from '../services/httpClient';

export class ClienteRepository {
  static async getClientes() {
    return httpClient.get('/api/clientes/');
  }

  static async getClienteById(id) {
    return httpClient.get(`/api/clientes/${id}`);
  }

  static async createCliente(clienteData) {
    return httpClient.post('/api/clientes/', clienteData);
  }

  static async updateCliente(id, clienteData) {
    return httpClient.put(`/api/clientes/${id}`, clienteData);
  }

  static async deleteCliente(id) {
    return httpClient.delete(`/clientes/${id}`);
  }
}