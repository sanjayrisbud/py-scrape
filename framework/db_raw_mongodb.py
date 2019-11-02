# Interface to a MongoDB database
import datetime
import pymongo
from .db_int import DatabaseInterface


class DatabaseInterfaceRawMongoDB(DatabaseInterface):

    __database = None

    def __init__(self, dsn, logger):
        super().__init__(logger)
        self._conn = pymongo.MongoClient(dsn)
        self.__database = self._conn["test-database"]

    def query(self, dbtype, params={}):
        if isinstance(dbtype, str):
            col_name = dbtype
        else:
            col_name = dbtype.__class__.__name__
        c = self.__database[col_name]
        return c.find(params)

    def find(self, dbtype):
        c = self.__database[dbtype.__class__.__name__]
        return c.find_one({"ObjectKey": dbtype.computekey()}) is not None

    def delete(self, dbtype):
        c = self.__database[dbtype.__class__.__name__]
        c.delete_one({"ObjectKey": dbtype.computekey()})

    def store(self, dbtype):
        dbtype.set_private_fields()
        c = self.__database[dbtype.__class__.__name__]
        if self.find(dbtype):
            self._logger.debug("Updating record")
            d = dbtype.get_fields_and_values("update")
            d["LastExtracted"] = datetime.datetime.now()
            c.update_one({"ObjectKey": dbtype.computekey()}, {"$set": d})
        else:
            self._logger.debug("Inserting record")
            d = dbtype.get_fields_and_values("insert")
            c.insert_one(d)

    def create(self, dbtype):
        self.__database[dbtype.__class__.__name__]
