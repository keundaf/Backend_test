import json
from urllib import response
from xmlrpc.client import ResponseError
from flask import Flask,render_template,request,redirect, jsonify
from models import db,Usuario,User2dic,Userlist2dic
import uuid
from datetime import datetime
import psycopg2

from email_validator import validate_email, EmailNotValidError

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Kibernum@localhost/usuarios'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
 
@app.before_first_request
def create_table():
    db.create_all()

@app.route('/usuarios', methods = ['GET','POST'])
def create():

    if request.method == 'GET':
        Usuarios = Usuario.query.all()
        if not Usuarios:
            return jsonify({}),204
        else:
            return jsonify(Userlist2dic(Usuarios)),200

    if request.method == 'POST':

        usuario_nuevo = request.json
        #DATA
        ID_usuario = uuid.uuid4()
        nombre_usuario = usuario_nuevo["nombre"]
        apellido_usuario = usuario_nuevo["apellido"]

        email_usuario = usuario_nuevo["correo"]
        # Validar correo.
        try:
            valid = validate_email(email_usuario)
            email = valid.email
        except EmailNotValidError as e:
            print(str(e))
            return jsonify({"message": "formato correo no valido"}),400

        correo = Usuario.query.filter_by(Email=email).first()
        if correo:
            return jsonify({"message": "correo duplicado"}),400


            
        Fecha_str = usuario_nuevo["Fecha_nacimiento"]

        Fecha_nacimiento = datetime.strptime(Fecha_str, '%Y-%m-%d') # utilizar regex
        #ALMACENAR

        

        # if (usuario and not correo) or (usuario==correo):



        # trabajar en validación (correo y fecha) y agregar verificacion de uniquidad de correo
        usuario = Usuario(ID_usuario,nombre_usuario, apellido_usuario, email_usuario, Fecha_nacimiento)
        db.session.add(usuario)
        db.session.commit()
        usuario_salida = {"ID":ID_usuario,"nombre":nombre_usuario,"apellido":apellido_usuario,"correo":email_usuario,"Fecha_nacimiento":Fecha_str}
        
        return jsonify(usuario_salida),201



@app.route('/usuarios/<string:id>', methods=['GET','PUT','DELETE'])
def RetrieveSingleEmployee(id):
    usuario = Usuario.query.filter_by(ID=id).first()
    if request.method == 'GET':
        if usuario:
            return jsonify(User2dic(usuario)),200



    if request.method == 'PUT':
        #actualizacion completa
        usuario_requerido= request.json
        id=usuario_requerido["ID"]
        mail=usuario_requerido["correo"]
        
        '''llamo el usuario existente'''

        correo = Usuario.query.filter_by(Email=mail).first()

        if (usuario and not correo) or (usuario==correo):
            db.session.delete(usuario)
            db.session.commit()
            #DATA
            ID_usuario = id
            nombre_usuario = usuario_requerido["nombre"]
            apellido_usuario = usuario_requerido["apellido"]
            email_usuario = usuario_requerido["correo"]
            Fecha_str = usuario_requerido["Fecha_nacimiento"]
            Fecha_nacimiento = datetime.strptime(Fecha_str, '%Y-%m-%d')
            #ALMACENAR

            usuario = Usuario(ID_usuario,nombre_usuario, apellido_usuario, email_usuario, Fecha_nacimiento)
            db.session.add(usuario)
            db.session.commit()

            return redirect('/data')
        else:
            if not usuario:
                return "Usuario no Existe",404
            if correo:
                return "Correo existente"

    if request.method == 'DELETE':
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            return jsonify({"message": "usuario eliminado satisfactoriamente"}),200
        else:
            return jsonify({"message": "id de usuario no encontrado"}),404





@app.route('/usuario/modificar',methods = ['POST'])
def update():
    
    if request.method == 'POST':
        usuario_requerido= request.json
        id=usuario_requerido["ID"]
        mail=usuario_requerido["correo"]
        
        '''llamo el usuario existente'''
        usuario = Usuario.query.filter_by(ID=id).first()
        correo = Usuario.query.filter_by(Email=mail).first()

        if (usuario and not correo) or (usuario==correo):
            db.session.delete(usuario)
            db.session.commit()
            #DATA
            ID_usuario = id
            nombre_usuario = usuario_requerido["nombre"]
            apellido_usuario = usuario_requerido["apellido"]
            email_usuario = usuario_requerido["correo"]
            Fecha_str = usuario_requerido["Fecha_nacimiento"]
            Fecha_nacimiento = datetime.strptime(Fecha_str, '%Y-%m-%d')
            #ALMACENAR

            usuario = Usuario(ID_usuario,nombre_usuario, apellido_usuario, email_usuario, Fecha_nacimiento)
            db.session.add(usuario)
            db.session.commit()

            return redirect('/data')
        else:
            if not usuario:
                return "Usuario no Existe"
            if correo:
                return "Correo existente" 



app.run(host='localhost', port=5000, debug=True)
