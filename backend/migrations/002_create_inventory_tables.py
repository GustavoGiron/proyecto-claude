from app.database import db

def up():
    """Create inventory related tables"""
    with db.engine.connect() as conn:
        # Tabla IngresosMercancia
        conn.execute(db.text("""
            CREATE TABLE IngresosMercancia (
                Id INT AUTO_INCREMENT PRIMARY KEY,
                FechaIngreso DATE NOT NULL,
                NumeroContenedor VARCHAR(50) NOT NULL,
                NumeroDuca VARCHAR(50) NOT NULL,
                FechaDuca DATE NOT NULL,
                NumeroDucaRectificada VARCHAR(50),
                FechaDucaRectificada DATE,
                Observaciones TEXT,
                UsuarioCreacion VARCHAR(50)
            )
        """))
        
        # Tabla DetalleIngresosMercancia
        conn.execute(db.text("""
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
            )
        """))
        
        # Tabla Inventario
        conn.execute(db.text("""
            CREATE TABLE Inventario (
                Id INT AUTO_INCREMENT PRIMARY KEY,
                ProductoId INT NOT NULL UNIQUE,
                StockDisponible INT NOT NULL DEFAULT 0,
                StockApartado INT NOT NULL DEFAULT 0,
                StockTotal INT GENERATED ALWAYS AS (StockDisponible + StockApartado) STORED,
                FechaUltimaActualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UsuarioUltimaActualizacion VARCHAR(50),
                FOREIGN KEY (ProductoId) REFERENCES Productos(Id)
            )
        """))
        
        # Tabla MovimientosInventario
        conn.execute(db.text("""
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
            )
        """))
        
        conn.commit()

def down():
    """Drop inventory tables"""
    with db.engine.connect() as conn:
        tables = ['MovimientosInventario', 'Inventario', 'DetalleIngresosMercancia', 'IngresosMercancia']
        for table in tables:
            conn.execute(db.text(f"DROP TABLE IF EXISTS {table}"))
        conn.commit()