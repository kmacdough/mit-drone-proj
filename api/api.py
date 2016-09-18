"""
Defines API endpoints for accessing the application
"""
from flask import jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4 as uuid

from app import app, logger, db
from models import Place, User, Parcel, Drone, ParcelStatus
from util import error_handle


def create_basic_endpoints(base_endpoint, cls):
    """
    Create basic get all and get by id endpoints for a given class with
    a base endpoint
    """
    @app.route(base_endpoint, methods=['GET'])
    @error_handle
    def get_all():
        """
        Get the instances of the class from Mongo
        """
        all_objs = cls.query(db)
        response = [obj.to_dict() for obj in all_objs]
        return jsonify(status="success", data=response)

    @app.route('/place/<obj_id>', methods=['GET'])
    @error_handle
    def get_place(obj_id):
        """
        Get the data for the object with the given ID
        """
        place = Place.get_by_id(obj_id, db)
        if place is None:
            return jsonify(status='fail',
                           message='No Place exists with id = {}'.format(obj_id))
        return jsonify(status='success', data=place.to_dict()), 200


############################################
#             User Endpoints               #
############################################


@app.route('/login', methods=['POST'])
def login():
    post_json = request.get_json()
    email = post_json['email']
    password = post_json['password']
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
    if len(User.query(db, email=json['email'])) > 0:
        return jsonify(status='fail', message='User already exists with email address')
    else:
        user = User(str(uuid()), json['email'], generate_password_hash(json['password']))
        result = User.insert(user, db)
        return jsonify(status='success', data=user.id_)


############################################
#            Place Endpoints               #
############################################


create_basic_endpoints('/place', Place)


@app.route('/place', methods=['POST'])
def create_place():
    """
    Create a new place entry in the database
    """
    json = request.get_json()
    json['id'] = str(uuid())
    result = Place.insert(Place.from_dict(json), db)
    return jsonify(status='success', data=json['id']), 200


############################################
#            Parcel Endpoints              #
############################################


create_basic_endpoints('/parcel', Place)


@app.route('/parcel', methods=['POST'])
@error_handle
def new_parcel():
    request_json = request.get_json()
    sender_id = request_json["sender_id"],
    recipient_id = request_json["recipient_id"],
    origin_id= request_json["origin_id"],
    destination_id = request_json["destination_id"],
    length = request_json["length"]
    width = request_json["width"]
    height = request_json["height"]
    weight = request_json["weight"]

    id_ = str(uuid())

    parcel = Parcel(
        id_=id_,
        sender_id=sender_id,
        recipient_id=recipient_id,
        origin_id=origin_id,
        destination_id=destination_id,
        length=length,
        width=width,
        height=height,
        weight=weight
    )
    Parcel.insert(parcel, db)
    return jsonify(status='success', data=id_)


############################################
#            Drone Endpoints               #
############################################


create_basic_endpoints('/drones', Drone)


@app.route('/drones', methods=['POST'])
def new_drone():
    json = request.get_json()

    json['geolocation'] = {'latitude': json['latitude'], 'longitude': json['longitude']}
    json['id'] = str(uuid())

    result = Drone.insert(Drone.from_dict(json), db)
    return jsonify(status='success', data=json['id']), 200
    

@app.route('/drones/<id>', methods=['PUT'])
def update_drone():
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