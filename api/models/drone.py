from .geolocation import Geolocation
from .mongo_object import MongoObject

class Drone(MongoObject):
    """
    Represents an individual drone
    """

    _collection_name = 'drones'

    def __init__(self, id_, geolocation, battery=1.0, parcel_id=None):
        self.id_ = id_
        assert isinstance(geolocation, Geolocation)
        self.geolocation = geolocation
        assert 0 <= battery <= 1
        self.battery = battery
        self.parcel_id = parcel_id

    def to_dict(self):
        """
        Get a python dictionary representation of this object
        :return:
        """
        return {
            'id': self.id_,
            'geolocation': self.geolocation.to_dict(),
            'battery': self.battery,
            'parcel_id': self.parcel_id,
        }

    @classmethod
    def from_dict(cls, d):
        """
        Create a new Drone from a python dictionary
        :param d:
        :return:
        """
        return cls(
            id_=d['id'],
            geolocation=Geolocation.from_dict(d['geolocation']),
            battery=d.get('battery', 1.0),
            parcel_id=d.get('parcel_id', None),
        )

    def __eq__(self, other):
        return self.id_ == other.id_ and \
            self.geolocation == other.geolocation and \
            self.battery == other.battery and \
            self.parcel_id == other.parcel_id
