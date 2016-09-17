class MongoObject(object):

    @classmethod
    def get_by_id(cls, db, id_):
        """
        Get the item with the given ID from the Mongo collection designated in the
        calling class.

        :param db: MongoClient to use to retrieve the information
        :param id_: ID of the record to retrieve
        """
        mongo_result = db.get_collection(cls._collection_name).find_one({'id': id_})
        return cls.from_dict(mongo_result) if mongo_result is not None else None