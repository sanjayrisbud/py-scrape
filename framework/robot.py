###
# This is the parent class for all robots.
# It contains different functions for use of website-specific robots.
###

import logging
import os
import random
import sys
from time import sleep
from datetime import datetime

from common.generic_input import GenericInput


class Robot:
    _robotname = None
    _executionid = None
    _database = None
    _email = None
    logger = None
    GenericInput = None

    def __init__(self, args):
        self._robotname = args[0].replace("/", " ").replace("\\", " ").split()[-1][:-3]
        self.GenericInput = GenericInput()
        self.parse_input(args)
        self._executionid = hash(self.now()) + hash(self.GenericInput)
        self.init_loggers()
        self.logger.debug("{} {}".format(self._robotname, self._executionid))

    def init_loggers(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(
            f"{sys.path[0]}{os.sep}logs{os.sep}{self._robotname}_{self._executionid}.log", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
        file_handler.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
        self.logger.addHandler(stream_handler)

    def now(self):
        return datetime.today()

    def date(self):
        d = self.now()
        return datetime(d.year, d.month, d.day, 0, 0, 0)

    def wait(self, min=3, max=5):
        t = random.uniform(min, max)
        self.logger.debug(f"Sleeping for {t} seconds")
        sleep(t)

    def parse_input(self, args):
        if len(args) == 1:
            args.append("")
        if not str(args[1]).startswith("l1="):
            args[1] = "l1=" + args[1]
        for i in args[1:]:
            if i.startswith("s1"):
                self.GenericInput.shortText1 = i.split("=")[-1]
            elif i.startswith("s2"):
                self.GenericInput.shortText2 = i.split("=")[-1]
            elif i.startswith("s3"):
                self.GenericInput.shortText3 = i.split("=")[-1]
            elif i.startswith("s4"):
                self.GenericInput.shortText4 = i.split("=")[-1]
            elif i.startswith("l1"):
                self.GenericInput.longText1 = i.split("=")[-1]
            elif i.startswith("l2"):
                self.GenericInput.longText2 = i.split("=")[-1]
            elif i.startswith("i1"):
                self.GenericInput.integer1 = int(i.split("=")[-1])
            elif i.startswith("i2"):
                self.GenericInput.integer2 = int(i.split("=")[-1])
            elif i.startswith("n1"):
                self.GenericInput.number1 = float(i.split("=")[-1])
            elif i.startswith("n2"):
                self.GenericInput.number2 = float(i.split("=")[-1])
            elif i.startswith("d"):
                self.GenericInput.date = datetime.strptime(i.split("=")[-1], "%m/%d/%Y")

    def execute(self):
        try:
            self.run()
            self.finalize()
        except Exception as e:
            self.logger.exception(e)

    def run(self):
        raise NotImplementedError

    def finalize(self):
        raise NotImplementedError
