"""
Migración 008: Crear tablas de autenticación y permisos
"""
from app.database import db

def up():
    """Create auth tables"""
    with db.engine.connect() as conn:
        # Crear tabla de roles
        conn.execute(db.text("""
            CREATE TABLE IF NOT EXISTS roles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(50) NOT NULL UNIQUE,
                descripcion VARCHAR(200),
                is_active BOOLEAN DEFAULT TRUE,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """))
        
        # Crear tabla de usuarios
        conn.execute(db.text("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                email VARCHAR(100) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                apellido VARCHAR(100) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                ultima_sesion DATETIME NULL,
                role_id INT NOT NULL,
                FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE RESTRICT ON UPDATE CASCADE,
                INDEX idx_username (username),
                INDEX idx_email (email),
                INDEX idx_role (role_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """))
        
        # Crear tabla de módulos
        conn.execute(db.text("""
            CREATE TABLE IF NOT EXISTS modules (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(50) NOT NULL UNIQUE,
                descripcion VARCHAR(200),
                ruta VARCHAR(100),
                icono VARCHAR(50),
                orden INT DEFAULT 0,
                is_active BOOLEAN DEFAULT TRUE,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_orden (orden)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """))
        
        # Crear tabla de permisos
        conn.execute(db.text("""
            CREATE TABLE IF NOT EXISTS permissions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(50) NOT NULL,
                descripcion VARCHAR(200),
                accion VARCHAR(50) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                module_id INT NOT NULL,
                FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE ON UPDATE CASCADE,
                INDEX idx_module (module_id),
                INDEX idx_accion (accion)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """))
        
        # Crear tabla de relación role_modules
        conn.execute(db.text("""
            CREATE TABLE IF NOT EXISTS role_modules (
                id INT AUTO_INCREMENT PRIMARY KEY,
                role_id INT NOT NULL,
                module_id INT NOT NULL,
                FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE ON UPDATE CASCADE,
                UNIQUE KEY unique_role_module (role_id, module_id),
                INDEX idx_role (role_id),
                INDEX idx_module (module_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """))
        
        # Crear tabla de relación role_permissions
        conn.execute(db.text("""
            CREATE TABLE IF NOT EXISTS role_permissions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                role_id INT NOT NULL,
                permission_id INT NOT NULL,
                FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE ON UPDATE CASCADE,
                UNIQUE KEY unique_role_permission (role_id, permission_id),
                INDEX idx_role (role_id),
                INDEX idx_permission (permission_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """))
        
        # Insertar roles iniciales
        conn.execute(db.text("""
            INSERT INTO roles (nombre, descripcion) VALUES 
            ('Gerencia General', 'Acceso completo a todos los módulos del sistema'),
            ('Gerencia de Ventas y Finanzas', 'Acceso a módulos de ventas, clientes y pagos'),
            ('Gerencia de Inventario', 'Acceso a módulos de productos, inventario y movimientos');
        """))
        
        # Insertar módulos iniciales
        conn.execute(db.text("""
            INSERT INTO modules (nombre, descripcion, ruta, icono, orden) VALUES 
            ('Dashboard', 'Panel de control principal', '/dashboard', 'dashboard', 1),
            ('Clientes', 'Gestión de clientes', '/clientes', 'people', 2),
            ('Productos', 'Gestión de productos', '/productos', 'inventory', 3),
            ('Inventario', 'Control de inventario', '/inventario', 'warehouse', 4),
            ('Ingresos', 'Registro de ingresos de inventario', '/ingresos', 'add_box', 5),
            ('Salidas', 'Registro de salidas de inventario', '/salidas', 'remove_circle', 6),
            ('Ventas', 'Gestión de ventas', '/ventas', 'shopping_cart', 7),
            ('Pagos', 'Gestión de pagos', '/pagos', 'payment', 8),
            ('Vendedores', 'Gestión de vendedores', '/vendedores', 'badge', 9),
            ('Reportes', 'Reportes del sistema', '/reportes', 'analytics', 10),
            ('Configuración', 'Configuración del sistema', '/configuracion', 'settings', 11);
        """))
        
        # Asignar módulos a roles
        conn.execute(db.text("""
            INSERT INTO role_modules (role_id, module_id)
            SELECT 1, id FROM modules;  -- Gerencia General tiene acceso a todos los módulos
        """))
        
        conn.execute(db.text("""
            INSERT INTO role_modules (role_id, module_id)
            SELECT 2, id FROM modules 
            WHERE nombre IN ('Dashboard', 'Clientes', 'Ventas', 'Pagos', 'Vendedores', 'Reportes');
        """))
        
        conn.execute(db.text("""
            INSERT INTO role_modules (role_id, module_id)
            SELECT 3, id FROM modules 
            WHERE nombre IN ('Dashboard', 'Productos', 'Inventario', 'Ingresos', 'Salidas', 'Reportes');
        """))
        
        # Insertar permisos básicos
        conn.execute(db.text("""
            INSERT INTO permissions (nombre, descripcion, accion, module_id)
            SELECT 
                CONCAT('Ver ', m.nombre) as nombre,
                CONCAT('Permiso para ver ', m.nombre) as descripcion,
                'read' as accion,
                m.id as module_id
            FROM modules m;
        """))
        
        conn.execute(db.text("""
            INSERT INTO permissions (nombre, descripcion, accion, module_id)
            SELECT 
                CONCAT('Crear ', m.nombre) as nombre,
                CONCAT('Permiso para crear en ', m.nombre) as descripcion,
                'create' as accion,
                m.id as module_id
            FROM modules m
            WHERE m.nombre NOT IN ('Dashboard', 'Reportes', 'Configuración');
        """))
        
        conn.execute(db.text("""
            INSERT INTO permissions (nombre, descripcion, accion, module_id)
            SELECT 
                CONCAT('Editar ', m.nombre) as nombre,
                CONCAT('Permiso para editar en ', m.nombre) as descripcion,
                'update' as accion,
                m.id as module_id
            FROM modules m
            WHERE m.nombre NOT IN ('Dashboard', 'Reportes');
        """))
        
        conn.execute(db.text("""
            INSERT INTO permissions (nombre, descripcion, accion, module_id)
            SELECT 
                CONCAT('Eliminar ', m.nombre) as nombre,
                CONCAT('Permiso para eliminar en ', m.nombre) as descripcion,
                'delete' as accion,
                m.id as module_id
            FROM modules m
            WHERE m.nombre NOT IN ('Dashboard', 'Reportes', 'Configuración');
        """))
        
        conn.commit()
        print("✅ Migración 008: Tablas de autenticación creadas exitosamente")

def down():
    """Drop auth tables"""
    with db.engine.connect() as conn:
        # Eliminar tablas en orden inverso por las foreign keys
        conn.execute(db.text("DROP TABLE IF EXISTS role_permissions"))
        conn.execute(db.text("DROP TABLE IF EXISTS role_modules"))
        conn.execute(db.text("DROP TABLE IF EXISTS permissions"))
        conn.execute(db.text("DROP TABLE IF EXISTS usuarios"))
        conn.execute(db.text("DROP TABLE IF EXISTS modules"))
        conn.execute(db.text("DROP TABLE IF EXISTS roles"))
        
        conn.commit()
        print("✅ Migración 008: Rollback completado")