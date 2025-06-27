# app/api/usuarios_api.py
from flask import Blueprint, request, jsonify
from app.services.usuarios_service import UsuariosService
from app.dtos.usuario_dto import usuario_input_dto, usuario_output_dto

usuarios_bp = Blueprint('usuarios_bp', __name__)
service = UsuariosService()

@usuarios_bp.route('/', methods=['GET'])
def listar_usuarios():
    usuarios = service.obtener_todos()
    return jsonify([usuario_output_dto(u) for u in usuarios]), 200

@usuarios_bp.route('/<int:usuario_id>', methods=['GET'])
def obtener_usuario(usuario_id):
    usuario = service.obtener_por_id(usuario_id)
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify(usuario_output_dto(usuario)), 200

@usuarios_bp.route('/', methods=['POST'])
def crear_usuario():
    data = usuario_input_dto(request.get_json())
    try:
        usuario = service.crear_usuario(data)
        return jsonify(usuario_output_dto(usuario)), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@usuarios_bp.route('/<int:usuario_id>', methods=['PUT'])
def actualizar_usuario(usuario_id):
    data = request.get_json()
    try:
        usuario = service.actualizar_usuario(usuario_id, data)
        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        return jsonify(usuario_output_dto(usuario)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@usuarios_bp.route('/<int:usuario_id>', methods=['DELETE'])
def eliminar_usuario(usuario_id):
    try:
        resultado = service.eliminar_usuario(usuario_id)
        return jsonify({'success': resultado}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
