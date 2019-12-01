import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from framework.raw_req import RawRequests
from test.test_type import TestType


class TestRobot(RawRequests):
    def __init__(self, args):
        super().__init__(args)
        self.tt = TestType(self._robotname, self._executionid)

    def run(self):
        url = 'https://httpbin.org/ip'
        response = self.get(url)
        print(response.json())

if __name__ == "__main__":
    tr = TestRobot(sys.argv)
    tr.execute()
