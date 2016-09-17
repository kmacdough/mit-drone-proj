from models.geolocation import Geolocation
from models.mongo_object import MongoObject

class Parcel(MongoObject):
    """
    Model object representing a parcel to be sent via drone
    """

    _collection_name = "parcels"

    def __init__(self, id_, length, width, height, weight, origin, destination, location):
        self.id_ = id_
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight
        self.origin = origin
        self.destination = destination
        self.location = location

    def to_dict(self):
        """
        Return the dictionary representation of this Parcel
        :return: dictionary representation of this object
        """
        return {
            "id": self.id_,
            "dimensions": {
                "width": self.width,
                "height": self.height,
                "length": self.length,
                "weight": self.weight
            },
            "locations": {
                "origin": self.origin.to_dict(),
                "destination": self.destination.to_dict(),
                "current": self.location.to_dict(),
            }
        }

    @classmethod
    def from_dict(cls, d):
        """
        Create a new Place from a python dictionary
        :param d: python dictionary Place
        :return:
        """
        return cls(
            _id=d["id"],
            width=d["dimensions"]["width"],
            height=d["dimensions"]["height"],
            length=d["dimensions"]["length"],
            weight=d["dimensions"]["weight"],
            origin=Geolocation.from_dict(d["locations"]["origin"]),
            destination=Geolocation.from_dict(d["locations"]["destination"]),
            location=Geolocation.from_dict(d["locations"]["current"]),
        )