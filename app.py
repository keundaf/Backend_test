from flask import Flask,render_template,request,redirect
from models import db,Usuario
import uuid
from datetime import datetime
import psycopg2

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Kibernum@localhost/usuarios'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
 
@app.before_first_request
def create_table():
    db.create_all()

@app.route('/data/crear', methods = ['GET','POST'])
def create():

    if request.method == 'GET':
        return 'JSON no recibido'

    if request.method == 'POST':

        usuario_nuevo = request.json
        #DATA
        ID_usuario = uuid.uuid4()
        nombre_usuario = usuario_nuevo["nombre"]
        apellido_usuario = usuario_nuevo["apellido"]
        email_usuario = usuario_nuevo["correo"]
        Fecha_str = usuario_nuevo["Fecha_nacimiento"]
        Fecha_nacimiento = datetime.strptime(Fecha_str, '%Y-%m-%d')
        #ALMACENAR
        usuario = Usuario(ID_usuario,nombre_usuario, apellido_usuario, email_usuario, Fecha_nacimiento)
        db.session.add(usuario)
        db.session.commit()
        
        return 'usuario creado'

@app.route('/data')
def RetrieveDataList():
    Usuarios = Usuario.query.all()
    return render_template('lista_usuarios.html',Usuarios = Usuarios)

@app.route('/data/leer', methods=['GET'])
def RetrieveSingleEmployee():
    if request.method == 'GET':
        usuario_requerido= request.json
        id=usuario_requerido["ID"]
        usuario = Usuario.query.filter_by(ID=id).first()
        if usuario:
            return render_template('datos.html', usuario = usuario)
        return f"Usuario con id ={id} no existe"

@app.route('/data/modificar',methods = ['POST'])
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


@app.route('/data/eliminar', methods=['DELETE'])
def delete():
    usuario_requerido= request.json
    id=usuario_requerido["ID"]
    usuario = Usuario.query.filter_by(ID=id).first()
    if request.method == 'DELETE':
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            return "usuario eliminado"
        return "usuario no encontrado"
 
    #return render_template('borrar.html')

app.run(host='localhost', port=5000, debug=True)