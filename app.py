from flask import Flask, request
from flask_jwt_extended import JWTManager
from config import config
from src.routes.organizationsRoutes import organizacion_blueprint
from src.routes.donationsRoutes import donacion_blueprint
from src.routes.membershipRoutes import membresias_blueprint
from src.routes.dipomexRoutes import dipomex_blueprint
from src.routes.driveRoutes import drive_bp
from src.models import db
from flask import Flask
from flask_cors import CORS
from datetime import timedelta

from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(config['development'])

    db.init_app(app)
    jwt = JWTManager(app)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)  # Duración de 2 horas

    # Habilitar CORS para todos los recursos
    CORS(app, resources={
    r"/*": {
        "origins": "http://localhost:4200",
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})


    # Manejo explícito de solicitudes OPTIONS (preflight) si es necesario
    @app.after_request
    def after_request(response):
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:4200'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    app.register_blueprint(organizacion_blueprint)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
