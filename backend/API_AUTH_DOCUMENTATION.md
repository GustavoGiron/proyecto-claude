# Documentación API de Autenticación

## Endpoints de Autenticación

### 1. Login de Usuario
**POST** `/api/auth/login`

Autentica un usuario y devuelve tokens de acceso.

#### Request
```json
{
  "username": "admin",
  "password": "admin123"
}
```

#### Response (200 OK)
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@imporcomgua.com",
    "nombre": "Administrador",
    "apellido": "General",
    "is_active": true,
    "fecha_creacion": "2025-01-20T10:30:00",
    "ultima_sesion": "2025-01-20T15:45:00",
    "role": "Gerencia General"
  }
}
```

#### Errores
- **401**: Credenciales inválidas o usuario inactivo
- **400**: Datos inválidos

---

### 2. Refrescar Token
**POST** `/api/auth/refresh`

Genera un nuevo access token usando el refresh token.

#### Request
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Response (200 OK)
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Errores
- **401**: Token inválido o expirado

---

### 3. Obtener Usuario Actual
**GET** `/api/auth/me`

Obtiene la información del usuario autenticado.

#### Headers
```
Authorization: Bearer {access_token}
```

#### Response (200 OK)
```json
{
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@imporcomgua.com", 
    "nombre": "Administrador",
    "apellido": "General",
    "is_active": true,
    "fecha_creacion": "2025-01-20T10:30:00",
    "ultima_sesion": "2025-01-20T15:45:00",
    "role": "Gerencia General"
  }
}
```

#### Errores
- **401**: Token inválido, expirado o usuario no encontrado

---

### 4. Obtener Permisos del Usuario
**GET** `/api/auth/permissions`

Obtiene los módulos y permisos del usuario autenticado.

#### Headers
```
Authorization: Bearer {access_token}
```

#### Response (200 OK)
```json
{
  "role": "Gerencia General",
  "modules": [
    {
      "id": 1,
      "nombre": "Dashboard",
      "ruta": "/dashboard", 
      "icono": "dashboard"
    },
    {
      "id": 2,
      "nombre": "Clientes",
      "ruta": "/clientes",
      "icono": "people"
    },
    {
      "id": 3,
      "nombre": "Productos", 
      "ruta": "/productos",
      "icono": "inventory"
    }
    // ... más módulos
  ],
  "permissions": [
    {
      "module": "Clientes",
      "action": "read",
      "permission": "Ver Clientes"
    },
    {
      "module": "Clientes", 
      "action": "create",
      "permission": "Crear Clientes"
    },
    {
      "module": "Productos",
      "action": "read", 
      "permission": "Ver Productos"
    }
    // ... más permisos
  ]
}
```

#### Errores
- **401**: Token inválido o usuario no encontrado
- **400**: Error al procesar la solicitud

---

### 5. Cerrar Sesión
**POST** `/api/auth/logout`

Cierra la sesión del usuario (invalidación del lado del cliente).

#### Headers
```
Authorization: Bearer {access_token}
```

#### Response (200 OK)
```json
{
  "message": "Sesión cerrada exitosamente"
}
```

---

## Usuarios de Prueba

Después de ejecutar las migraciones y seeders:

| Username | Password | Rol | Módulos de Acceso |
|----------|----------|-----|-------------------|
| `admin` | `admin123` | Gerencia General | Todos los módulos |
| `gerente_ventas` | `ventas123` | Gerencia de Ventas y Finanzas | Dashboard, Clientes, Ventas, Pagos, Vendedores, Reportes |
| `gerente_inventario` | `inventario123` | Gerencia de Inventario | Dashboard, Productos, Inventario, Ingresos, Salidas, Reportes |

---

## Módulos del Sistema

| ID | Nombre | Descripción | Ruta | Icono |
|----|--------|-------------|------|-------|
| 1 | Dashboard | Panel de control principal | `/dashboard` | `dashboard` |
| 2 | Clientes | Gestión de clientes | `/clientes` | `people` |
| 3 | Productos | Gestión de productos | `/productos` | `inventory` |
| 4 | Inventario | Control de inventario | `/inventario` | `warehouse` |
| 5 | Ingresos | Registro de ingresos | `/ingresos` | `add_box` |
| 6 | Salidas | Registro de salidas | `/salidas` | `remove_circle` |
| 7 | Ventas | Gestión de ventas | `/ventas` | `shopping_cart` |
| 8 | Pagos | Gestión de pagos | `/pagos` | `payment` |
| 9 | Vendedores | Gestión de vendedores | `/vendedores` | `badge` |
| 10 | Reportes | Reportes del sistema | `/reportes` | `analytics` |
| 11 | Configuración | Configuración del sistema | `/configuracion` | `settings` |

---

## Permisos por Acción

### Acciones Disponibles:
- **read**: Ver/listar datos
- **create**: Crear nuevos registros
- **update**: Modificar registros existentes
- **delete**: Eliminar registros

### Matriz de Permisos por Rol:

| Módulo | Gerencia General | Gerencia Ventas | Gerencia Inventario |
|--------|------------------|-----------------|-------------------|
| Dashboard | ✅ read | ✅ read | ✅ read |
| Clientes | ✅ CRUD | ✅ CRUD | ❌ |
| Productos | ✅ CRUD | ❌ | ✅ CRUD |
| Inventario | ✅ CRUD | ❌ | ✅ CRUD |
| Ingresos | ✅ CRUD | ❌ | ✅ CRUD |
| Salidas | ✅ CRUD | ❌ | ✅ CRUD |
| Ventas | ✅ CRUD | ✅ CRUD | ❌ |
| Pagos | ✅ CRUD | ✅ CRUD | ❌ |
| Vendedores | ✅ CRUD | ✅ CRUD | ❌ |
| Reportes | ✅ read | ✅ read | ✅ read |
| Configuración | ✅ update | ❌ | ❌ |

---

## Uso en el Frontend

### 1. Almacenar Tokens
```javascript
// Después del login exitoso
localStorage.setItem('access_token', response.access_token);
localStorage.setItem('refresh_token', response.refresh_token);
localStorage.setItem('user', JSON.stringify(response.user));
```

### 2. Configurar Headers de Autenticación
```javascript
// Para todas las requests autenticadas
const token = localStorage.getItem('access_token');
axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
```

### 3. Manejar Tokens Expirados
```javascript
// Interceptor para refrescar tokens automáticamente
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const refreshToken = localStorage.getItem('refresh_token');
      try {
        const response = await axios.post('/api/auth/refresh', {
          refresh_token: refreshToken
        });
        localStorage.setItem('access_token', response.data.access_token);
        // Reintentar la request original
        error.config.headers.Authorization = `Bearer ${response.data.access_token}`;
        return axios.request(error.config);
      } catch {
        // Redirigir al login
        localStorage.clear();
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);
```

### 4. Verificar Permisos en el Frontend
```javascript
// Obtener permisos del usuario
const permissions = await axios.get('/api/auth/permissions');

