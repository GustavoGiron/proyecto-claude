from app.database import db

def up():
    """Create database structure"""
    with db.engine.connect() as conn:
        # Tabla Departamentos
        conn.execute(db.text("""
            CREATE TABLE Departamentos (
                Id INT AUTO_INCREMENT PRIMARY KEY,
                Codigo VARCHAR(2) NOT NULL UNIQUE,
                Nombre VARCHAR(50) NOT NULL
            )
        """))
        
        # Tabla Municipios
        conn.execute(db.text("""
            CREATE TABLE Municipios (
                Id INT AUTO_INCREMENT PRIMARY KEY,
                DepartamentoId INT NOT NULL,
                Nombre VARCHAR(100) NOT NULL,
                FOREIGN KEY (DepartamentoId) REFERENCES Departamentos(Id)
            )
        """))
        
        # Tabla Vendedores
        conn.execute(db.text("""
            CREATE TABLE Vendedores (
                Id INT AUTO_INCREMENT PRIMARY KEY,
                CodigoVendedor VARCHAR(20) NOT NULL UNIQUE,
                Nombres VARCHAR(100) NOT NULL,
                Apellidos VARCHAR(100) NOT NULL,
                Telefono VARCHAR(20),
                Direccion TEXT,
                PorcentajeComision DECIMAL(5,2) NOT NULL,
                FechaModificacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UsuarioCreacion VARCHAR(50),
                UsuarioModificacion VARCHAR(50)
            )
        """))
        
        # Tabla Clientes
        conn.execute(db.text("""
            CREATE TABLE Clientes (
                Id INT AUTO_INCREMENT PRIMARY KEY,
                NumeroCliente INT NOT NULL UNIQUE,
                CodigoCliente VARCHAR(10) NOT NULL UNIQUE,
                NombreContacto VARCHAR(200) NOT NULL,
                NombreNegocio VARCHAR(200),
                DepartamentoId INT NOT NULL,
                MunicipioId INT NOT NULL,
                Direccion TEXT,
                Nit VARCHAR(15),
                EncargadoBodega VARCHAR(100),
                Telefono VARCHAR(20),
                TipoVentaAutorizado VARCHAR(10) NOT NULL CHECK (TipoVentaAutorizado IN ('Credito', 'Contado', 'Ambas')),
                Observaciones TEXT,
                FechaModificacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UsuarioCreacion VARCHAR(50),
                UsuarioModificacion VARCHAR(50),
                FOREIGN KEY (DepartamentoId) REFERENCES Departamentos(Id),
                FOREIGN KEY (MunicipioId) REFERENCES Municipios(Id)
            )
        """))
        
        # Tabla Productos
        conn.execute(db.text("""
            CREATE TABLE Productos (
                Id INT AUTO_INCREMENT PRIMARY KEY,
                CodigoProducto VARCHAR(50) NOT NULL UNIQUE,
                NombreProducto VARCHAR(200) NOT NULL,
                UnidadMedida VARCHAR(10) NOT NULL CHECK (UnidadMedida IN ('Unidad', 'Fardo', 'Paquete')),
                UnidadesPorFardoPaquete INT NOT NULL DEFAULT 1,
                StockMinimo INT DEFAULT 0,
                FechaModificacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UsuarioCreacion VARCHAR(50),
                UsuarioModificacion VARCHAR(50)
            )
        """))
        
        conn.commit()

def down():
    """Drop all tables"""
    with db.engine.connect() as conn:
        tables = ['Clientes', 'Productos', 'Vendedores', 'Municipios', 'Departamentos']
        for table in tables:
            conn.execute(db.text(f"DROP TABLE IF EXISTS {table}"))
        conn.commit()