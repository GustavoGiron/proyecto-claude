# backend/app/models/__init__.py

# Importa todos tus modelos para que SQLAlchemy los registre
from .departamentos_model import Departamento
from .municipios_model    import Municipio
from .clientes_model      import Cliente
from .productos_model     import Producto
from .vendedores_model    import Vendedor
from .logs_model          import Log
