"""
Defines API endpoints for accessing the application
"""
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4 as uuid

from app import app, logger, db
from models import Place, User, Parcel
from util import error_handle


@app.route('/test', methods=['GET'])
def test():
    logger.info('Received request at /test endpoint')
    return jsonify(status='success', data='It works!'), 200

@app.route('/test', methods=['POST'])
def test_retrieval():
    id_ = int(request.get_json()['id'])
    print(Place.get_by_id(db, id_).to_dict())
    return jsonify(status='success'), 200


############################################
#             User Endpoints               #
############################################

@app.route('/login', methods=['POST'])
def login():
    email = request.headers.get('email')
    password = request.headers.get('password')
    if email is None or password is None:
        return jsonify(status='fail', message='Missing username or password'), 400
    else:
        users = User.query(db, email=email)
        print(users)
        if len(users) > 0 and check_password_hash(users[0].salted_password, password):
            resp = make_response(jsonify(status='success', data=users[0].to_dict())), 200
            resp.set_cookie('user_id', users[0].id_)
            return resp
        else:
            return jsonify(status='fail', message='Unauthorized'), 401

@app.route('/user', methods=['POST'])
def create_user():
    """
    Create a new user from the provided information
    """
    json = request.get_json()
    user = User(str(uuid()), json['email'], generate_password_hash(json['password']))
    result = User.insert(user, db)
    return jsonify(status='success', data=user.id_)


############################################
#            Place Endpoints               #
############################################


@app.route('/place', methods=['POST'])
def create_place():
    """
    Create a new place entry in the database
    """
    json = request.get_json()
    json['id'] = str(uuid())
    result = Place.insert(Place.from_dict(json), db)
    return jsonify(status='success', data=json['id']), 200

@app.route('/place/<place_id>', methods=['GET'])
def get_place(place_id):
    """
    Get the data for the place withthe given ID
    """
    place = Place.get_by_id(place_id, db)
    return jsonify(status='success', data=place.to_dict()), 200

@app.route('/place', methods=['GET'])
def get_all_places():
    """
    Get the data for all of the places associated with the given user
    """

@app.route('/parcel', methods=['POST'])
@error_handle
def new_parcel():
    request_json = request.get_json()
    length = request_json["length"]
    width = request_json["width"]
    height = request_json["height"]
    weight = request_json["weight"]
    origin_uuid = request_json["origin"]
    destination_uuid = request_json["destination"]

    id_ = str(uuid())
    origin = Place.get_by_id(origin_uuid).geolocation
    destination = Place.get_by_id(destination_uuid).geolocation
    location = origin

    parcel = Parcel(
        id_=id_,
        length=length,
        width=width,
        height=height,
        weight=weight,
        origin=origin,
        destination=destination,
        location=location
    )
    return jsonify(status='success', data=id_)


@app.route('/parcel/<uuid>', methods=['GET'])
@error_handle
def get_parcel(uuid):
    parcel = Parcel.get_by_id(uuid)
    if parcel is None:
        jsonify(status='fail', message='No parcel existed with id = {}'.format(uuid))
    else:
        jsonify(status='success', data=parcel.to_dict())
