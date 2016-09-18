from .mongo_object import MongoObject

class User(MongoObject):
    """
    Represents a user of the system
    """

    _collection_name = 'users'

    def __init__(self, id_, email, salted_password=None):
        self.id_ = id_
        self.email = email
        self.salted_password = salted_password

    def to_dict(self):
        """
        Return the dictionary representation of this user
        :return: dictionary representation of this user
        """
        return {
            "id": self.id_,
            "email": self.email,
            "salted_password": self.salted_password
        }

    @classmethod
    def from_dict(cls, d):
        """
        Return a new User from the given dict
        """
        return cls(d['id'], d['email'])