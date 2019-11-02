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
from typing import List

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
        return hashlib.md5(s.encode("utf-8")).hexdigest()

    def set_private_fields(self):
        self.__objectkey = self.computekey()
        self.__firstextracted = self.__lastextracted = datetime.now()

    def row(self, header=False, storable_only=False, with_private_fields=False):
        row = []
        if with_private_fields:
            if header:
                row = [
                    "ObjectKey",
                    "RobotName",
                    "ExecutionId",
                    "FirstExtracted",
                    "LastExtracted",
                ]
            else:
                row = [
                    self.__objectkey,
                    self.__robotname,
                    self.__executionid,
                    self.__firstextracted,
                    self.__lastextracted,
                ]
        row.extend(super().row(header, storable_only))
        return row

    def get_create_script(self):
        s = f"CREATE TABLE {self.__class__.__name__} "
        s += """(
            ObjectKey <objkey>,
            RobotName <rname>,
            ExecutionId <exid>,
            FirstExtracted <datetime>,
            LastExtracted <datetime>,
            <cols>
            CONSTRAINT pk_ObjKey PRIMARY KEY (ObjectKey)
        )"""
        cols = ""
        for f in self._fields:
            if f["storable"]:
                cols += "{} <{}>, ".format(f["name"], f["type"])
        s = s.replace("<cols>", cols)
        return s

    def get_select_clause(self):
        query = f"SELECT ObjectKey FROM {self.__class__.__name__} WHERE ObjectKey = ?"
        return query, (self.__objectkey)

    def get_delete_clause(self):
        query = f"DELETE FROM {self.__class__.__name__} WHERE ObjectKey = ?"
        return query, (self.__objectkey)

    def get_insert_clause(self):
        query = ""
        row_dict = self.get_fields_and_values("insert")
        fields = []
        values = []
        for k, v in row_dict.items():
            if v:
                fields.append(k)
                values.append(v)
        query = "INSERT INTO {}{} VALUES{}".format(
            self.__class__.__name__,
            str(tuple(fields)).replace("'", ""),
            str(tuple(["?" for _ in fields])).replace("'", ""),
        )
        return query, tuple(values)

    def get_update_clause(self):
        query = ""
        row_dict = self.get_fields_and_values("update")
        fields = []
        values = []
        fields.append("LastExtracted = ?")
        values.append(self.__lastextracted)
        for k, v in row_dict.items():
            if v:
                fields.append(f"{k} = ?")
                values.append(v)
            else:
                fields.append(f"{k} = NULL")
        values.append(self.__objectkey)
        query = "UPDATE {} SET {} WHERE ObjectKey = ?".format(
            self.__class__.__name__, str(fields).replace("'", "").strip("[]")
        )
        return query, tuple(values)

    def get_fields_and_values(self, script):
        if script == "insert":
            wpf = True
        else:
            wpf = False
        fields = self.row(header=True, storable_only=True, with_private_fields=wpf)
        values = self.row(header=False, storable_only=True, with_private_fields=wpf)
        return dict(zip(fields, values))

