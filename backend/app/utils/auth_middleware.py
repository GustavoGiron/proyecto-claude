from functools import wraps
from flask import request, jsonify, current_app
import jwt
from app.repositories.usuarios_repo import UsuariosRepository


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'error': 'Token malformado'}), 401
        
        if not token:
            return jsonify({'error': 'Token faltante'}), 401
        
        try:
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=[current_app.config['JWT_ALGORITHM']]
            )
            
            if payload.get('type') != 'access':
                return jsonify({'error': 'Token inválido'}), 401
            
            usuarios_repo = UsuariosRepository()
            current_user = usuarios_repo.get_by_id(payload['user_id'])
            
            if not current_user:
                return jsonify({'error': 'Usuario no encontrado'}), 401
            
            if not current_user.is_active:
                return jsonify({'error': 'Usuario inactivo'}), 401
            
            return f(current_user, *args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401
        except Exception as e:
            return jsonify({'error': 'Error al procesar token'}), 401
    
    return decorated


def require_permission(module, action):
    def decorator(f):
        @wraps(f)
        def decorated(current_user, *args, **kwargs):
            usuarios_repo = UsuariosRepository()
            permissions = usuarios_repo.get_user_permissions(current_user.id)
            
            has_permission = any(
                p['module'] == module and p['action'] == action 
                for p in permissions
            )
            
            if not has_permission:
                return jsonify({
                    'error': 'Sin permisos para esta acción',
                    'required': f'{module}:{action}'
                }), 403
            
            return f(current_user, *args, **kwargs)
        
        return decorated
    return decorator


def require_role(role_name):
    def decorator(f):
        @wraps(f)
        def decorated(current_user, *args, **kwargs):
            if not current_user.role or current_user.role.nombre != role_name:
                return jsonify({
                    'error': 'Rol insuficiente',
                    'required_role': role_name
                }), 403
            
            return f(current_user, *args, **kwargs)
        
        return decorated
    return decorator


def require_any_role(role_names):
    def decorator(f):
        @wraps(f)
        def decorated(current_user, *args, **kwargs):
            if not current_user.role or current_user.role.nombre not in role_names:
                return jsonify({
                    'error': 'Rol insuficiente',
                    'required_roles': role_names
                }), 403
            
            return f(current_user, *args, **kwargs)
        
        return decorated
    return decorator