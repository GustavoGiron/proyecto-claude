from app.database import db

def up():
    """Add Estado column to Clientes table"""
    with db.engine.connect() as conn:
        # Agregar columna Estado a la tabla Clientes
        conn.execute(db.text("""
            ALTER TABLE Clientes 
            ADD COLUMN Estado BOOLEAN DEFAULT TRUE
        """))
        
        conn.commit()

def down():
    """Remove Estado column from Clientes table"""
    with db.engine.connect() as conn:
        # Remover columna Estado de la tabla Clientes
        conn.execute(db.text("""
            ALTER TABLE Clientes 
            DROP COLUMN Estado
        """))
        
        conn.commit() 