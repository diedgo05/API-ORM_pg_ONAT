from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from src.models import db
from dotenv import load_dotenv
import os
import json
from sqlalchemy.dialects.postgresql import JSONB

bcrypt = Bcrypt()
load_dotenv()

class Membership(db.Model):
    schema_name = os.getenv('SCHEMA_NAME')
    __tablename__ = 'membresia'
    __table_args__ = { 'schema': schema_name}

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    plan = db.Column(db.String(50), nullable = True)
    costo = db.Column(db.Numeric(10,2), nullable = True)
    contenido = db.Column(db.String(500), nullable = True)    

    def __init__(self, plan, costo, contenido):
        self.plan = plan
        self.costo = costo
        self.contenido = json.dumps(contenido) if (contenido) else None

    def checar_contenido (self):
        return json.loads(self.contenido) if self.contenido else {}

    def __repr__(self):
        return f'<Donations {self.plan}>'
