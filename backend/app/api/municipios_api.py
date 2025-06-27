from flask import Blueprint, jsonify
from app.services.municipios_service import MunicipioService
from app.dtos.municipios_dto import MunicipioSchema
from app.utils.logger import handle_exceptions
from app.utils.auth_middleware import token_required, require_permission

municipios_bp = Blueprint('municipios_bp', __name__)

muni_schema   = MunicipioSchema()
munis_schema  = MunicipioSchema(many=True)

@municipios_bp.route('/', methods=['GET'])
@token_required
@require_permission('Dashboard', 'read')
@handle_exceptions(servicio='Municipios', cod_mensaje=4001)
def list_municipios(current_user):
    """
    Listar todos los municipios
    ---
    tags:
      - Municipios
    responses:
      200:
        description: Lista de municipios
        schema:
          type: array
          items:
            $ref: '#/definitions/Municipio'
    """
    return munis_schema.jsonify(MunicipioService.list_all()), 200

@municipios_bp.route('/<int:id>', methods=['GET'])
@token_required
@require_permission('Dashboard', 'read')
@handle_exceptions(servicio='Municipios', cod_mensaje=4002)
def get_municipio(current_user, id):
    """
    Obtener municipio por ID
    ---
    tags:
      - Municipios
    parameters:
      - name: id
        in: path
        type: integer
    responses:
      200:
        schema:
          $ref: '#/definitions/Municipio'
      404:
        description: No encontrado
    """
    muni = MunicipioService.get_by_id(id)
    if not muni:
        return jsonify({"error": "No encontrado"}), 404
    return muni_schema.jsonify(muni), 200
