#!/usr/bin/env python3
import os
import sys
import importlib.util
from flask import Flask
from app.config import Config
from app.database import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app

def get_migrations():
    """Get all migration files in order"""
    migrations_dir = os.path.join(os.path.dirname(__file__), 'migrations')
    migration_files = []
    
    for filename in os.listdir(migrations_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            migration_files.append(filename)
    
    return sorted(migration_files)

def load_migration(migration_file):
    """Load a migration module"""
    migrations_dir = os.path.join(os.path.dirname(__file__), 'migrations')
    file_path = os.path.join(migrations_dir, migration_file)
    
    spec = importlib.util.spec_from_file_location(migration_file[:-3], file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    return module

def create_migration_table():
    """Create table to track migrations"""
    try:
        with db.engine.connect() as conn:
            conn.execute(db.text("""
                CREATE TABLE IF NOT EXISTS migrations (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    migration_name VARCHAR(255) NOT NULL UNIQUE,
                    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
        print("✓ Migration tracking table created")
    except Exception as e:
        print(f"Error creating migration table: {e}")

def get_applied_migrations():
    """Get list of applied migrations"""
    try:
        with db.engine.connect() as conn:
            result = conn.execute(db.text("SELECT migration_name FROM migrations ORDER BY id"))
            return [row[0] for row in result]
    except:
        return []

def mark_migration_applied(migration_name):
    """Mark migration as applied"""
    with db.engine.connect() as conn:
        conn.execute(
            db.text("INSERT INTO migrations (migration_name) VALUES (:name)"),
            {"name": migration_name}
        )
        conn.commit()

def run_migrations():
    """Run pending migrations"""
    app = create_app()
    
    with app.app_context():
        print("🚀 Starting database migration...")
        
        # Create migration tracking table
        create_migration_table()
        
        # Get all migrations and applied ones
        all_migrations = get_migrations()
        applied_migrations = get_applied_migrations()
        
        pending_migrations = [m for m in all_migrations if m not in applied_migrations]
        
        if not pending_migrations:
            print("✅ No pending migrations")
            return
        
        print(f"📋 Found {len(pending_migrations)} pending migrations")
        
        for migration_file in pending_migrations:
            try:
                print(f"⚡ Running migration: {migration_file}")
                migration_module = load_migration(migration_file)
                
                if hasattr(migration_module, 'up'):
                    migration_module.up()
                    mark_migration_applied(migration_file)
                    print(f"✅ Migration {migration_file} completed")
                else:
                    print(f"❌ Migration {migration_file} has no 'up' function")
                    
            except Exception as e:
                print(f"❌ Error running migration {migration_file}: {e}")
                break
        
        print("🎉 Database migration completed!")

def rollback_migration(migration_name=None):
    """Rollback the last migration or specific migration"""
    app = create_app()
    
    with app.app_context():
        applied_migrations = get_applied_migrations()
        
        if not applied_migrations:
            print("No migrations to rollback")
            return
        
        target_migration = migration_name or applied_migrations[-1]
        
        if target_migration not in applied_migrations:
            print(f"Migration {target_migration} is not applied")
            return
        
        try:
            print(f"⏪ Rolling back migration: {target_migration}")
            migration_module = load_migration(target_migration)
            
            if hasattr(migration_module, 'down'):
                migration_module.down()
                with db.engine.connect() as conn:
                    conn.execute(
                        db.text("DELETE FROM migrations WHERE migration_name = :name"),
                        {"name": target_migration}
                    )
                    conn.commit()
                print(f"✅ Migration {target_migration} rolled back")
            else:
                print(f"❌ Migration {target_migration} has no 'down' function")
                
        except Exception as e:
            print(f"❌ Error rolling back migration {target_migration}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "migrate":
            run_migrations()
        elif command == "rollback":
            migration_name = sys.argv[2] if len(sys.argv) > 2 else None
            rollback_migration(migration_name)
        else:
            print("Usage: python migrate.py [migrate|rollback] [migration_name]")
    else:
        run_migrations()