"""
app.py

Create an instance of the web service
"""
from flask import Flask
import os
from pymongo import MongoClient

import config


app = Flask(__name__)
app.config.from_object('config.' + os.environ.get('APP_SETTINGS', 'DevelopmentConfig'))
logger = app.logger
mongo_client = MongoClient('localhost', 27017)
db = mongo_client['drones']