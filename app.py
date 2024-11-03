from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import config
from src.routes.organizationsRoutes import organizacion_blueprint
from src.models.organizations import db
from src.models.donations import db
from src.routes.donationsRoutes import donacion_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object(config['development'])
    db.init_app(app)
    jwt = JWTManager(app)

    app.register_blueprint(donacion_blueprint)
    app.register_blueprint(organizacion_blueprint)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)