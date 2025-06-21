from app.database import db

def up():
    """Create pagos table"""
    with db.engine.connect() as conn:
        conn.execute(db.text("""
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
            )
        """))
        conn.commit()

def down():
    """Drop pagos table"""
    with db.engine.connect() as conn:
        conn.execute(db.text("DROP TABLE IF EXISTS Pagos"))
        conn.commit()