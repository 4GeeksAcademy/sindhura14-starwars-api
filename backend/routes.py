"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, Blueprint
from backend.models import db, User,Characters,Planets,Favorites
from flask_cors import CORS
from flask_jwt_extended import (
    create_access_token, current_user, jwt_required
)




api = Blueprint('api', __name__, url_prefix="/api")

# Allow CORS requests to this API
CORS(api)

#verification when user tries to login
@api.route("/login", methods=["POST"])
def login():
    body = request.json
    user: User | None = User.query.filter_by(
        email=body["email"]
    ).first()

    if not user:
        return jsonify(msg="Invalid credentials."), 401
    
    if user.password != body.get("password"):
        return jsonify(msg="Invalid credentials."), 401

    return jsonify(
        token=create_access_token(user)
    )


#creating a new user
@api.route("/users", methods=["POST"])
def create_user():
    body = request.json
    user: User | None = User.query.filter_by(
        email=body["email"]
    ).first()
    if user:
        return jsonify(msg="User already exists"), 400
    
    user = User(
        email=body["email"],
        password=body["password"]
    )
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)

    return jsonify(user.serialize())

#get current user
@api.route("/users/current", methods=["GET"])
def get_current_user():
    return jsonify(current_user.serialize())

#get all users
@api.route("/users", methods=["GET"])
def get_all_users():
    all_users = User.query.all()
    users=[user.serialize() for user in all_users] 
    return jsonify(users)

#get a particular user
@api.route("/users/<string:email>", methods=["GET"])
def get_single_user(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify(msg="User does not exist."), 404
    return jsonify(user.serialize())

#get user favorites
@api.route("/users/<int:id>/favourites",methods=['GET'])
def get_user_favorites(id):
    user = User.query.get(id)
    if not user:
        return jsonify(msg='User not found'), 404
    favourites = user.favourites
    all_favourites = [favourite.serialize() for favourite in favourites]
    return jsonify(all_favourites), 200


#get all characters
@api.route("/people", methods=["GET"])
def get_all_characters():
    characters = Characters.query.all()
    characters=[person.serialize() for person in characters]
    return jsonify(characters)

#get a particular person
@api.route("/people/<int:id>", methods=["GET"])
def get_single_character(id: int):
    character = Characters.query.filter_by(id=id).first()
    if not character:
        return jsonify(msg="Character does not exist."), 404
    return jsonify(character.serialize())

#get all planets
@api.route("/planets", methods=["GET"])
def get_all_planets():
    planets = Planets.query.all()
    return jsonify(planets=[planet.serialize() for planet in planets])

#get a particular planet
@api.route("/planet/<int:id>", methods=["GET"])
def get_single_planet(id: int):
    planet = Planets.query.filter_by(id=id).first()
    if not planet:
        return jsonify(msg="Planet does not exist."), 404
    return jsonify(planet.serialize())

#add a  favorite planet
@api.route('/favorite/planet/<int:planets_id>', methods=['POST'])
def add_favourite_planet(planets_id):
    user_id = current_user.id
    print(user_id)
    user = User.query.get(user_id)
    if not user:
        return jsonify(msg="User not found"), 404

    planet = Planets.query.get(planets_id)
    if not planet:
        return jsonify(msg="Planet not found"), 404

    favorite_planet = Favorites(user_id=user.id, planet_id=planet.id)
    db.session.add(favorite_planet)
    db.session.commit()
    return jsonify(msg='Favourite planet added successfully'), 200

#add a favorite person
@api.route('/favorite/people/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    user_id = current_user.id
    user = User.query.get(user_id)
    if not user:
        return jsonify(msg='User not found'), 404

    character = Characters.query.get(character_id)
    if not character:
        return jsonify(msg='Character not found'), 404

    favorite_character = Favorites(user_id=user.id, character_id=character.id)
    db.session.add(favorite_character)
    db.session.commit()

    return jsonify({'msg': 'Favourite character added successfully'}), 200


#delete a planet from favorites
@api.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = current_user.id
    favorite_planet = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favorite_planet:
        return jsonify(msg= 'Favourite planet not found'), 404

    db.session.delete(favorite_planet)
    db.session.commit()

    return jsonify(msg='Favourite planet deleted successfully'), 200

#delete a person from favorites
@api.route('/favorite/people/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(character_id):
    user_id = request.headers.get('user_id')
    favorite_character = Favorites.query.filter_by(user_id=user_id, character_id=character_id).first()
    if not favorite_character:
        return jsonify(msg='Favourite character not found'), 404

    db.session.delete(favorite_character)
    db.session.commit()

    return jsonify(msg='Favourite character deleted successfully'), 200
    



