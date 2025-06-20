from functools import wraps
from flask import jsonify
from app.repositories.logs_repo import LogRepo

def handle_exceptions(servicio: str, cod_mensaje: int = 500):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapper
    return decorator
