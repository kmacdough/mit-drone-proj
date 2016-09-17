class Geolocation(object):
    """
    Model object representing a geolocation
    """
    def __init__(self, latitude, longitude):
        assert 0 <= latitude <= 180 and 0 <= longitude <= 180
        self.latitude = lat
        self.longitude = longitude

    def to_dict():
        """
        Return the dictionary representation of this geolocation.
        :return: dictionary representation of this geolocation
        """
        return {
            "latitude": self.latitude,
            "longitude": self.longitude
        }