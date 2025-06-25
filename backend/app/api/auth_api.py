from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app.services.auth_service import AuthService
from app.dtos.auth_dto import (
    LoginRequestSchema, 
    RefreshTokenRequestSchema,
    LoginResponseSchema,
    TokenResponseSchema,
    PermissionsResponseSchema
)
from app.utils.auth_middleware import token_required


auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()


@auth_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Autenticación'],
    'description': 'Iniciar sesión',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': LoginRequestSchema
    }],
    'responses': {
        200: {
            'description': 'Login exitoso',
            'schema': LoginResponseSchema
        },
        401: {
            'description': 'Credenciales inválidas'
        }
    }
})
def login():
    try:
        schema = LoginRequestSchema()
        data = schema.load(request.json)
        
        result, error = auth_service.login(data['username'], data['password'])
        
        if error:
            return jsonify({'error': error}), 401
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': 'Datos inválidos', 'details': str(e)}), 400


@auth_bp.route('/refresh', methods=['POST'])
@swag_from({
    'tags': ['Autenticación'],
    'description': 'Refrescar token de acceso',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': RefreshTokenRequestSchema
    }],
    'responses': {
        200: {
            'description': 'Token refrescado exitosamente',
            'schema': TokenResponseSchema
        },
        401: {
            'description': 'Token inválido o expirado'
        }
    }
})
def refresh_token():
    try:
        schema = RefreshTokenRequestSchema()
        data = schema.load(request.json)
        
        result, error = auth_service.refresh_access_token(data['refresh_token'])
        
        if error:
            return jsonify({'error': error}), 401
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': 'Datos inválidos', 'details': str(e)}), 400


@auth_bp.route('/me', methods=['GET'])
@swag_from({
    'tags': ['Autenticación'],
    'description': 'Obtener información del usuario actual',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Información del usuario',
            'schema': {
                'type': 'object',
                'properties': {
                    'user': {'$ref': '#/definitions/UserResponse'}
                }
            }
        },
        401: {
            'description': 'No autorizado'
        }
    }
})
@token_required
def get_current_user(current_user):
    return jsonify({'user': current_user.to_dict()}), 200


@auth_bp.route('/permissions', methods=['GET'])
@swag_from({
    'tags': ['Autenticación'],
    'description': 'Obtener permisos del usuario actual',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Permisos del usuario',
            'schema': PermissionsResponseSchema
        },
        401: {
            'description': 'No autorizado'
        }
    }
})
@token_required
def get_user_permissions(current_user):
    permissions, error = auth_service.get_user_permissions(current_user.id)
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify(permissions), 200


@auth_bp.route('/logout', methods=['POST'])
@swag_from({
    'tags': ['Autenticación'],
    'description': 'Cerrar sesión',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Sesión cerrada exitosamente'
        },
        401: {
            'description': 'No autorizado'
        }
    }
})
@token_required
def logout(current_user):
    return jsonify({'message': 'Sesión cerrada exitosamente'}), 200