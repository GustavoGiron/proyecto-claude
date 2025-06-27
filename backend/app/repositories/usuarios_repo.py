from datetime import datetime
from app.database import db
from app.models.usuarios_model import Usuario
from app.utils.logger import log_info, log_error


class UsuariosRepository:
    def get_all(self):
        try:
            return Usuario.query.all()
        except Exception as e:
            log_error("usuarios", "get_all", f"Error al obtener usuarios: {str(e)}")
            return []
    
    def get_by_id(self, usuario_id):
        try:
            return Usuario.query.get(usuario_id)
        except Exception as e:
            log_error("usuarios", "get_by_id", f"Error al obtener usuario por ID: {str(e)}")
            return None

    def get_by_role_id(self, role_id):
        try:
            usuarios = Usuario.query.filter_by(role_id=role_id, is_active=True).all()
            return usuarios
        except Exception as e:
            log_error("usuarios", "get_by_role_id", f"Error al obtener usuarios por rol: {str(e)}")
            return []     
   
    def get_by_username(self, username):
        return Usuario.query.filter_by(username=username).first()

    def get_by_email(self, email):
        try:
            return Usuario.query.filter_by(email=email).first()
        except Exception as e:
            log_error("usuarios", "get_by_email", f"Error al obtener usuario por email: {str(e)}")
            return None
    
    def create(self, data):
        try:
            usuario = Usuario(
                username=data['username'],
                email=data['email'],
                nombre=data['nombre'],
                apellido=data['apellido'],
                role_id=data['role_id']
            )
            usuario.set_password(data['password'])
            
            db.session.add(usuario)
            db.session.commit()
            
            log_info("usuarios", "create", f"Usuario creado: {usuario.username}")
            return usuario
            
        except Exception as e:
            db.session.rollback()
            log_error("usuarios", "create", f"Error al crear usuario: {str(e)}")
            return None
    
    def update(self, usuario_id, data):
        try:
            usuario = self.get_by_id(usuario_id)
            if not usuario:
                return None
            
            if 'email' in data:
                usuario.email = data['email']
            if 'nombre' in data:
                usuario.nombre = data['nombre']
            if 'apellido' in data:
                usuario.apellido = data['apellido']
            if 'role_id' in data:
                usuario.role_id = data['role_id']
            if 'is_active' in data:
                usuario.is_active = data['is_active']
            if 'password' in data and data['password']:
                usuario.set_password(data['password'])
            
            db.session.commit()
            log_info("usuarios", "update", f"Usuario actualizado: {usuario.username}")
            return usuario
            
        except Exception as e:
            db.session.rollback()
            log_error("usuarios", "update", f"Error al actualizar usuario: {str(e)}")
            return None
    
    def delete(self, usuario_id):
        try:
            usuario = self.get_by_id(usuario_id)
            if not usuario:
                return False
            
            usuario.is_active = False
            db.session.commit()
            
            log_info("usuarios", "delete", f"Usuario desactivado: {usuario.username}")
            return True
            
        except Exception as e:
            db.session.rollback()
            log_error("usuarios", "delete", f"Error al desactivar usuario: {str(e)}")
            return False
    
    def update_last_login(self, usuario_id):
        try:
            usuario = self.get_by_id(usuario_id)
            if usuario:
                usuario.ultima_sesion = datetime.utcnow()
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            log_error("usuarios", "update_last_login", f"Error al actualizar última sesión: {str(e)}")
            return False
    
    def get_user_permissions(self, usuario_id):
        try:
            usuario = self.get_by_id(usuario_id)
            if not usuario or not usuario.role:
                return []
            
            permissions = []
            
            for rp in usuario.role.role_permissions:
                if rp.permission and rp.permission.is_active:
                    permissions.append({
                        'module': rp.permission.module.nombre,
                        'action': rp.permission.accion,
                        'permission': rp.permission.nombre
                    })
            
            for rm in usuario.role.role_modules:
                for perm in rm.module.permissions:
                    if perm.is_active:
                        permissions.append({
                            'module': rm.module.nombre,
                            'action': perm.accion,
                            'permission': perm.nombre
                        })
            
            unique_permissions = []
            seen = set()
            for perm in permissions:
                key = f"{perm['module']}_{perm['action']}"
                if key not in seen:
                    seen.add(key)
                    unique_permissions.append(perm)
            
            return unique_permissions
            
        except Exception as e:
            log_error("usuarios", "get_user_permissions", f"Error al obtener permisos del usuario: {str(e)}")
            return []
        

    def get_user_role(self, role_id):
        try:
            usuario = self.get_by_role_id(role_id)
            if usuario and usuario.role:
                return {
                    'id': usuario.role.id,
                    'nombre': usuario.role.nombre,
                    'email': usuario.email,
                    'descripcion': usuario.role.descripcion
                }
            return None
        except Exception as e:
            log_error("usuarios", "get_user_role", f"Error al obtener rol del usuario: {str(e)}")
            return None