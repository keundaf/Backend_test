from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'DatosUsuarios'
    ID = db.Column(db.String(50), primary_key=True)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    Email = db.Column(db.String(50), unique=True)
    Fecha_nacimiento = db.Column(db.DateTime)

    def __init__(self, ID, nombre, apellido, Email, Fecha_nacimiento):
        self.ID = ID
        self.nombre = nombre
        self.apellido = apellido
        self.Email = Email
        self.Fecha_nacimiento = Fecha_nacimiento.date()
    
    def __repr__(self):
        return f"{self.apellido}, {self.nombre}: ID= {self.ID}"
