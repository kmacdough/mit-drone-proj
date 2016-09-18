from models.geolocation import Geolocation
from models.mongo_object import MongoObject

class Drone(MongoObject):
    """
    Represents an individual drone
    """

    _collection_name = 'drones'

    def __init__(self, id_, location, trip_id=None):
        self.id_ = id_
        self.location = location
        self.trip_id = trip_id

    def to_dict(self):
        """
        Get a python dictionary representation of this object
        :return:
        """
        return {
            "id": self.id_,
            "location": self.location.to_dict(),
            "trip_id": self.trip.to_dict()
        }

    @classmethod
    def from_dict(cls, d):
        """
        Create a new Drone from a python dictionary
        :param d:
        :return:
        """
        return cls(
            d["id"],
            Geolocation.from_dict(d["location"]),
            d["trip_id"]
        )
