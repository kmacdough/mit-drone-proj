import unittest
import uuid
from datetime import datetime

from . import *

def new_id():
    return str(uuid.uuid4())

class TestDrone(unittest.TestCase):
    def test_dict_round_trip(self):
        d = Drone(new_id(), Geolocation(80.45, 100.90), .9, None)
        self.assertEqual(d, Drone.from_dict(d.to_dict()))


class TestGeolocation(unittest.TestCase):
    def test_dict_round_trip(self):
        g = Geolocation(80.45, 100.90)
        self.assertEqual(g, Geolocation.from_dict(g.to_dict()))


class TestPlace(unittest.TestCase):
    def test_dict_round_trip(self):
        p = Place(new_id(), "bermuda", Geolocation(80.45, 100.90))
        self.assertEqual(p, Place.from_dict(p.to_dict()))


class TestParcel(unittest.TestCase):
    def test_dict_round_trip(self):
        p = Parcel(new_id(), new_id(), new_id(), new_id(), new_id(),
                   12, 12, 12, 12,
                   datetime.utcnow().replace(hour=1),
                   datetime.utcnow().replace(hour=2),
                   datetime.utcnow().replace(hour=3))
        self.assertEqual(p, Parcel.from_dict(p.to_dict()))
