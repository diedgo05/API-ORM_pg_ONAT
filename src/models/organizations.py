from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

db  = SQLAlchemy()
bcrypt = Bcrypt()
load_dotenv()

class Organizations(db.Model):
    schema_name = os.getenv('SCHEMA_NAME')
    __tablename__ = 'organizations'
    __table_args__ = { 'schema': schema_name}
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50), nullable = False, unique = True)
    correo = db.Column(db.String(50), nullable = False, unique = True)
    estado = db.Column(db.String(50), nullable = False)
    direccion = db.Column(db.String(100), nullable = False)
    rfc = db.Column(db.String(13), nullable = False, unique = True)
    telefono = db.Column(db.String(10), nullable = False, unique = True)
    contraseña = db.Column(db.String(200), nullable = False, unique = True)
    imagen = db.Column(db.LargeBinary, nullable = False)

    def __init__(self,nombre,correo,estado,rfc,telefono,contraseña,imagen,direccion):
        self.nombre = nombre
        self.correo = correo
        self.estado = estado
        self.rfc = rfc
        self.telefono = telefono
        self.imagen = imagen
        self.direccion = direccion
        self.contraseña = bcrypt.generate_password_hash(contraseña).decode('utf-8')

    def check_contraseña(self,contraseña):
        return bcrypt.check_password_hash(self.contraseña, contraseña)
    
    def __repr__(self):
        return f'<Organizations {self.nombre}'