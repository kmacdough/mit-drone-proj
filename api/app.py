"""
app.py

Create an instance of the web service
"""
from flask import Flask
import os

import config


app = Flask(__name__)
app.config.from_object('config.' + os.environ.get('APP_SETTINGS', 'DevelopmentConfig'))
logger = app.logger