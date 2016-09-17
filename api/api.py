"""
Defines API endpoints for accessing the application
"""
from flask import jsonify

from app import app, logger


@app.route('/test', methods=['GET'])
def test():
    logger.info('Received request at /test endpoint')
    return jsonify(status='success', data='It works!'), 200