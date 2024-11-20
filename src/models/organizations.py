from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from src.models import db
from dotenv import load_dotenv
import os
from sqlalchemy.orm import validates
import re

bcrypt = Bcrypt()
load_dotenv()

class Organizations(db.Model):
    schema_name = os.getenv('SCHEMA_NAME')
    __tablename__ = 'organizations'
    __table_args__ = {'schema': schema_name}
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    correo = db.Column(db.String(50), nullable=False, unique=True)
    
    cp = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    municipio = db.Column(db.String(50), nullable=False)  
    colonia = db.Column(db.String(50), nullable=False)
    
    direccion = db.Column(db.String(100), nullable=False)
    rfc = db.Column(db.String(13), nullable=False, unique=True)
    telefono = db.Column(db.String(10), nullable=False, unique=True)
    contrasena = db.Column(db.String(200), nullable=False, unique=True)
    imagen = db.Column(db.String(100))
    
    # Valida que "correo" utilice @ 
    @validates('correo')
    def validate_correo(self,key,correo):
        if not correo or  '@' not in correo:
            raise ValueError('El correo ingresado no es válido.')
        return correo
    
    # Valida que "rfc" tenga 13 dígitos y convierte las letras a mayúsculas
    @validates('rfc')
    def validate_rfc(self, key, rfc):
        if not re.match(r'^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$', rfc.upper()):
            raise ValueError("El RFC proporcionado no es válido.")
        return rfc.upper()
    
    # Valida que "telefono" solo tenga 10 dígitos
    @validates('telefono')
    def validate_telefono(self, key, telefono):
        if not re.match(r'^\d{10}$', telefono):
            raise ValueError("El teléfono debe contener exactamente 10 dígitos.")
        return telefono

    def __init__(self, nombre, correo, cp, estado, municipio, colonia, rfc, telefono, contrasena, imagen, direccion):
        self.nombre = nombre
        self.correo = correo
        self.cp = cp
        self.estado = estado
        self.municipio = municipio
        self.colonia = colonia
        self.rfc = rfc
        self.telefono = telefono
        self.imagen = imagen
        self.direccion = direccion
        self.contrasena = bcrypt.generate_password_hash(contrasena).decode('utf-8')

    def check_contrasena(self, contrasena):
        return bcrypt.check_password_hash(self.contrasena, contrasena)
    
    def __repr__(self):
        return f'<Organizations {self.nombre}>'
