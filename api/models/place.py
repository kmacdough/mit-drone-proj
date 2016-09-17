from models.geolocation import Geolocation

class Place(object):
    def __init__(self, id_, geolocation, name):
        self.id_ = id_
        self.geolocation = geolocation
        self.name = name

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
            d["id"],
            Geolocation.from_dict(d["geolocation"]),
            d["name"]
        )