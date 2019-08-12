"""
    This is the parent class for all robots.
    It contains different functions for use of website-specific robots.
"""

from datetime import datetime
from .gi import GenericInput
import logging,os

class Robot:

    GenericInput = GenericInput
    logger= None

    def __init__(self, args):
        name = args[0].replace("/", " ").split()[-1][:-3]
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler("logs{}{}.log".format(os.sep, name), encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(message)s"))
        file_handler.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(logging.Formatter("%(levelname)s"))
        self.logger.addHandler(stream_handler)

        print()

    # Return the current timestamp.
    def now(self):
        return datetime.today()

    # Return the current timetamp, with hours/minutes/seconds zeroed out.
    def date(self):
        d = self.now()
        return datetime(d.year, d.month, d.day, 0, 0, 0)

    def parse_input(self, args):
        if len(args) is 1:
            args.append("")
        if not str(args[1]).startswith("l1="):
            args[1] = "l1=" +  args[1]
        for i in args[1:]:
            i = str(i)
            if i.startswith("s1"):  self.GenericInput.shortText1 = i.split("=")[-1]
            if i.startswith("s2"):  self.GenericInput.shortText2 = i.split("=")[-1]
            if i.startswith("s3"):  self.GenericInput.shortText3 = i.split("=")[-1]
            if i.startswith("s4"):  self.GenericInput.shortText4 = i.split("=")[-1]
            if i.startswith("l1"):  self.GenericInput.longText1 = i.split("=")[-1]
            if i.startswith("l2"):  self.GenericInput.longText2 = i.split("=")[-1]
            if i.startswith("i1"):  self.GenericInput.integer1 = int(i.split("=")[-1])
            if i.startswith("i2"):  self.GenericInput.integer2 = int(i.split("=")[-1])
            if i.startswith("n1"):  self.GenericInput.number1 = float(i.split("=")[-1])
            if i.startswith("n2"):  self.GenericInput.number2 = float(i.split("=")[-1])
            if i.startswith("d"):  self.GenericInput.date = datetime.strptime(i.split("=")[-1], "%m/%d/%Y")

    def execute(self):
        try:
            self.run()
        except Exception as e:
            print("gotcha "+str(e))

    def run(self):
        raise NotImplementedError