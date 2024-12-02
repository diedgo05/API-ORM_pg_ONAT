from flask import Blueprint, request
from src.controllers.organizationController import crear_org, obtener_organizaciones, login_organizacion, actualizar_organizaciones, eliminar_organizacion, validarToken, obtener_organizacion_por_id

organizacion_blueprint = Blueprint('organizaciones', __name__, url_prefix="/organizaciones")

@organizacion_blueprint.route('/crear_org', methods=['POST'])
def crear_organizacion_ruta():
    return crear_org()

@organizacion_blueprint.route('/obtenerOrgPorId/<string:id>', methods=['Post'])
def obtener_organizacion_por_id():
     return  obtener_organizacion_por_id(id)
    
@organizacion_blueprint.route('/obtenerOrg', methods=['GET'])
def obtener_organizaciones_ruta():
    return obtener_organizaciones()
@organizacion_blueprint.route('/login', methods=['POST'])
def login_organizacion_ruta():
    data = request.get_json()
    return login_organizacion(data)
@organizacion_blueprint.route('/editarOrg/<int:id>', methods=['PUT'])
def actualizar_organizaciones_ruta(id):
    data = request.get_json()
    return actualizar_organizaciones(id, data)
@organizacion_blueprint.route('/eliminarOrg/<int:id>', methods=['DELETE'])
def eliminar_organizaciones_ruta(id):
    return eliminar_organizacion(id)

@organizacion_blueprint.route('/validar-token/', methods=['POST'])
def validar_token():
    return validarToken()