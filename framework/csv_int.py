# An interface to an output CSV file

import csv
import os, sys


class CsvInterface:

    __path = None
    __filename = None
    __fp = None
    __writer = None
    __closed = True

    def __init__(self, filename, **kwargs):
        self.__filename = filename
        self.__path = kwargs.get("path", f"{sys.path[0]}{os.sep}out{os.sep}")
        d = kwargs.get("delimiter", ",")
        q = kwargs.get("quoting", csv.QUOTE_ALL)
        self.__fp = open(
            self.__path + self.__filename, "w", encoding="utf-8", newline=""
        )
        self.__writer = csv.writer(self.__fp, delimiter=d, quoting=q, quotechar='"')
        self.__closed = False

    def writerow(self, row):
        self.__writer.writerow(row)

    def close(self):
        self.__fp.close
        self.__closed = True

    def isclosed(self):
        return self.__closed
