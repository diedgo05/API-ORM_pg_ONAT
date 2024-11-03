from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

from sqlalchemy import ForeignKey

db  = SQLAlchemy()
bcrypt = Bcrypt()
load_dotenv()

class Donations(db.Model):
    schema_name = os.getenv('SCHEMA_NAME')
    __tablename__ = 'donations'
    __table_args__ = { 'schema': schema_name}
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50), nullable = False, unique = True)
    apellido_m = db.Column(db.String(50), nullable = False,)
    apellido_p = db.Column(db.String(50), nullable = False,)    
    correo = db.Column(db.String(50), nullable = False, unique = True)
    nacionalidad = db.Column(db.String(50), nullable = False)
    cantidad = db.Column(db.Float, nullable = False)
    id_org = db.Column(db.Integer, ForeignKey('organizations.id'))

    def __init__(self, nombre, apellido_m, apellido_p, correo, nacionalidad, cantidad, id_org):
        self.nombre = nombre
        self.apellido_m = apellido_m
        self.apellido_p = apellido_p
        self.correo = correo
        self.nacionalidad = nacionalidad
        self.cantidad = cantidad
        self.id_org = id_org

    def __repr__(self):
        return f'<Donations {self.nombre} {self.apellido_p}>'
