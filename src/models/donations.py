from flask_bcrypt import Bcrypt
from sqlalchemy.orm import relationship
from sqlalchemy import Enum
import enum
from src.models import db
from dotenv import load_dotenv
import os
from sqlalchemy import ForeignKey

bcrypt = Bcrypt()
load_dotenv()

class TipoDonacion(enum.Enum):
    unica = "unica"
    membresia = "membresia"

class Donations(db.Model):
    schema_name = os.getenv('SCHEMA_NAME')
    __tablename__ = 'donations'
    __table_args__ = {'schema': schema_name}

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido_m = db.Column(db.String(50), nullable=False)
    apellido_p = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(50), nullable=False, unique=True)
    nacionalidad = db.Column(db.String(50), nullable=False)
    cantidad = db.Column(db.Numeric(10, 2), nullable=False)
    tipo_donacion = db.Column(Enum(TipoDonacion), nullable=False)
    id_membresia = db.Column(db.Integer, ForeignKey(f'{schema_name}.membresia.id'), nullable=True)
    id_org = db.Column(db.Integer, ForeignKey(f'{schema_name}.organizations.id'), nullable=False)

    membresia = relationship('Membership', backref='donations', lazy=True)
    organization = relationship('Organizations', backref='donations', lazy=True)

    def __init__(self, nombre, apellido_m, apellido_p, correo, nacionalidad, cantidad, tipo_donacion, id_org, id_membresia=None):
        self.nombre = nombre
        self.apellido_m = apellido_m
        self.apellido_p = apellido_p
        self.correo = correo
        self.nacionalidad = nacionalidad
        self.cantidad = cantidad
        self.tipo_donacion = tipo_donacion
        self.id_org = id_org
        self.id_membresia = id_membresia

    def __repr__(self):
        return f'<Donations {self.nombre} {self.apellido_p}>'