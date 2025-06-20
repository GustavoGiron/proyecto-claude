from app.database import db

def up():
    """Create sales related tables"""
    with db.engine.connect() as conn:
        # Tabla Ventas
        conn.execute(db.text("""
            CREATE TABLE Ventas (
                Id INT AUTO_INCREMENT PRIMARY KEY,
                FechaVenta DATE NOT NULL,
                FechaSalidaBodega DATE,
                ClienteId INT NOT NULL,
                NitCliente VARCHAR(15),
                NumeroEnvio VARCHAR(50) NOT NULL UNIQUE,
                TipoPago VARCHAR(10) NOT NULL CHECK (TipoPago IN ('Contado', 'Credito')),
                DiasCredito INT NOT NULL DEFAULT 0,
                FechaVencimiento DATE GENERATED ALWAYS AS (DATE_ADD(FechaVenta, INTERVAL DiasCredito DAY)) STORED,
                VendedorId INT NOT NULL,
                NumeroFacturaDTE VARCHAR(50),
                NombreFactura VARCHAR(200),
                NitFactura VARCHAR(15),
                SubtotalVenta DECIMAL(12,2) NOT NULL DEFAULT 0,
                IvaVenta DECIMAL(12,2) NOT NULL DEFAULT 0,
                TotalVenta DECIMAL(12,2) NOT NULL DEFAULT 0,
                EstadoVenta VARCHAR(20) NOT NULL DEFAULT 'Vigente' CHECK (EstadoVenta IN ('Vigente', 'Anulada')),
                EstadoCobro VARCHAR(20) NOT NULL DEFAULT 'Pendiente' CHECK (EstadoCobro IN ('Pendiente', 'Parcial', 'Pagada', 'Morosa')),
                EstadoEntrega VARCHAR(20) NOT NULL DEFAULT 'Pendiente' CHECK (EstadoEntrega IN ('Pendiente', 'Entregado')),
                FechaPagoCompleto DATE,
                SaldoPendiente DECIMAL(12,2) NOT NULL DEFAULT 0,
                FechaModificacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UsuarioCreacion VARCHAR(50),
                UsuarioModificacion VARCHAR(50),
                FOREIGN KEY (ClienteId) REFERENCES Clientes(Id),
                FOREIGN KEY (VendedorId) REFERENCES Vendedores(Id)
            )
        """))
        
        # Tabla DetalleVentas
        conn.execute(db.text("""
            CREATE TABLE DetalleVentas (
                Id INT AUTO_INCREMENT PRIMARY KEY,
                VentaId INT NOT NULL,
                ProductoId INT NOT NULL,
                Cantidad INT NOT NULL,
                CantidadUnidades INT NOT NULL DEFAULT 0,
                PrecioPorFardoPaquete DECIMAL(10,2) NOT NULL,
                SubtotalLinea DECIMAL(12,2) NOT NULL,
                IvaLinea DECIMAL(12,2) NOT NULL DEFAULT 0,
                TotalLinea DECIMAL(12,2) NOT NULL,
                EstadoLinea VARCHAR(20) NOT NULL DEFAULT 'Pendiente' CHECK (EstadoLinea IN ('Pendiente', 'Entregado')),
                Observaciones TEXT,
                UsuarioCreacion VARCHAR(50),
                FOREIGN KEY (VentaId) REFERENCES Ventas(Id),
                FOREIGN KEY (ProductoId) REFERENCES Productos(Id)
            )
        """))
        
        # Tabla Comisiones
        conn.execute(db.text("""
            CREATE TABLE Comisiones (
                Id INT AUTO_INCREMENT PRIMARY KEY,
                VentaId INT NOT NULL,
                VendedorId INT NOT NULL,
                TotalNetoVenta DECIMAL(12,2) NOT NULL,
                PorcentajeAplicado DECIMAL(5,2) NOT NULL,
                MontoComision DECIMAL(12,2) NOT NULL,
                EstadoComision VARCHAR(20) NOT NULL DEFAULT 'Pendiente' CHECK (EstadoComision IN ('Pendiente', 'Pagada')),
                FechaGeneracion DATETIME DEFAULT CURRENT_TIMESTAMP,
                FechaPago DATE,
                UsuarioPago VARCHAR(50),
                Observaciones TEXT,
                FOREIGN KEY (VentaId) REFERENCES Ventas(Id),
                FOREIGN KEY (VendedorId) REFERENCES Vendedores(Id)
            )
        """))
        
        conn.commit()

def down():
    """Drop sales tables"""
    with db.engine.connect() as conn:
        tables = ['Comisiones', 'DetalleVentas', 'Ventas']
        for table in tables:
            conn.execute(db.text(f"DROP TABLE IF EXISTS {table}"))
        conn.commit()