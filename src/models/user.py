from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from dotenv import load_dotenv
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
load_dotenv()

class User(db.Model):
    schema_name = os.getenv('SCHEMA_NAME')
    __tablename__ = 'user'
    __table_args__ = {'schema': schema_name} 
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, nombre, email, password):
        self.nombre = nombre
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.nombre}>'
