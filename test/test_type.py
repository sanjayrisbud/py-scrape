
from framework.db_type import DatabaseType


class TestType(DatabaseType):

    def __init__(self, name, eid):
        super().__init__(name, eid)
        self.FetchDate = self.add_field("datetime", part_of_key=True, storable=True)
        self.Id = self.add_field("integer", part_of_key=True, storable=True)
        self.Symbol = self.add_field("string", part_of_key=True, storable=True)
        self.Description = self.add_field("text")
        self.Price = self.add_field("number", storable=True)
