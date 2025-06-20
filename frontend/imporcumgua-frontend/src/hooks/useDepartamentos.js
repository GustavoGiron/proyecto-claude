import { useState, useEffect } from 'react';
import { DepartamentoRepository } from '../repositories/departamentoRepository';

export const useDepartamentos = () => {
  const [departamentos, setDepartamentos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDepartamentos = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await DepartamentoRepository.getDepartamentos();
        setDepartamentos(Array.isArray(data) ? data : [data]);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchDepartamentos();
  }, []);

  const getMunicipios = async (departamentoId) => {
    try {
      return await DepartamentoRepository.getMunicipiosByDepartamento(departamentoId);
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };

  return {
    departamentos,
    loading,
    error,
    getMunicipios,
  };
};