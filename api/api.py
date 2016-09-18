"""
Defines API endpoints for accessing the application
"""
from flask import jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4 as uuid

from app import app, logger, db
from models import Place, User, Parcel, Drone, ParcelStatus
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
        if len(users) > 0 and check_password_hash(users[0].salted_password, password):
            resp = make_response(jsonify(status='success', data=users[0].to_dict(has_salted_password=False)), 200)
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
    if len(User.query(email=json['email'])) > 0:
        return jsonify(status='fail', message='User already exists with email address')
    else:
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
    pass


############################################
#            Parcel Endpoints              #
############################################

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
    origin = Place.get_by_id(origin_uuid, db).geolocation
    destination = Place.get_by_id(destination_uuid, db).geolocation
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

@error_handle
@app.route('/parcel/<uuid>', methods=['GET'])
def get_parcel(uuid):
    parcel = Parcel.get_by_id(uuid)
    if parcel is None:
        jsonify(status='fail', message='No parcel existed with id = {}'.format(uuid))
    else:
        jsonify(status='success', data=parcel.to_dict())

############################################
#            Drone Endpoints               #
############################################

@app.route('/drones', methods=['POST'])
def new_drone():
    json = request.get_json()

    json['geolocation'] = {'latitude': json['latitude'], 'longitude': json['longitude']}
    json['id'] = str(uuid())

    result = Drone.insert(Drone.from_dict(json), db)
    return jsonify(status='success', data=json['id']), 200

@app.route('/drones/<drone_id>', methods=['PUT'])
def update_drone(drone_id):
    json = request.get_json()
    json['geolocation'] = {'latitude': json['latitude'], 'longitude': json['longitude']}
    update_json = {key: val for key, val in json.items() if key not in ['latitude', 'longitude']}
    if 'status' in update_json:
        parcel_status = {
            'PICK UP': ParcelStatus.PENDING_PICKUP,
            'DROP OFF': ParcelStatus.IN_DELIVERY,
            'IDLE': ParcelStatus.DELIVERED
        }[update_json['status']]
        if parcel_status == ParcelStatus.DELIVERED:
            Parcel.update(db, update_json['delivered_parcel'], status=ParcelStatus.DELIVERED)
            del update_json['delivered_parcel']
    print(drone_id, update_json)
    Drone.update(drone_id, db, **update_json)

    return jsonify(status='success', data=True)


@app.route('/drones/<id>', methods=['GET'])
def get_drone(id):
    drone = Drone.get_by_id(id, db)
    return jsonify(status='success', data=drone.to_dict())


@app.route('/drones/nearest', methods=['GET'])
def get_nearest_drones():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    available_drones = Drone.query(db, parcel=None)

    best_drone = None
    min_distance = float('Inf')

    for available_drone in available_drones:
        distance = (available_drone.geolocation.longitude - float(lon)) ** 2 + (available_drone.geolocation.latitude - float(lat)) ** 2
        if distance < min_distance:
            min_distance = distance
            best_drone = available_drone

    if best_drone:
        return best_drone.id_
    else:
        return "None"


