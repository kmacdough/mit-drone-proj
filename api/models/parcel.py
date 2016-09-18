from datetime import datetime

from util import expand_ref

from .geolocation import Geolocation
from .mongo_object import MongoObject


class ParcelStatus(object):
    UNASSIGNED = "unassigned"
    PENDING_PICKUP = "pending_pickup"
    IN_DELIVERY = "in_delivery"
    DELIVERED = "delivered"

class Parcel(MongoObject):
    """
    Model object representing a parcel to be sent via drone
    """

    _collection_name = "parcels"

    def __init__(self, id_, sender_id, recipient_id, origin_id,
                 destination_id, length, width, height, weight,
                 status=ParcelStatus.UNASSIGNED, created_time=None,
                 pickup_time=None, dropoff_time=None):
        self.id_ = id_
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.origin_id = origin_id
        self.destination_id = destination_id
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight
        self.status = status
        self.created_time = created_time if created_time is not None else datetime.utcnow()
        self.pickup_time = pickup_time
        self.dropoff_time = dropoff_time

    def to_dict(self, expand_refs=False, db=None):
        """
        Return the dictionary representation of this Parcel
        :return: dictionary representation of this object
        """
        result_dict = {
            "id": self.id_,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "origin_id": self.origin_id,
            "destination_id": self.destination_id,
            "dimensions": {
                "width": self.width,
                "height": self.height,
                "length": self.length,
                "weight": self.weight
            },
            "status": "status",
            "created_time": self.created_time,
            "pickup_time": self.pickup_time,
            "dropoff_time": self.dropoff_time
        }
        if expand_refs:
            assert db is not None
        return result_dict

    @classmethod
    def from_dict(cls, d):
        """
        Create a new Place from a python dictionary
        :param d: python dictionary Place
        :return:
        """
        return cls(
            id_=d["id"],
            sender_id=d["sender_id"],
            recipient_id=d["recipient_id"],
            origin_id=d["origin_id"],
            destination_id=d["destination_id"],
            width=d["dimensions"]["width"],
            height=d["dimensions"]["height"],
            length=d["dimensions"]["length"],
            weight=d["dimensions"]["weight"],
            created_time=d["created_time"],
            pickup_time=d["pickup_time"],
            dropoff_time=d["dropoff_time"],
        )

    def __eq__(self, other):
        return self.id_ == other.id_ and \
            self.sender_id == other.sender_id and \
            self.recipient_id == other.recipient_id and \
            self.origin_id == other.origin_id and \
            self.destination_id == other.destination_id and \
            self.width == other.width and \
            self.height == other.height and \
            self.length == other.length and \
            self.weight == other.weight and \
            self.created_time == other.created_time and \
            self.pickup_time == other.pickup_time and \
            self.dropoff_time == other.dropoff_time