from flask import Blueprint, request
from src.controllers.userController import crear_usuario, crear_usuario_base,login_usuario, obtener_usuario, eliminar_usuario
from flask_jwt_extended import JWTManager

usuario_blueprint = Blueprint('usuarios', __name__)

@usuario_blueprint.route('/users', methods=['POST'])
def crear_usuario_ruta():
    data = request.get_json()
    return crear_usuario(data)

@usuario_blueprint.route('/user_base', methods=['POST'])
def crear_usuario_base_ruta():
    data = request.get_json()
    return crear_usuario_base(data)

@usuario_blueprint.route('/login', methods=['POST'])
def login_ruta():
    data = request.get_json()
    return login_usuario(data)

@usuario_blueprint.route('/profile', methods=['GET'])
def obtener_usuario_ruta():
    return obtener_usuario()

@usuario_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
def eliminar_usuario_ruta(user_id):
    return eliminar_usuario(user_id)
