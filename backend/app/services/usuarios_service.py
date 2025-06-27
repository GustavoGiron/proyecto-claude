from app.repositories.usuarios_repo import UsuariosRepository

class UsuariosService:
    def __init__(self):
        self.repo = UsuariosRepository()

    def obtener_todos(self):
        return self.repo.get_all()

    def obtener_por_id(self, usuario_id):
        return self.repo.get_by_id(usuario_id)

    def crear_usuario(self, data):
        if self.repo.get_by_username(data['username']):
            raise ValueError("El nombre de usuario ya existe.")
        if self.repo.get_by_email(data['email']):
            raise ValueError("El correo ya está registrado.")
        return self.repo.create(data)

    def actualizar_usuario(self, usuario_id, data):
        usuario = self.repo.get_by_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado.")
        usuario.nombre = data.get('nombre', usuario.nombre)
        usuario.apellido = data.get('apellido', usuario.apellido)
        usuario.email = data.get('email', usuario.email)
        usuario.role_id = data.get('role_id', usuario.role_id)

        if 'password' in data and data['password']:
            usuario.set_password(data['password'])

        return self.repo.update(usuario_id, data)

    def eliminar_usuario(self, usuario_id):
        usuario = self.repo.get_by_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado.")
        return self.repo.delete(usuario_id)

