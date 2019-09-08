# Abstraction of a specialized Type that can be saved to the database.
# Aside from user-defined fields, each database type has the following system fields:
#     -> RobotName: name of the robot that created this instance
#     -> ExecutionId: id of the robot run that created this instance
#     -> ObjectKey: an id for this instance; a hash of the user-defined fields
#                     with "part of database key" equal to True
#     -> FirstExtracted: the time when this instance was saved to the database
#     -> LastExtracted: default is FirstExtracted, however when record is updated this field reflects update time

import hashlib
from datetime import datetime
from .type import Type


class DatabaseType(Type):

    __objectkey = None
    __robotname = None
    __executionid = None
    __firstextracted = None
    __lastextracted = None

    def __init__(self, name, eid):
        super().__init__()
        self.__robotname = name
        self.__executionid = eid

    def computekey(self):
        s = str([f["value"] for f in self._fields if f["part_of_key"]])
        return hashlib.md5(s.encode('utf-8')).hexdigest()

    def set_private_fields(self):
        self.__objectkey = self.computekey()
        self.__firstextracted = self.__lastextracted = datetime.now()

    def row(self, header=False, storable_only=False, with_private_fields=False):
        row = []
        if with_private_fields:
            if header:
                row = ["ObjectKey", "RobotName", "ExecutionId", "FirstExtracted", "LastExtracted"]
            else:
                row = [self.__objectkey, self.__robotname, self.__executionid, self.__firstextracted, self.__lastextracted]
        row.extend(super().row(header, storable_only))
        return row

