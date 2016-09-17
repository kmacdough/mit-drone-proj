from models.geolocation import Geolocation
from models.mongo_object import MongoObject

class Drone(MongoObject):
    """
    Represents an individual drone
    """

    _collection_name = 'drones'

    def __init__(self, id_, position, trip_id=None):
        self.id_ = id_
        self.position = position
        self.trip_id = trip_id

    def to_dict(self):
        """
        Get a python dictionary representation of this object
        :return:
        """
        return {
            "id": self.id_,
            "position": self.position.to_dict(),
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
            Position.from_dict(d["position"]),
            d["trip_id"]
        )
