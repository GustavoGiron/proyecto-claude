#!/usr/bin/env python3
from flask import Flask
from app.config import Config
from app.database import db

def check_tables():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    with app.app_context():
        with db.engine.connect() as conn:
            result = conn.execute(db.text("SHOW TABLES"))
            tables = [row[0] for row in result]
            
            print("\n📊 Database Tables:")
            print("-" * 30)
            for table in sorted(tables):
                print(f"  • {table}")
            
            # Check auth tables specifically
            auth_tables = ['roles', 'usuarios', 'modules', 'permissions', 'role_modules', 'role_permissions']
            auth_present = [t for t in auth_tables if t in tables]
            
            print(f"\n✅ Auth tables created: {len(auth_present)}/{len(auth_tables)}")
            if len(auth_present) < len(auth_tables):
                missing = set(auth_tables) - set(auth_present)
                print(f"❌ Missing tables: {', '.join(missing)}")

if __name__ == "__main__":
    check_tables()