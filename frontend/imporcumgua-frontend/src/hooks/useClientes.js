import { useState, useEffect } from 'react';
import { ClienteRepository } from '../repositories/clienteRepository';

export const useClientes = () => {
  const [clientes, setClientes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchClientes = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await ClienteRepository.getClientes();
      setClientes(Array.isArray(data) ? data : [data]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchClientes();
  }, []);

  const createCliente = async (clienteData) => {
    try {
      const newCliente = await ClienteRepository.createCliente(clienteData);
      setClientes(prev => [...prev, newCliente]);
      return newCliente;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };

  const updateCliente = async (id, clienteData) => {
    try {
      const updatedCliente = await ClienteRepository.updateCliente(id, clienteData);
      setClientes(prev => 
        prev.map(cliente => 
          cliente.codigo_cliente === id ? updatedCliente : cliente
        )
      );
      return updatedCliente;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };

  const deleteCliente = async (id) => {
  try {
    await ClienteRepository.deleteCliente(id);
    fetchClientes();
    setClientes(prev => prev.filter(cliente => cliente.codigo_cliente !== id));
  } catch (err) {
    setError(err.message);
    throw err;
  }
};

  return {
    clientes,
    loading,
    error,
    fetchClientes,
    createCliente,
    updateCliente,
    deleteCliente,
  };
};