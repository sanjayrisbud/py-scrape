# This is the parent class for all types.  An instance of Type corresponds to a row of data.
# Each type has a list "fields"  that represent the Type's fields.
# Each element of this list is in turn a dict to represent the dimensions of field.
# These dimensions are:
#     -> name: the name of the field
#     -> value: the value of the field
#     -> data type: the data type of the field
#     -> part of database key: boolean to define whether the field's value is to be considered
#                     when generating the instance's objectKey
#     -> storable: boolean to define whether the field can be stored
# The last 2 dimensions only apply to instances of DatabaseType


class Type:
    _fields = None

    def __init__(self):
        self._fields = []

    def __getattr__(self, item):
        if self._fields:
            for f in self._fields:
                if f["name"] == item:
                    return f["value"]
        return super().__getattribute__(item)

    def __setattr__(self, key, value):
        # case wherein a new field is added
        if isinstance(value, dict) and "part_of_key" in value:
            value["name"] = key
            return self._fields.append(value)
        # case wherein the value of a field is set
        elif self._fields:
            for f in self._fields:
                if f["name"] == key:
                    f["value"] = value
                    return
        # case wherein a Type instance's attribute is set
        super().__setattr__(key, value)

    def add_field(self, datatype, **kwargs):
        d = {"name": None, "type": datatype, "value": kwargs.get("value", None),
             "part_of_key": kwargs.get("part_of_key", False), "storable": kwargs.get("storable", False)}
        return d

    def row(self, header=False, storable_only=False):
        if header:
            i = "name"
        else:
            i = "value"
        if storable_only:
            row = [f[i] for f in self._fields if f["storable"]]
        else:
            row = [f[i] for f in self._fields]
        return row
