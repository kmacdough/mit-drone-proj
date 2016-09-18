from .geolocation import Geolocation
from .mongo_object import MongoObject
from .parcel import Parcel
from api import db
from util import expand_ref

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

    def to_dict(self, expand_refs=False, db=None):
        """
        Get a python dictionary representation of this object

        NOTE: if expand_refs == True then this is not reversed by from_dict
        :return:
        """
        result_dict = {
            'id': self.id_,
            'geolocation': self.geolocation.to_dict(),
            'battery': self.battery,
        }
        if expand_refs:
            assert db is not None
            expand_ref(result_dict, 'parcel_id', 'parcel', Parcel, db)
        return result_dict

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
