import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from framework.raw_req import RawRequests
from framework.csv_int import CsvInterface
from test.test_type import TestType


class TestRobot(RawRequests):
    def __init__(self, args):
        super().__init__(args)
        self.csv = CsvInterface("test.csv")
        self.tt = TestType(self._robotname, self._executionid)

    def run(self):
        print(self.tt.row(header=True))
        self.tt.FetchDate = self.date()
        self.tt.Id = 135
        self.tt.Symbol = "ALI"
        self.tt.Description = "Ayala Land Inc"
        self.tt.Price = 51.75
        print(self.tt.row())
        print(self.tt.row(header=True, storable_only=True))
        print(self.tt.row(storable_only=True))
        print(self.tt.row(header=True, storable_only=True, with_private_fields=True))
        self.csv.writerow(self.tt.row(header=True, storable_only=True, with_private_fields=True))
        print(self.tt.row(storable_only=True, with_private_fields=True))
        self.csv.writerow(self.tt.row(storable_only=True, with_private_fields=True))
        self.tt.set_private_fields()
        print(self.tt.row(storable_only=True, with_private_fields=True))
        self.csv.writerow(self.tt.row(storable_only=True, with_private_fields=True))
        self.tt.Id = 76
        self.tt.Symbol = "JFC"
        self.tt.Description = "Jollibee Foods Corporation"
        self.tt.Price = 228.0
        self.tt.set_private_fields()
        print(self.tt.row(storable_only=True, with_private_fields=True))
        self.csv.writerow(self.tt.row(storable_only=True, with_private_fields=True))
        self.tt.Id = 432
        self.tt.set_private_fields()
        print(self.tt.row(storable_only=True, with_private_fields=True))
        self.csv.writerow(self.tt.row(storable_only=True, with_private_fields=True))
        self.tt.Price = 233.5
        self.tt.set_private_fields()
        print(self.tt.row(storable_only=True, with_private_fields=True))
        self.csv.writerow(self.tt.row(storable_only=True, with_private_fields=True))
        if not self.csv.isclosed():
            print("closing")
            self.csv.close()


if __name__ == "__main__":
    tr = TestRobot(sys.argv)
    tr.execute()
