class Geolocation(object):
    """
    Model object representing a geolocation
    """
    def __init__(self, latitude, longitude):
        assert -90 <= latitude <= 90
        self.latitude = latitude
        assert -180 <= longitude <= 180
        self.longitude = longitude

    def to_dict(self):
        """
        Return the dictionary representation of this geolocation.
        :return: dictionary representation of this geolocation
        """
        return {
            "latitude": self.latitude,
            "longitude": self.longitude
        }

    @classmethod
    def from_dict(cls, d):
        """
        Create a new Place from a python dictionary
        :param d: python dictionary Place
        :return:
        """
        return cls(
            d["latitude"],
            d["longitude"]
        )

    def __eq__(self, other):
        return self.latitude == other.latitude and \
            self.longitude == other.longitude