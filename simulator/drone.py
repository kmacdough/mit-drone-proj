"""
drone.py

Simulates a drone that can deliver packages from one location
to another.
"""
import math
import requests

from config import DRONE_SPEED, API_HOST

class Drone(object):
    """
    Represents a drone that can deliver packages.
    """
    def __init__(self, latitude, longitude, destination = None, parcel=None, battery=1.0, id_=None):
        self.latitude = latitude
        self.longitude = longitude
        self.dest = destination
        self.parcel = parcel
        self.battery = battery
        new_json = {
            'latitude': latitude,
            'longitude': longitude,
            'battery': battery,
            'parcel_id': parcel.id_ if parcel is not None else None
        }
        response = requests.post(API_HOST + '/drones', json=new_json)
        self.id_ = response.json()['data']

    def at_destination(self):
        return self.latitude == self.dest['lat'] and self.longitude == self.dest['long'] 

    def on_tick(self):
        """
        Simulate one second of travel for this drone
        """
        if self.parcel is not None:
            reached_destination = False
            d_lat = self.dest['lat'] - self.latitude
            d_long = self.dest['long'] - self.longitude
            arctan = math.atan(d_lat / d_long) if d_long != 0 else (3.141592 / 2.0)
            new_lat = self.latitude + math.sin(arctan) * DRONE_SPEED
            new_long = self.longitude + math.cos(arctan) * DRONE_SPEED
            
            # check if this clock tick caused the drone to reach the target
            if (self.parcel.get('lat', self.parcel.get('latitude')) - new_lat) * d_lat <= 0:
                reached_destination = True
                self.latitude = self.dest['lat']
                self.longitude = self.dest['long']
            else:
                self.latitude = new_lat
                self.longitude = new_long

            update_payload = {
                "latitude": self.latitude,
                "longitude": self.longitude,
            }

            if reached_destination and parcel is None:
                update_payload['status'] = "DROP OFF"
                update_payload['has_parcel'] = True
            elif reach_destination and parcel is not None:
                update_payload['status'] = "IDLE"
                update_payload['has_parcel'] = False
                update_payload['delivered_parcel'] = self.parcel['id']
        else:
            update_payload = {
                "latitude": self.latitude,
                "longitude": self.longitude,
                "has_parcel": self.parcel is not None
            }
        print(update_payload)
        response = requests.put(API_HOST + '/drones/' + str(self.id_), json=update_payload)

        if len(response.json()) > 0:
            self.parcel = response.json()['data']
            self.dest = {
                'lat': self.parcel['destination']['geolocation']['latitude'],
                'long': self.parcel['destination']['geolocation']['longitude']
            }
        print(response.json())


