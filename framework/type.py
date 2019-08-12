"""
    This is the parent class for all types.  A type instance (object) corresponds to a row of data.
    Aside from user-defined fields, each type has the following housekeeping fields:
        -> robotName: name of the robot that created this type instance
        -> executionId: id of the robot run that created this type instance
        -> objectKey: an id for this type instance; a hash of the type's user-defined fields
                        with "part of database key" equal to True
        -> lastExtracted: the time when this instance was saved to the database
    Each type has a list "userFields"  that represent the use-defined fields.
    Each element of this list is in turn a list to represent the dimensions of each user-defined field.
    These dimensions are:
        -> name: the name of the field
        -> value: the value of the field
        -> data type: the data type of the field
        -> part of database key: boolean to define whether the field's value is to be considered
                        when generating the type instance's objectKey
"""

import inspect
import hashlib
from datetime import datetime


class Type:

    # Initialize the type instance by setting "robotName" and "executionId".
    def __init__(self):
        self.housekeeping = dict()
        self.userFields = [[]]

        frame = inspect.stack()[2]
        module = inspect.getmodule(frame[0])
        self.housekeeping.update({"robotName": module.__file__.split("/")[-1]})
        self.housekeeping.update({"executionId": str(hash(datetime.now()))})

    # Set "objectKey" and "lastExtracted".
    def generate(self):
        s = str([o[1] for o in self.userFields if(o[3] is True)])
        self.housekeeping.update({"objectKey": hashlib.md5(s.encode('utf-8')).hexdigest()})
        self.housekeeping.update({"lastExtracted": datetime.now()})

    # Set the value of the field "k".
    # k: the field to set
    # v: the new value of the field
    def set(self, k, v):
        for o in self.userFields:
            if o[0] == k : o[1] = v

    # Get the value of the field "k".
    # k: the field whose value is to be fetched
    def get(self, k):
        for o in self.userFields:
            if o[0] == k : return o[1]
