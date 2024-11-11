from flask import Blueprint, request
from src.controllers.organizationController import crear_org, obtener_organizaciones, login_organizacion, actualizar_organizaciones, eliminar_organizacion

organizacion_blueprint = Blueprint('organizaciones', __name__)

# Modificación de esta ruta para poder guardar imagenes
@organizacion_blueprint.route('/crear_org', methods=['POST'])
def crear_organizacion_ruta():
    return crear_org()

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