"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, make_response
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, association_people, association_planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    people_list = list(map(lambda x: x.serialize(), people))

    return jsonify(people_list), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id(people_id):
    people1 = People.query.filter_by(id=people_id)[0]

    return jsonify(people1.serialize()), 200


@app.route('/planets', methods=['GET'])
def get_planets():

    planets = Planets.query.all()
    planets_list = list(map(lambda x: x.serialize(), planets))

    return jsonify(planets_list), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planets_id(planets_id):
    planet1 = Planets.query.filter_by(id=planets_id)[0]

    return jsonify(planet1.serialize()), 200

@app.route('/user', methods=['GET'])
def get_users():

    users = User.query.all()
    user_list = list(map(lambda x: x.serialize(), users))

    return jsonify(user_list), 200

@app.route('/user/favorites/<int:user_id>', methods=['GET'])
def get_user_favorites(user_id):

    user_people = User.query.filter_by(id=user_id).first().people
    user_planets = User.query.filter_by(id=user_id).first().planets

    mixed = {
        "people": list(map(lambda x: x.serialize(), user_people)),
        "planets": list(map(lambda x: x.serialize(), user_planets))
            }
    #user_fav_list = list(map(lambda x: x.serialize(), mixed))

    return jsonify(mixed), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def post_favorite_planet(planet_id):
    #Mandamos el user_id como parametro de la url ?user_id=1
    user_id = request.args.get("user_id")

    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)

    fav_planet = user.planets.append(planet)

    db.session.commit()

    return "Success:su planeta se agrego correctamente a favoritos", 200


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def post_favorite_people(people_id):
    #Mandamos el user_id como parametro de la url ?user_id=1
    user_id = request.args.get("user_id")

    user = User.query.get(user_id)
    people = People.query.get(people_id)

    fav_people = user.people.append(people)

    db.session.commit()

    return "Success:su people se agrego correctamente a favoritos", 200

    
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    #Mandamos el user_id como parametro de la url ?user_id=1
    user_id = request.args.get("user_id")

    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)

    fav_planet = user.planets.remove(planet)

    db.session.commit()

    return "Success:su planeta se borro correctamente de favoritos", 200


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    #Mandamos el user_id como parametro de la url ?user_id=1
    user_id = request.args.get("user_id")

    user = User.query.get(user_id)
    people = People.query.get(people_id)

    fav_people = user.people.remove(people)

    db.session.commit()

    return "Success:su people se Borro correctamente de favoritos", 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
