from models.place import Place

class Trip(object):
    def __init__(self, stops):
        self.stops = stops

    def to_dict(self):
        """
        Get a python dictionary representation of this object
        :return:
        """
        return {
            "stops": [stop.to_dict for stop in self.stops]
        }

    @classmethod
    def from_dict(cls, d):
        """
        Create a new Trip from a python dictionary
        :param d: python dictionary Trip
        :return:
        """
        return cls(
            [Place.from_dict(stop_dict) for stop_dict in d["stops"]]
        )