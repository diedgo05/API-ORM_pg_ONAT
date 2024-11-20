from flask import Flask, request
from flask_jwt_extended import JWTManager
from config import config
from src.routes.organizationsRoutes import organizacion_blueprint
from src.routes.donationsRoutes import donacion_blueprint
from src.routes.membershipRoutes import membresias_blueprint
from src.routes.dipomexRoutes import dipomex_blueprint
from src.routes.driveRoutes import drive_bp
from src.models import db
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(config['development'])
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app)

    app.register_blueprint(donacion_blueprint)
    app.register_blueprint(organizacion_blueprint)
    app.register_blueprint(membresias_blueprint)
    app.register_blueprint(dipomex_blueprint)
    app.register_blueprint(drive_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)

    