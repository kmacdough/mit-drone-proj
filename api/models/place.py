from .geolocation import Geolocation
from .mongo_object import MongoObject


class Place(MongoObject):

    _collection_name = "places"

    def __init__(self, id_, name, geolocation):
        self.id_ = id_
        self.name = name
        self.geolocation = geolocation

    def to_dict(self):
        """
        Get a python dictionary representation of this object
        :return:
        """
        return {
            "id": self.id_,
            "geolocation": self.geolocation.to_dict(),
            "name": self.name
        }

    @classmethod
    def from_dict(cls, d):
        """
        Create a new Place from a python dictionary
        :param d: python dictionary Place
        :return:
        """
        return cls(
            id_=d["id"],
            geolocation=Geolocation.from_dict(d["geolocation"]),
            name=d["name"]
        )

    def __eq__(self, other):
        return self.id_ == other.id_ and \
            self.geolocation == other.geolocation and \
            self.name == other.name
