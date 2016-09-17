"""
Defines API endpoints for accessing the application
"""
from flask import jsonify, request
from uuid import uuid4 as uuid

from app import app, logger, db
from models import Place, Parcel

@app.route('/test', methods=['GET'])
def test():
    logger.info('Received request at /test endpoint')
    return jsonify(status='success', data='It works!'), 200

@app.route('/test', methods=['POST'])
def test_retrieval():
    id_ = int(request.get_json()['id'])
    print(Place.get_by_id(db, id_).to_dict())
    return jsonify(status='success'), 200


@app.route('/parcel', methods=['POST'])
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
def get_parcel(uuid):
    parcel = Parcel.get_by_id(uuid)
    if parcel is None:
        jsonify(status='fail', message='No parcel existed with id = {}'.format(uuid))
    else:
        jsonify(status='success', data=parcel.to_dict())