// Función helper para verificar permisos
function hasPermission(module, action) {
  return permissions.data.permissions.some(
    p => p.module === module && p.action === action
  );
}

// Uso en componentes
if (hasPermission('Clientes', 'create')) {
  // Mostrar botón de crear cliente
}
```

### 5. Generar Menú Dinámico
```javascript
// Usar los módulos para generar el menú de navegación
const modules = permissions.data.modules;
const menuItems = modules.map(module => ({
  name: module.nombre,
  path: module.ruta,
  icon: module.icono
}));
```

---

## Configuración de Desarrollo

### Variables de Entorno
Agregar al archivo `.env`:
```
SECRET_KEY=tu-clave-secreta-muy-segura
JWT_SECRET_KEY=tu-clave-jwt-muy-segura
```

### Ejecutar Migraciones y Seeders
```bash
# Ejecutar migración de autenticación
python migrate.py

# Crear usuarios de prueba
python seeders/usuarios_seeder.py
```

### Swagger/OpenAPI
La documentación interactiva está disponible en:
```
http://localhost:5000/docs/
```

---

## Códigos de Error Comunes

| Código | Descripción | Solución |
|--------|-------------|----------|
| 401 | Token faltante | Incluir header `Authorization: Bearer {token}` |
| 401 | Token expirado | Usar refresh token para obtener nuevo access token |
| 401 | Token inválido | Verificar formato del token o re-autenticar |
| 403 | Sin permisos | Usuario no tiene permisos para esta acción |
| 400 | Datos inválidos | Verificar formato de los datos enviados |

---

## Seguridad

### Buenas Prácticas Implementadas:
- ✅ Tokens JWT con expiración (24h access, 30d refresh)
- ✅ Hashing seguro de contraseñas (PBKDF2-SHA256)
- ✅ Validación de permisos granular
- ✅ Headers CORS configurados
- ✅ Logging de intentos de autenticación
- ✅ Validación de usuarios activos

### Recomendaciones:
- Usar HTTPS en producción
- Configurar SECRET_KEY y JWT_SECRET_KEY seguros
- Rotar secrets periódicamente
- Implementar rate limiting en endpoints de login
- Monitorear intentos de acceso fallidos