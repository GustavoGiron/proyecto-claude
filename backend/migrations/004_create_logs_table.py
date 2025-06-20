from app.database import db

def up():
    """Create logs table"""
    with db.engine.connect() as conn:
        conn.execute(db.text("""
            CREATE TABLE Logs (
                Id INT AUTO_INCREMENT PRIMARY KEY,
                Fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
                Funcion VARCHAR(100) NOT NULL,
                codMensaje INT NOT NULL,
                Servicio VARCHAR(100) NOT NULL,
                Descripcion TEXT
            )
        """))
        conn.commit()

def down():
    """Drop logs table"""
    with db.engine.connect() as conn:
        conn.execute(db.text("DROP TABLE IF EXISTS Logs"))
        conn.commit()