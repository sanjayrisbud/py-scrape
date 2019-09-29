import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from framework.db_type import DatabaseType
from framework.db_factory import DatabaseFactory

class TestType(DatabaseType):

    def __init__(self, name, eid):
        
        super().__init__(name, eid)
        self.FetchDate = self.add_field("datetime", part_of_key=True, storable=True)
        self.StockId = self.add_field("integer", part_of_key=True, storable=True)
        self.Symbol = self.add_field("string", part_of_key=True, storable=True)
        self.Description = self.add_field("text")
        self.Price = self.add_field("number", storable=True)

if __name__ == "__main__":
    DatabaseFactory.getdb("odbc-postgres").create(TestType(None, None))
