from functools import wraps
from flask import jsonify
from app.repositories.logs_repo import LogRepo

def log_info(service: str, action: str, message: str, user: str = None):
    """Log info level message"""
    try:
        LogRepo.add(
            funcion=action,
            cod_mensaje=200,  # Success code for info
            servicio=service,
            descripcion=f"[INFO] {message}"
        )
    except Exception as e:
        print(f"Error logging info: {e}")

def log_error(service: str, action: str, message: str, user: str = None):
    """Log error level message"""
    try:
        LogRepo.add(
            funcion=action,
            cod_mensaje=500,  # Error code
            servicio=service,
            descripcion=f"[ERROR] {message}"
        )
    except Exception as e:
        print(f"Error logging error: {e}")

def handle_exceptions(servicio: str, cod_mensaje: int = 500):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapper
    return decorator
