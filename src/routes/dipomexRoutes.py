from flask import Blueprint, request
from src.controllers.dipomexController import get_cp

dipomex_blueprint = Blueprint('dipomex', __name__)

@dipomex_blueprint.route('/codigo_postal', methods=['GET'])
def get_cp_ruta():
    return get_cp()