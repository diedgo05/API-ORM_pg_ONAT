from flask_bcrypt import Bcrypt
from sqlalchemy.orm import relationship
from src.models import db
from dotenv import load_dotenv
import os
from sqlalchemy import ForeignKey
from sqlalchemy.orm import validates

bcrypt = Bcrypt()
load_dotenv()

class Card(db.Model):
    schema_name = os.getenv('SCHEMA_NAME')
    __tablename__ = 'tarjeta'
    __table_args__ = {'schema': schema_name}

    id = db.Column(db.Integer, primary_key=True)
    numero_tarjeta = db.Column(db.String(16), nullable=False)
    cvv = db.Column(db.String(3), nullable=False)
    fecha_expiracion = db.Column(db.Date, nullable=False)
    id_donacion = db.Column(db.Integer, ForeignKey(f'{schema_name}.donations.id'), nullable=False)

    donacion = relationship('Donations', backref='tarjeta', lazy=True)

    def __init__(self,numero_tarjeta,cvv,fecha_expiracion,id_donacion):
        self.numero_tarjeta = numero_tarjeta
        self.cvv = cvv
        self.fecha_expiracion = fecha_expiracion
        self.id_donacion = id_donacion

    def __repr__(self):
        return f'Card {self.numero_tarjeta}'