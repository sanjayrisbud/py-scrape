import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from framework.raw_req import RawRequests
from test.test_type import TestType


class TestRobot(RawRequests):
    def __init__(self, args):
        super().__init__(args)
        self.tt = TestType(self._robotname, self._executionid)

    def run(self):
        rs = self._database.query("select * from actor limit 3")
        for li in rs:
            print(li["last_name"])

        self.tt.FetchDate = self.date()
        self.tt.StockId = 135
        self.tt.Symbol = "ALI"
        self.tt.Description = "Ayala Land Inc"
        self.tt.Price = 51.75
        
        self._database.store(self.tt)   # insert record

        self.tt.Price = 63
        self._database.store(self.tt)   # update record

        self.tt.StockId = 76
        self.tt.Symbol = "JFC"
        self.tt.Description = "Jollibee Foods Corporation"
        self.tt.Price = 228.0
        self.logger.debug(self._database.find(self.tt))    # False
        self._database.delete(self.tt)  # nothing deleted

        self._database.store(self.tt)   # insert record
        self.logger.debug(self._database.find(self.tt))    # True
        self._database.delete(self.tt)  # 1 record deleted

if __name__ == "__main__":
    tr = TestRobot(sys.argv)
    tr.execute()
