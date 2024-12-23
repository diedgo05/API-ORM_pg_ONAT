from flask import Blueprint, request
from src.controllers.donationsController import crear_donacion, obtener_donacion,obtener_donacionesByID_org

donacion_blueprint = Blueprint('donaciones', __name__, url_prefix="/donaciones")

@donacion_blueprint.route('/realizarDonacion', methods=['POST'])
def crear_donacion_ruta():
    data = request.get_json()
    return crear_donacion(data)

@donacion_blueprint.route('/obtenerDon', methods=['GET'])
def obtener_donaciones_ruta():
    return obtener_donacion()

@donacion_blueprint.route('/org/<int:org_id>', methods=['GET'])
def obtener_donaciones_by_org(org_id):
    return obtener_donacionesByID_org(org_id)

