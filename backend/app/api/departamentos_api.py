from flask import Blueprint, jsonify
from app.services.departamentos_service import DepartamentoService
from app.dtos.departamentos_dto import DepartamentoSchema
from app.dtos.municipios_dto import MunicipioSchema
from app.utils.logger import handle_exceptions

departamentos_bp = Blueprint('departamentos_bp', __name__)
dep_schema       = DepartamentoSchema()
deps_schema      = DepartamentoSchema(many=True)
munis_schema     = MunicipioSchema(many=True)

@departamentos_bp.route('/', methods=['GET'])
@handle_exceptions(servicio='Departamentos', cod_mensaje=3001)
def list_departamentos():
    """
    Listar departamentos
    ---
    tags:
      - Departamentos
    responses:
      200:
        description: Lista de departamentos
        schema:
          type: array
          items:
            $ref: '#/definitions/Departamento'
    """
    return deps_schema.jsonify(DepartamentoService.list_all()), 200

@departamentos_bp.route('/<int:id>', methods=['GET'])
@handle_exceptions(servicio='Departamentos', cod_mensaje=3002)
def get_departamento(id):
    """
    Obtener departamento por ID
    ---
    tags:
      - Departamentos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        schema:
          $ref: '#/definitions/Departamento'
      404:
        description: No encontrado
    """
    dep = DepartamentoService.get_by_id(id)
    if not dep:
        return jsonify({"error": "No encontrado"}), 404
    return dep_schema.jsonify(dep), 200

@departamentos_bp.route('/<int:id>/municipios', methods=['GET'])
@handle_exceptions(servicio='Departamentos', cod_mensaje=3003)
def get_municipios_por_departamento(id):
    """
    Listar municipios de un departamento
    ---
    tags:
      - Departamentos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Lista de municipios
        schema:
          type: array
          items:
            $ref: '#/definitions/Municipio'
    """
    return munis_schema.jsonify(DepartamentoService.get_municipios(id)), 200
