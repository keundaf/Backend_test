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
    '''
    def __repr__(self):
        return f"{self.apellido}, {self.nombre}: ID= {self.ID}"
    '''

def RKB(self):
    json_data_id = []
    json_data_nombre = []
    json_data_apellido = []
    json_data_email = []
    json_data_fecha = []
    for usuario in self:
        json_data_id.append(usuario.ID)
        json_data_nombre.append(usuario.nombre)
        json_data_apellido.append(usuario.apellido)
        json_data_email.append(usuario.Email)
        json_data_fecha.append(usuario.Fecha_nacimiento)
    return {"ID":json_data_id,"nombre":json_data_nombre,"apellido":json_data_apellido,"correo":json_data_email,"Fecha_nacimiento":json_data_fecha}
        #return {"ID":self.ID,"nombre":self.nombre,"apellido":self.apellido,"correo":self.Email,"Fecha_nacimiento":self.Fecha_nacimiento}
