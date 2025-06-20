import React, { useState } from 'react';
import { useClientes } from '../hooks/useClientes';
import { useDepartamentos } from '../hooks/useDepartamentos';
import ClienteForm from './ClienteForm';

const ClientesList = () => {
  const { clientes, loading, error, deleteCliente } = useClientes();
  const { departamentos } = useDepartamentos();
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [activeView, setActiveView] = useState('list');
  const [clienteToEdit, setClienteToEdit] = useState(null);
  const [showNewButton, setShowNewButton] = useState(true);

  const itemsPerPage = 10;

  // Filtrar clientes por término de búsqueda
  const filteredClientes = clientes.filter(cliente =>
    cliente.nombre_contacto?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    cliente.nombre_negocio?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    cliente.codigo_cliente?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Paginación
  const totalPages = Math.ceil(filteredClientes.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const paginatedClientes = filteredClientes.slice(startIndex, startIndex + itemsPerPage);




  const handleDelete = async (id) => {
    if (window.confirm('¿Estás seguro de eliminar este cliente?')) {
      try {
        await deleteCliente(id);
        alert('Cliente eliminado exitosamente');
      } catch (err) {
        alert('Error al eliminar cliente: ' + err.message);
      }
    }
  };

  const getDepartamentoNombre = (departamentoId) => {
    const dept = departamentos.find(d => d.id === departamentoId);
    return dept ? dept.nombre : 'N/A';
  };

  const getUbicacion = (cliente) => {
    const departamento = getDepartamentoNombre(cliente.departamento_id);
    return departamento !== 'N/A' ? `${departamento}\n${cliente.direccion || ''}` : cliente.direccion || 'N/A';
  };

  if (loading) return <div className="loading">Cargando clientes...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  const handleDeleteClick = (codigo_cliente) => {
    const id = Number(codigo_cliente);
    if (isNaN(id)) {
      alert('ID inválido');
      return;
    }
    handleDelete(id);
  };

  return (
    <div className="clientes-container">
      {/* Header */}
      <div className="clientes-header">
        <h1>Clientes</h1>
        {showNewButton && (
          <button
            className="btn-nuevo-cliente"
            onClick={() => {
              setActiveView('form');
              setClienteToEdit(null);
              setShowNewButton(false); // Ocultar el botón
            }}
          >
            <span className="plus-icon">+</span>
            Nuevo Cliente
          </button>
        )}
      </div>

      {/* Mostrar tabla solo si activeView es 'list' */}
      {activeView === 'list' && (
        <>
          {/* Buscador */}
          <div className="search-container">
            <div className="search-input-wrapper">
              <span className="search-icon">🔍</span>
              <input
                type="text"
                placeholder="Buscar clientes"
                value={searchTerm}
                onChange={(e) => {
                  setSearchTerm(e.target.value);
                  setCurrentPage(1); // Reset a la primera página cuando se busca
                }}
                className="search-input"
              />
            </div>
          </div>

          {/* Tabla */}
          <div className="table-container">
            <table className="clientes-table">
              <thead>
                <tr>
                  <th>NÚMERO</th>
                  <th>CÓDIGO</th>
                  <th>NOMBRE DEL CONTACTO</th>
                  <th>NOMBRE DEL NEGOCIO</th>
                  <th>UBICACIÓN</th>
                  <th>TELÉFONO</th>
                  <th>ACCIONES</th>
                </tr>
              </thead>
              <tbody>
                {paginatedClientes.map((cliente) => (
                  <tr key={cliente.numero_cliente}>
                    <td>{cliente.numero_cliente}</td>
                    <td>{cliente.codigo_cliente}</td>
                    <td>{cliente.nombre_contacto}</td>
                    <td>{cliente.nombre_negocio}</td>
                    <td className="ubicacion-cell">
                      <div className="ubicacion-text">
                        {getUbicacion(cliente)}
                      </div>
                    </td>
                    <td>{cliente.telefono}</td>
                    <td>
                      <div className="actions-container">
                        <button
                          onClick={() => {
                            setShowNewButton(false);
                            setClienteToEdit(cliente);
                            setActiveView('form');
                          }}
                          className="action-btn edit-btn"
                          title="Editar"
                        >
                          ✏️
                        </button>
                        <button
                          onClick={() => handleDeleteClick(cliente.numero_cliente)}
                          className="action-btn delete-btn"
                          title="Eliminar"
                        >
                          🗑️
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Paginación */}
          <div className="pagination-container">
            <div className="pagination-info">
              Mostrando {startIndex + 1} a {Math.min(startIndex + itemsPerPage, filteredClientes.length)} de {filteredClientes.length} clientes
            </div>
            <div className="pagination-controls">
              <button
                className="pagination-btn"
                onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                disabled={currentPage === 1}
              >
                Anterior
              </button>
              <span className="pagination-current">{currentPage}</span>
              <button
                className="pagination-btn"
                onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                disabled={currentPage === totalPages}
              >
                Siguiente
              </button>
            </div>
          </div>
        </>
      )}

      {/* Mostrar formulario solo si activeView es 'form' */}
      {activeView === 'form' && (
        <ClienteForm
          onSuccess={() => {
            setActiveView('list');
            setClienteToEdit(null);
            setShowNewButton(true);
          }}
          cliente={clienteToEdit}
        />
      )}
    </div>
  );
}

export default ClientesList;