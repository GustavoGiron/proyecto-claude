import jwt
from datetime import datetime, timedelta
from flask import current_app
from app.repositories.usuarios_repo import UsuariosRepository
from app.utils.logger import log_info, log_error


class AuthService:
    def __init__(self):
        self.usuarios_repo = UsuariosRepository()
    
    def login(self, username, password):
        try:
            usuario = self.usuarios_repo.get_by_username(username)
            if not usuario:
                log_info("auth", "login", f"Intento de login fallido - Usuario no encontrado: {username}")
                return None, "Usuario o contraseña incorrectos"
            
            if not usuario.is_active:
                log_info("auth", "login", f"Intento de login fallido - Usuario inactivo: {username}")
                return None, "Usuario inactivo"
            
            if not usuario.check_password(password):
                log_info("auth", "login", f"Intento de login fallido - Contraseña incorrecta: {username}")
                return None, "Usuario o contraseña incorrectos"
            
            self.usuarios_repo.update_last_login(usuario.id)
            
            access_token = self.generate_access_token(usuario)
            refresh_token = self.generate_refresh_token(usuario)
            
            log_info("auth", "login", f"Login exitoso: {username}")
            
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': usuario.to_dict()
            }, None
            
        except Exception as e:
            log_error("auth", "login", f"Error en login: {str(e)}")
            return None, "Error al procesar la solicitud"
    
    def generate_access_token(self, usuario):
        payload = {
            'user_id': usuario.id,
            'username': usuario.username,
            'role_id': usuario.role_id,
            'role': usuario.role.nombre if usuario.role else None,
            'exp': datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES'],
            'iat': datetime.utcnow(),
            'type': 'access'
        }
        
        return jwt.encode(
            payload,
            current_app.config['JWT_SECRET_KEY'],
            algorithm=current_app.config['JWT_ALGORITHM']
        )
    
    def generate_refresh_token(self, usuario):
        payload = {
            'user_id': usuario.id,
            'exp': datetime.utcnow() + current_app.config['JWT_REFRESH_TOKEN_EXPIRES'],
            'iat': datetime.utcnow(),
            'type': 'refresh'
        }
        
        return jwt.encode(
            payload,
            current_app.config['JWT_SECRET_KEY'],
            algorithm=current_app.config['JWT_ALGORITHM']
        )
    
    def verify_token(self, token):
        try:
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=[current_app.config['JWT_ALGORITHM']]
            )
            return payload, None
        except jwt.ExpiredSignatureError:
            return None, "Token expirado"
        except jwt.InvalidTokenError:
            return None, "Token inválido"
    
    def refresh_access_token(self, refresh_token):
        try:
            payload, error = self.verify_token(refresh_token)
            
            if error:
                return None, error
            
            if payload.get('type') != 'refresh':
                return None, "Token inválido"
            
            usuario = self.usuarios_repo.get_by_id(payload['user_id'])
            
            if not usuario or not usuario.is_active:
                return None, "Usuario no válido"
            
            access_token = self.generate_access_token(usuario)
            
            return {'access_token': access_token}, None
            
        except Exception as e:
            log_error("auth", "refresh_token", f"Error al refrescar token: {str(e)}")
            return None, "Error al procesar la solicitud"
    
    def get_user_permissions(self, user_id):
        try:
            usuario = self.usuarios_repo.get_by_id(user_id)
            
            if not usuario:
                return None, "Usuario no encontrado"
            
            permissions = {
                'role': usuario.role.nombre if usuario.role else None,
                'modules': [],
                'permissions': []
            }
            
            if usuario.role:
                for rm in usuario.role.role_modules:
                    permissions['modules'].append({
                        'id': rm.module.id,
                        'nombre': rm.module.nombre,
                        'ruta': rm.module.ruta,
                        'icono': rm.module.icono
                    })
                
                permissions['permissions'] = self.usuarios_repo.get_user_permissions(user_id)
            
            return permissions, None
            
        except Exception as e:
            log_error("auth", "get_permissions", f"Error al obtener permisos: {str(e)}")
            return None, "Error al procesar la solicitud"
        
    
    def get_user_role(self, role_id):
        try:
            usuario = self.usuarios_repo.get_by_role_id(role_id)
            
            if not usuario or not usuario.role:
                return None, "Usuario o rol no encontrado"
            
            role_info = {
                'id': usuario.role.id,
                'nombre': usuario.role.nombre,
                'email': usuario.email,
                'descripcion': usuario.role.descripcion
            }
            
            return role_info, None
            
        except Exception as e:
            log_error("auth", "get_user_role", f"Error al obtener rol del usuario: {str(e)}")
            return None, "Error al procesar la solicitud"