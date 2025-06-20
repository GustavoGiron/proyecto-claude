from app.database import db

def up():
    """Add FechaCreacion column to Clientes table"""
    with db.engine.connect() as conn:
        # Agregar columna FechaCreacion a la tabla Clientes
        conn.execute(db.text("""
            ALTER TABLE Clientes 
            ADD COLUMN FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP
        """))
        
        conn.commit()

def down():
    """Remove FechaCreacion column from Clientes table"""
    with db.engine.connect() as conn:
        # Remover columna FechaCreacion de la tabla Clientes
        conn.execute(db.text("""
            ALTER TABLE Clientes 
            DROP COLUMN FechaCreacion
        """))
        
        conn.commit() 