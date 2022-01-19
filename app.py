
from flask import Flask,request,redirect, jsonify
from models import db,Usuario,User2dic,Userlist2dic
import uuid
from datetime import datetime
from email_validator import validate_email, EmailNotValidError

app = Flask(__name__)
# configuracion de base de datos
user_psql = 'postgres'
pass_psql = 'Kibernum'
baseDdatos = 'usuarios'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://'+user_psql+':'+pass_psql+'@localhost/'+baseDdatos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# crea tabla [EXPLICAR BIEN] 
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
        # Validar correo
        try:
            valid = validate_email(email_usuario)
            email = valid.email
        except EmailNotValidError as e:
            print(str(e))
            return jsonify({"message": "formato correo no valido: " + str(e)}),400

        correo = Usuario.query.filter_by(Email=email).first()
        if correo:
            return jsonify({"message": "correo duplicado"}),400
        
        # validar fecha
        Fecha_str = usuario_nuevo["Fecha_nacimiento"]
        hoy = datetime.now()
        try:
            Fecha_nacimiento = datetime.strptime(Fecha_str, '%Y-%m-%d')
            if hoy<Fecha_nacimiento:
                return jsonify({"message": "Bienvenido hombre del futuro"}),400
        except:
            return jsonify({"message": "Fecha no valida"}),400

        usuario = Usuario(ID_usuario,nombre_usuario, apellido_usuario, email_usuario, Fecha_nacimiento)
        db.session.add(usuario)
        db.session.commit()
        return jsonify(User2dic(usuario)),201

@app.route('/usuarios/<string:id>', methods=['GET','PUT','DELETE'])
def RetrieveSingleEmployee(id):
    usuario = Usuario.query.filter_by(ID=id).first()
    if request.method == 'GET':
        if usuario:
            return jsonify(User2dic(usuario)),200

    if request.method == 'PUT':
        #actualizacion completa
        usuario_requerido= request.json
        mail=usuario_requerido["correo"]
        
        '''llamo el usuario existente'''

        usuario_bycorreo = Usuario.query.filter_by(Email=mail).first()

        if (usuario and not usuario_bycorreo) or (usuario==usuario_bycorreo):
            #DATA
            ID_usuario = id
            nombre_usuario = usuario_requerido["nombre"]
            apellido_usuario = usuario_requerido["apellido"]
            email_usuario = usuario_requerido["correo"]


            # validar fecha
            Fecha_str = usuario_requerido["Fecha_nacimiento"]
            hoy = datetime.now()
            try:
                Fecha_nacimiento = datetime.strptime(Fecha_str, '%Y-%m-%d')
                if hoy<Fecha_nacimiento:
                    return jsonify({"message": "Bienvenido hombre del futuro"}),400
            except:
                return jsonify({"message": "Fecha no valida"}),400
            db.session.delete(usuario)
            db.session.commit()
            #ALMACENAR
            usuario = Usuario(ID_usuario,nombre_usuario, apellido_usuario, email_usuario, Fecha_nacimiento)
            db.session.add(usuario)
            db.session.commit()
            return jsonify(User2dic(usuario)),200
        else:
            if not usuario:
                return jsonify({"message": "Usuario no existe"}),404
            if usuario_bycorreo:
                return jsonify({"message": "Email duplicado"}),400

    if request.method == 'DELETE':
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            return jsonify({"message": "usuario eliminado satisfactoriamente"}),200
        else:
            return jsonify({"message": "id de usuario no encontrado"}),404


app.run(host='localhost', port=5000, debug=True)
