import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from framework.db_type import DatabaseType
from framework.db_factory import DatabaseFactory


class Team(DatabaseType):

    def __init__(self, name, eid):
        
        super().__init__(name, eid)
        self.FetchDate = self.add_field("datetime", part_of_key=True, storable=True)
        self.Id = self.add_field("string", part_of_key=True, storable=True)
        self.City = self.add_field("string", storable=True)
        self.Name = self.add_field("string", storable=True)
        self.URL = self.add_field("string", storable=True)
        self.Logo = self.add_field("string", storable=True)


if __name__ == "__main__":
    DatabaseFactory.getdb("odbc-sqlserver").create(Team(None, None))
