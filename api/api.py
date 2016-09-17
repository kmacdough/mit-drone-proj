"""
Defines API endpoints for accessing the application
"""
from flask import jsonify, request
from uuid import uuid4 as uuid

from app import app, logger, db
from models import Place

@app.route('/test', methods=['GET'])
def test():
    logger.info('Received request at /test endpoint')
    return jsonify(status='success', data='It works!'), 200

@app.route('/test', methods=['POST'])
def test_retrieval():
    id_ = int(request.get_json()['id'])
    print(Place.get_by_id(db, id_).to_dict())
    return jsonify(status='success'), 200

