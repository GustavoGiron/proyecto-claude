import React, { useState } from 'react';
import ClientesList from './components/ClientesList';
import ClienteForm from './components/ClienteForm';
import './App.css';

function App() {
  const [activeView, setActiveView] = useState('list');
  const [clienteToEdit, setClienteToEdit] = useState(null);

  const handleEdit = (cliente) => {
    setClienteToEdit(cliente);
    setActiveView('form');
  };

  return (
    <div className="App">
      <main>
        {activeView === 'list' && (
          <ClientesList />
        )}
        {activeView === 'form' && (
          <ClienteForm
            onSuccess={() => {
              setActiveView('list');
              setClienteToEdit(null); 
            }}
            cliente={clienteToEdit}
          />
        )}
      </main>
    </div>
  );
}

export default App;