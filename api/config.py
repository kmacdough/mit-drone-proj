"""
Manages configuration information for running the application
"""
import os

HOST = os.environ.get('HOST', 'localhost')
PORT = os.environ.get('PORT', 8080)

class Config(object):
    """
    Base configuration class for the web service
    """
    DEBUG = False
    TESTING = False
    UPLOAD_FOLDER = "/uploads"
    SECRET_KEY = os.environ.get("SECRET_KEY")


class DevelopmentConfig(Config):
    """
    Configuration class for development
    """
    DEBUG = True
