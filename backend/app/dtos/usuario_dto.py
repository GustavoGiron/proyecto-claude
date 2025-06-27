# app/dtos/usuarios_dto.py

def usuario_input_dto(data):
    return {
        'username': data.get('username'),
        'email': data.get('email'),
        'password': data.get('password'),
        'nombre': data.get('nombre'),
        'apellido': data.get('apellido'),
        'role_id': data.get('role_id')
    }

def usuario_output_dto(usuario):
    return usuario.to_dict() if usuario else None
