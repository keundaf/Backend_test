Kibernum - Prueba tecnica backend

# Instalación de requerimientos para backend

## Librerias
```bash
pip install -r requirements.txt
```

## Instalar postgreSQL y configurar base de datos

Descargar e instalar  PostgreSQL desde la pagina oficial
```
https://www.postgresql.org/download/
```
Guardar credenciales (superusuario, base de datos, contraseña, Puerto escogido)

Crear una base de datos por medio de la interfaz grafica (pgadmin4)

El nombre de la base de datos (usuarios) debe coincidir con el de la variable base de datos del archivo app.py linea 12
## Github
Abrir powershell y usar el siguiente comando para clonar
```powershell
git clone https://github.com/keundaf/PruebaKibernum
```
# Recursos para debugging
## Instalar Insomnia
```
https://insomnia.rest/download
```

# Uso de aplicación
Abrir repositorio clonado
```
cd PruebaKibernum
```
Para ejecutar backend utilizar
```
python3 app.py
```
Con API funcionando usar los comandos para simular comunicación desde frontend.

## Consultar usuarios registrados (GET)
Insomnia:
-
metodo GET sin cuerpo a endpoint http://localhost:5000/usuarios
```
```

Retorna json con los usuarios registrados. De estar vacio retorna un json vacio

-------
## Crear nuevo usuario (POST)
Insomnia:
-
metodo POST con json a endpoint http://localhost:5000/usuarios
```json
{
	"nombre": "Kevin", 
	"apellido": "Unda",
	"correo":"keundaf@gmail.com",
	"Fecha_nacimiento":"1988-12-09"
}
```
Crea un usuario si cumple con todos los requisitos. En caso de no cumplirse algun requisito se retorna un json con la razón.

---------------
## Consultar datos de un usuario (GET)
Insomnia:
-
metodo GET sin cuerpo a endpoint http://localhost:5000/<uuid_usuario>
```
```
Retorna datos de usuario solicitado en un json. En caso de fallar, retorna un json con la razón

NOTA:
-

"<uuid_usuario>" corresponde al ID del usuario generado automaticamente con el metodo uuid.
Basta con copiar el ID del usuario que se quiera consultar desde el metodo GET usuarios mostrado en "Consultar usuarios registrados"

----------
## Actualizar datos de un usuario (PUT)
Insomnia:
-
metodo PUT con json a endpoint http://localhost:5000/<uuid_usuario>
```json
{
	"nombre": "Kevin", 
	"apellido": "Doppelganger",
	"correo":"kedopp@gmail.com",
	"Fecha_nacimiento":"1988-04-01"
}
```
Actualiza los datos del usuario en la base de datos y retorna datos de usuario modificados en un json. En caso de fallar, retorna un json con la razón


NOTA:
-

"<uuid_usuario>" corresponde al ID del usuario generado automaticamente con el metodo uuid.
Basta con copiar el ID del usuario que se quiera modificar desde el metodo GET usuarios mostrado en "Consultar usuarios registrados"

------------
## Eliminar datos de un usuario (DELETE)
Insomnia:
-
metodo DELETE sin cuerpo a endpoint http://localhost:5000/<uuid_usuario>
```json
```
Elimina un usuario de la base de datos y retorna un json confirmando la eliminación. En caso de fallar, retorna un json con la razon

NOTA:
-

"<uuid_usuario>" corresponde al ID del usuario generado automaticamente con el metodo uuid.
Basta con copiar el ID del usuario que se quiera borrar desde el metodo GET usuarios mostrado en "Consultar usuarios registrados"

