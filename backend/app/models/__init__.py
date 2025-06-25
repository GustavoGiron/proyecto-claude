# backend/app/models/__init__.py

# Importa todos tus modelos para que SQLAlchemy los registre
from .departamentos_model import Departamento
from .municipios_model    import Municipio
from .clientes_model      import Cliente
from .productos_model     import Producto
from .vendedores_model    import Vendedor
from .logs_model          import Log
from .ventas_model        import Venta, DetalleVenta, Pago, Comision
from .usuarios_model      import Usuario
from .roles_model         import Role
from .modules_model       import Module
from .permissions_model   import Permission
from .role_modules_model  import RoleModule
from .role_permissions_model import RolePermission