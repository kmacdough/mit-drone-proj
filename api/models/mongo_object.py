class MongoObject(object):

    @classmethod
    def get_by_id(cls, id_, db):
        """
        Get the item with the given ID from the Mongo collection designated in the
        calling class.

        :param db: MongoClient to use to retrieve the information
        :param id_: ID of the record to retrieve
        """
        mongo_result = db.get_collection(cls._collection_name).find_one({'id': id_})
        return cls.from_dict(mongo_result) if mongo_result is not None else None

    @classmethod
    def query(cls, db, **kwargs):
        """
        Query the db for the given search parameters
        """
        mongo_result = db.get_collection(cls._collection_name).find(kwargs)
        return [cls.from_dict(result) for result in mongo_result]

    @classmethod
    def insert(cls, object, db):
        """
        """
        mongo_result = db.get_collection(cls._collection_name).insert(object.to_dict())
        return mongo_result

    @classmethod
    def update(cls, id_, db, **kwargs):
        """
        Updates an object based on the id using the kwargs
        """
        collection = db.get_collection(cls._collection_name)
        collection.update({"id": id_}, {"$set": kwargs})