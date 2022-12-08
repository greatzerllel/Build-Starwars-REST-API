"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from crypt import methods
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People,Planets, Favorite_Characters, Favorite_Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def traer_personajes():
     personajes = People.query.all()
     if not personajes: return jsonify({ "msg": "No hay personajes guadados en este momento. Agrega uno."}), 404
     personajes = list(map(lambda personaje: personaje.serialize(), personajes))
     return jsonify(personajes), 200

@app.route('/people/<int:id>', methods=['GET'])
def traer_personaje(id):
     personaje = People.query.get(id)
     return jsonify(personaje.serialize()), 200

@app.route('/people', methods=['POST']) 
def agregar_personajes():
    id = request.json.get('id')
    name = request.json.get('name')
    edad = request.json.get('edad')
    especie = request.json.get('especie')
    lugarNacimiento = request.json.get('lugarNacimiento')

    personaje = People()
    personaje.name = name
    personaje.edad = edad
    personaje.especie = especie
    personaje.lugarNacimiento = lugarNacimiento

    personaje.save()

    return jsonify(personaje.serialize()), 201

@app.route('/people/<int:id>', methods=['PUT'])
def actualizar_personaje(id):
    id = request.json.get('id')
    name = request.json.get('name')
    edad = request.json.get('edad')
    especie = request.json.get('especie')
    lugarNacimiento = request.json.get('lugarNacimiento')

    personaje = People.query.get(id)
    personaje.name = name
    personaje.edad = edad
    personaje.especie = especie
    personaje.lugarNacimiento = lugarNacimiento

    personaje.update()

    return jsonify(personaje.serialize()), 200

@app.route('/people/<int:id>', methods=['DELETE'])
def borrar_personaje(id):
    id = request.json.get('id')
    name=request.json.get('name')
    edad=request.json.get('edad')
    especie=request.json.get('especie')
    lugarNacimiento=request.json.get('lugarNacimiento')

    personaje = People.query.get(id)
    personaje.name=name
    personaje.edad =edad
    personaje.especie=especie
    personaje.lugarNacimiento=lugarNacimiento


    personaje.delete()

    return jsonify(personaje.serialize()), 200

@app.route('/planets', methods=['GET'])
def traer_planetas():
    planetas = Planets.query.all()
    if not planetas: return jsonify({ "msg": "No hay planetas guadados en este momento. Agrega uno."}), 404
    planetas = list(map(lambda planeta: planeta.serialize(), planetas))
    return jsonify(planetas), 200

@app.route('/planets/<int:id>', methods=['GET'])
def traer_planeta(id):
     planeta = Planets.query.get(id)
     return jsonify(planeta.serialize()), 200

@app.route('/planets', methods=['POST']) 
def agregar_planeta():
    id = request.json.get('id')
    name = request.json.get('name')
    galaxia = request.json.get('galaxia')

    planeta = Planets()
    planeta.id = id
    planeta.name = name
    planeta.galaxia = galaxia

    planeta.save()

    return jsonify(planeta.serialize()), 201


@app.route('/planets/<int:id>',methods=['PUT'])
def actualizar_planeta(id):
    id = request.json.get('id')
    name = request.json.get('name')
    galaxia = request.json.get('galaxia')

    planeta = Planets.query.get(id)
    planeta.id = id
    planeta.name = name
    planeta.galaxia = galaxia

    planeta.update()

    return jsonify(planeta.serialize()), 201

@app.route('/planets/<int:id>', methods =['DELETE'])
def eliminar_planeta(id):
    id = request.json.get('id')
    name = request.json.get('name')
    galaxia = request.json.get('galaxia')

    planeta = Planets.query.get(id)
    planeta.id = id
    planeta.name = name
    planeta.galaxia = galaxia

    planeta.delete()

    return jsonify(planeta.serialize()), 201


@app.route('/users', methods=['POST']) 
def agregar_usuario():
    id = db.Column(db.Integer, primary_key=True)
    nickname= db.Column(db.String(80), unique=False, nullable=True)
    name= db.Column(db.String(80), unique=False, nullable=True)
    lastname = db.Column(db.String(80), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    usuario = User()
    usuario.id = id
    usuario.nickname = nickname
    usuario.name = name
    usuario.lastname = lastname
    usuario.email = email

    usuario.save()

    return jsonify(usuario.serialize()), 201


@app.route('/users', methods=['GET'])
def traer_usuarios():
     usuarios = User.query.all()
     usuarios = list(map(lambda usuario: usuario.serialize(), usuarios))
     return jsonify(usuarios), 200

@app.route('/users/favorites', methods=['GET'])
def traer_favoritos_usuario():
     favoritos = User.query.all()
     favoritos= list(map(lambda favorito: favorito.serialize_with_favoritos(), favoritos))
     return jsonify(favoritos), 200

@app.route('/favorite/people/<int:id>', methods=['POST'])
def agregar_personaje_favorito(id):
    id_user = 1

    personaje_favorito = Favorite_Characters()
    personaje_favorito.id_user = id_user
    personaje_favorito.personaje_id = id


    personaje_favorito.save()

    return jsonify(personaje_favorito.serialize()), 201


@app.route('/favorite/planet/<int:planeta_id>', methods=['POST'])
def agregar_planeta_favorito(planeta_id):
    id_user = request.json.get('id_user')

    planeta_favorito = Favorite_Planets()
    planeta_favorito.id_user = id_user
    planeta_favorito.planeta_id = planeta_id


    planeta_favorito.save()

    return jsonify(planeta_favorito.serialize()), 201


@app.route('/favorite/people/<int:id>', methods=['DELETE'])
def borrar_personaje_favorito(id):

    personaje_favorito = Favorite_Characters.query.filter_by(id_user=1,personaje_id=id).first()

    personaje_favorito.delete()

    return jsonify({"mensaje":"personaje favorito eliminado"}), 200


@app.route('/favorite/planet/<int:id>', methods=['DELETE'])
def borrar_planeta_favorito(id):
    planeta_favorito = Favorite_Planets.query.filter_by(id_user=1,planeta_id=id).first()

    planeta_favorito.delete()

    return jsonify({"mensaje":"planeta favorito eliminado"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
