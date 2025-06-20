import React, { useState } from 'react';
import { useClientes } from '../hooks/useClientes';
import { useDepartamentos } from '../hooks/useDepartamentos';
//import './ClienteForm.css'; // Asegúrate de tener un archivo CSS para estilos

//const ClienteForm = ({ onSuccess }) => {
const ClienteForm = ({ onSuccess, cliente = null }) => {
  const { createCliente } = useClientes();
  const { departamentos, getMunicipios} = useDepartamentos();
  

   // Estado inicial para formData
  const [formData, setFormData] = useState({
    numero_cliente: cliente?.numero_cliente || '',
    codigo_cliente: cliente?.codigo_cliente || '',
    nombre_contacto: cliente?.nombre_contacto || '',
    nombre_negocio: cliente?.nombre_negocio || '',
    departamento_id: cliente?.departamento_id || '',
    municipio_id: cliente?.municipio_id || '',
    direccion: cliente?.direccion || '',
    nit: cliente?.nit || '',
    encargado_bodega: cliente?.encargado_bodega || '',
    telefono: cliente?.telefono || '',
    tipo_venta_autoriz: cliente?.tipo_venta_autoriz || 'Contado',
    observaciones: cliente?.observaciones || '',
    usuario_modificacion: 'frontend_user'
  });

  const [municipios, setMunicipios] = useState([]);
  const [loadingMunicipios, setLoadingMunicipios] = useState(false);
  const [errorMunicipios, setErrorMunicipios] = useState(null);

    const handleBack = () => {
    // Limpiamos los campos del formulario (opcional)
    setFormData({
      numero_cliente: '',
      codigo_cliente: '',
      nombre_contacto: '',
      nombre_negocio: '',
      departamento_id: '',
      municipio_id: '',
      direccion: '',
      nit: '',
      encargado_bodega: '',
      telefono: '',
      tipo_venta_autoriz: 'Contado',
      observaciones: '',
      usuario_modificacion: 'frontend_user'
    });
    setMunicipios([]);

    // Llamamos a onSuccess o simplemente regresamos
    if (onSuccess) {
      onSuccess();
    }
  };


  const handleChange = async (e) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value
    }));

    if (name === 'departamento_id') {
      if (!value) {
        setMunicipios([]);
        setFormData((prev) => ({ ...prev, municipio_id: '' }));
        return;
      }

      setLoadingMunicipios(true);
      setErrorMunicipios(null);
      try {
        const municipiosData = await getMunicipios(value);
        setMunicipios(municipiosData || []);
        setFormData((prev) => ({ ...prev, municipio_id: '' }));
      } catch (err) {
        console.error('Error al cargar municipios:', err);
        setErrorMunicipios('No se pudieron cargar los municipios.');
        setMunicipios([]);
      } finally {
        setLoadingMunicipios(false);
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validación básica
    if (!formData.departamento_id || !formData.municipio_id) {
      alert('Por favor selecciona un departamento y un municipio.');
      return;
    }

    try {
      await createCliente(formData);
      alert('Cliente creado exitosamente');
      onSuccess && onSuccess();

      // Reiniciar formulario
      setFormData({
        numero_cliente: '',
        codigo_cliente: '',
        nombre_contacto: '',
        nombre_negocio: '',
        departamento_id: '',
        municipio_id: '',
        direccion: '',
        nit: '',
        encargado_bodega: '',
        telefono: '',
        tipo_venta_autoriz: 'Contado',
        observaciones: '',
        usuario_modificacion: 'frontend_user'
      });
      setMunicipios([]);
    } catch (err) {
      alert('Error al crear cliente: ' + err.message);
    }
  };


  return (
    <form onSubmit={handleSubmit} className="cliente-form">
       <h2>{cliente ? 'Editar Cliente' : 'Crear Nuevo Cliente'}</h2>

      <div className="form-group">
        <label>Número Cliente:</label>
        <input
          type="number"
          name="numero_cliente"
          value={formData.numero_cliente}
          onChange={handleChange}
          required
          disabled={cliente ? true : false}
        />
      </div>

      <div className="form-group">
        <label>Código Cliente:</label>
        <input
          type="text"
          name="codigo_cliente"
          value={formData.codigo_cliente}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label>Nombre Contacto:</label>
        <input
          type="text"
          name="nombre_contacto"
          value={formData.nombre_contacto}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label>Nombre Negocio:</label>
        <input
          type="text"
          name="nombre_negocio"
          value={formData.nombre_negocio}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label>Departamento:</label>
        <select
          name="departamento_id"
          value={formData.departamento_id}
          onChange={handleChange}
          required
        >
          <option value="">Seleccionar Departamento</option>
          {departamentos.map((muni) => (
            <option key={muni.id} value={muni.id}>
              {muni.nombre}
            </option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label>Municipio:</label>
        <select
          name="municipio_id"
          value={formData.municipio_id}
          onChange={handleChange}
          required
        >
          <option value="">Seleccionar Municipio</option>
          {municipios.map((muni) => (
            <option key={muni.id} value={muni.id}>
              {muni.nombre}
            </option>
          ))}
        </select>
        {loadingMunicipios && <p>Cargando municipios...</p>}
        {errorMunicipios && <p style={{ color: 'red' }}>{errorMunicipios}</p>}
      </div>

      <div className="form-group">
        <label>Dirección:</label>
        <input
          type="text"
          name="direccion"
          value={formData.direccion}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label>NIT:</label>
        <input
          type="text"
          name="nit"
          value={formData.nit}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label>Encargado Bodega:</label>
        <input
          type="text"
          name="encargado_bodega"
          value={formData.encargado_bodega}
          onChange={handleChange}
        />
      </div>

      <div className="form-group">
        <label>Teléfono:</label>
        <input
          type="text"
          name="telefono"
          value={formData.telefono}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label>Tipo Venta Autorizada:</label>
        <select
          name="tipo_venta_autoriz"
          value={formData.tipo_venta_autoriz}
          onChange={handleChange}
        >
          <option value="Contado">Contado</option>
          <option value="Crédito">Crédito</option>
        </select>
      </div>

      <div className="form-group">
        <label>Observaciones:</label>
        <textarea
          name="observaciones"
          value={formData.observaciones}
          onChange={handleChange}
          rows="3"
        />
      </div>
      <button type="submit" onClick={handleBack}>
        Regresar
      </button>
      <button type="submit">{cliente ? 'Guardar Cambios' : 'Crear Cliente'}</button>
      {/* <button type="submit">Crear Cliente</button> */}
    </form>
  );
};

export default ClienteForm;