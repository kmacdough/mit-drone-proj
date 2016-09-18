"""
config.py

Reads configuration information for guiding a drone's location
"""

import json


# Represents the speed of the drone in delta(lat/long) per second
DRONE_SPEED = 0.1

# Amount of battery that is lost during every clock tick
DRONE_BATTERY_DRAIN_RATE = 0.001

API_HOST = 'http://localhost:8080'

def read(scenario):
    """
    Read the configuration for the given scenario
    """
    stream = open('scenarios/' + scenario + ".json", 'r')
    config = json.load(stream)
    print(config)
    return config