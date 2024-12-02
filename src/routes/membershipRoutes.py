from flask import Blueprint, request
from src.controllers.membershipController import crear_membresia,obtener_membresias, obtener_membresia_byID

membresias_blueprint = Blueprint('membresias', __name__, url_prefix="/membresias")

@membresias_blueprint.route('/addM', methods=['POST'])
def crear_membresia_ruta():
    data = request.get_json()
    return crear_membresia(data)

@membresias_blueprint.route('/getM', methods=['GET'])
def obtener_membresias_ruta():
    return obtener_membresias()

@membresias_blueprint.route('/getM/<int:id>', methods=['GET'])
def obtener_membresia_byID_ruta(id):
    return obtener_membresia_byID(id)
