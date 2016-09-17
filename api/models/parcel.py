class Parcel(object):
    """
    Model object representing a parcel to be sent via drone
    """
    def __init__(self, id_, length, width, height, weight, origin, destination, location):
        self.id_ = id
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
                "current": self.location.to_dict(),
                "origin": self.origin.to_dict(),
                "destination": self.destination.to_dict()
            }
        }