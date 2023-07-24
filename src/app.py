"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets
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

@app.route('/users', methods=['GET'])
def get_all_users():
     
     all_users = User.query.all()
     all_users = list(map(lambda x: x.serialize(), all_users))

     print(all_users)

     return jsonify(all_users), 200

@app.route('/create-user', methods=['POST'])
def create_user():

    data = request.get_json()

    if data is None:
            response_body = {
                "msg": "BODY should be passed with request"
            }
            return jsonify(response_body), 400
    if "email" not in data:
            response_body = {
                 "msg": "Email should be passed with request"
            }
            return jsonify(response_body), 400
    if "password" not in data:
            response_body = {
                 "msg": "Password should be passed with request"
            }
            return jsonify(response_body), 400
    
    new_user = User(email = data["email"], password = data["password"], is_active = True)
    db.session.add(new_user)
    db.session.commit()

    all_users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), all_users)) 

    print(all_users)

    return jsonify(all_users, 200)  

@app.route('/user/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    
    user = User.query.get(user_id)
    user = user.serialize()

    print(user)

    return jsonify(user), 200

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
     
    data = request.get_json()

    if data is None:
            response_body = {
                "msg": "BODY should be passed with request"
            }
            return jsonify(response_body), 400
    if "email" not in data:
            response_body = {
                 "msg": "Email should be passed with request"
            }
            return jsonify(response_body), 400
    if "password" not in data:
            response_body = {
                 "msg": "Password should be passed with request"
            }
            return jsonify(response_body), 400
    
    update_user = User.query.get(user_id)
    update_user.email = data["email"]
    update_user.password = data["password"]
    db.session.commit()

    user = User.query.get(user_id)
    user = user.serialize()

    print(user)

    return jsonify(user), 200

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
      
      user =  User.query.get(user_id)
      db.session.delete(user)
      db.session.commit()

      response_body = {
            "msg": "User Deleted Successfully!"
      }

      return jsonify(response_body)

@app.route('/people', methods=['GET'])
def get_all_people():
     
     all_people = People.query.all()
     all_people = list(map(lambda x: x.serialize(), all_people))

     print(all_people)

     return jsonify(all_people), 200

@app.route('/create-people', methods=['POST'])
def create_people():

    data = request.get_json()

    if data is None:
            response_body_people = {
                "msg": "BODY should be passed with request"
            }
            return jsonify(response_body_people), 400
    
    
    new_people = People(name=data["name"], gender=data["gender"])
    db.session.add(new_people)
    db.session.commit()

    all_people = People.query.all()
    all_people = list(map(lambda x: x.serialize(), all_people)) 

    print(all_people)

    return jsonify(all_people, 200)  

@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_people(people_id):

    people = People.query.get(people_id)

    return jsonify(people.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():
     
     all_planets = Planets.query.all()
     all_planets = list(map(lambda x: x.serialize(), all_planets))

     print(all_planets)

     return jsonify(all_planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):

    planet = Planets.query.get(planet_id)

    return jsonify(planet.serialize()), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
