"""
    This class is responsible for writing types to a csv file.
    The file is written one row at a time.
    Only the user-defined fields are written; the housekeeping fields are omitted.
"""

import csv


class CsvWrite:

    # Open a csv for writing.
    # filename: name f the csv to be written
    def __init__(self, filename):
        self.filename = filename
        self.ofile = open(filename, "w", newline="", encoding="utf-8")
        self.writer = csv.writer(self.ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    # Write out a row containing the field names.
    # t: the type that defines the row to be written
    def writeHeader(self, t):
        l = [o[0] for o in t.userFields]
        self.writer.writerow(l)

    # Write out a row containing the field values.
    # t: the type that defines the row to be written
    def writeRow(self, t):
        l = [o[1] for o in t.userFields]
        self.writer.writerow(l)

    # Close the csv.
    def close(self):
        self.ofile.close()
