"""
main.py

Main entry point for starting the web service
"""
from app import app
from config import HOST, PORT
from api import *

def main():
    """
    Main method to start the web server
    """
    app.run(HOST, PORT)
    return app


if __name__ == "__main__":
    main()