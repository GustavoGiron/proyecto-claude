CREATE DATABASE imporcomgua_db;

USE imporcomgua_db;

-- Tabla Departamentos
CREATE TABLE Departamentos (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Codigo VARCHAR(2) NOT NULL UNIQUE,
    Nombre VARCHAR(50) NOT NULL,
);

-- Tabla Municipios
CREATE TABLE Municipios (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    DepartamentoId INT NOT NULL,
    Nombre VARCHAR(100) NOT NULL,
    FOREIGN KEY (DepartamentoId) REFERENCES Departamentos(Id)
);

-- Tabla Vendedores
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
    UsuarioModificacion VARCHAR(50),
    
);

-- Tabla Clientes
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
);

-- Tabla Productos
CREATE TABLE Productos (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    CodigoProducto VARCHAR(50) NOT NULL UNIQUE,
    NombreProducto VARCHAR(200) NOT NULL,
    UnidadMedida VARCHAR(10) NOT NULL CHECK (UnidadMedida IN ('Unidad', 'Fardo', 'Paquete')),
    UnidadesPorFardoPaquete INT NOT NULL DEFAULT 1,
    StockMinimo INT DEFAULT 0,
    FechaModificacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UsuarioCreacion VARCHAR(50),
    UsuarioModificacion VARCHAR(50),
);

-- Tabla IngresosMercancia
CREATE TABLE IngresosMercancia (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    FechaIngreso DATE NOT NULL,
    NumeroContenedor VARCHAR(50) NOT NULL,
    NumeroDuca VARCHAR(50) NOT NULL,
    FechaDuca DATE NOT NULL,
    NumeroDucaRectificada VARCHAR(50),
    FechaDucaRectificada DATE,
    Observaciones TEXT,
    UsuarioCreacion VARCHAR(50),
);

-- Tabla DetalleIngresosMercancia
CREATE TABLE DetalleIngresosMercancia (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    IngresoMercanciaId INT NOT NULL,
    ProductoId INT NOT NULL,
    CantidadFardosPaquetes INT NOT NULL,
    UnidadesPorFardoPaquete INT NOT NULL,
    UnidadesTotales INT GENERATED ALWAYS AS (CantidadFardosPaquetes * UnidadesPorFardoPaquete) STORED,
    UsuarioCreacion VARCHAR(50),
    FOREIGN KEY (IngresoMercanciaId) REFERENCES IngresosMercancia(Id),
    FOREIGN KEY (ProductoId) REFERENCES Productos(Id)
);

-- Tabla Inventario
CREATE TABLE Inventario (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    ProductoId INT NOT NULL UNIQUE,
    StockDisponible INT NOT NULL DEFAULT 0,
    StockApartado INT NOT NULL DEFAULT 0,
    StockTotal INT GENERATED ALWAYS AS (StockDisponible + StockApartado) STORED,
    FechaUltimaActualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UsuarioUltimaActualizacion VARCHAR(50),
    FOREIGN KEY (ProductoId) REFERENCES Productos(Id)
);

-- Tabla MovimientosInventario
CREATE TABLE MovimientosInventario (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    ProductoId INT NOT NULL,
    TipoMovimiento VARCHAR(20) NOT NULL CHECK (TipoMovimiento IN ('Ingreso', 'Salida', 'Ajuste', 'Apartado', 'Liberado')),
    Cantidad INT NOT NULL,
    StockAnterior INT NOT NULL,
    StockNuevo INT NOT NULL,
    Referencia VARCHAR(100),
    Motivo VARCHAR(200),
    FechaMovimiento DATETIME DEFAULT CURRENT_TIMESTAMP,
    UsuarioMovimiento VARCHAR(50),
    FOREIGN KEY (ProductoId) REFERENCES Productos(Id)
);

-- Tabla Ventas
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
);

-- Tabla DetalleVentas
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
);

-- Tabla Pagos
CREATE TABLE Pagos (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    VentaId INT NOT NULL,
    NumeroReciboCaja VARCHAR(50) NOT NULL,
    FechaPago DATE NOT NULL,
    Banco VARCHAR(50) NOT NULL CHECK (Banco IN ('Industrial', 'Banrural', 'G&T', 'BAM')),
    NumeroCuenta VARCHAR(30) NOT NULL,
    NumeroTransferencia VARCHAR(50),
    MontoAbono DECIMAL(12,2) NOT NULL,
    SaldoAnterior DECIMAL(12,2) NOT NULL,
    SaldoActual DECIMAL(12,2) NOT NULL,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    UsuarioCreacion VARCHAR(50),
    FOREIGN KEY (VentaId) REFERENCES Ventas(Id)
);

-- Tabla Comisiones
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
);


-- Tabla logs
CREATE TABLE Logs (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    Funcion VARCHAR(100) NOT NULL,
    codMensaje INT NOT NULL,
    Servicio VARCHAR(100) NOT NULL,
    Descripcion TEXT
);