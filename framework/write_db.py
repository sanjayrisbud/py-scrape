"""
    This class is responsible for SQL database operations.
    This class assumes that an appropriate ODBC driver has already been configured for the target database.
"""

import pyodbc


class DatabaseWrite:

    # Open a connection to the target database.  Also creates a cursor on this connection.
    # dsn: name of ODBC driver
    # server: common name of the SQL server (for SQL vendor-specific syntax)
    def __init__(self, dsn, server):
        self.conn = pyodbc.connect("DSN="+dsn, autocommit=True)
        self.cursor = self.conn.cursor()
        self.server = server

    # Returns a SQL "create table" query.
    # t: the type that defines the database table to create
    # name: name of the table to create    
    def queryForCreate(self, t, name):
        query = "CREATE TABLE " + name + "("
        for f in t.userFields:
            if f[2] == "date":  s = " DATETIME, "
            elif f[2] == "double":  s = " REAL, "
            elif f[2] == "int": s = " INT, "
            else: s = " VARCHAR(255), "
            query += f[0] + s
        query += "objectKey VARCHAR(50), robotName VARCHAR(25), executionId VARCHAR(30), lastExtracted DATETIME, "
        query += " PRIMARY KEY (objectKey));"
        return query

    # Creates a database table.
    # t: the type that defines the database table to create
    # dropIfExists: if True, first drops the table to be created
    def create(self, t, dropIfExists=False):
        name = str(type(t)).split(".")[1][0:-2]
        if self.server == "MySQL": name = name.lower()
        if dropIfExists:
            self.cursor.execute("DROP TABLE IF EXISTS " + name)
        query = self.queryForCreate(t, name)
        self.cursor.execute(query)

    # Insert a record in a database table.
    # t: the type that defines the record to be inserted
    # name: name of the table where the record will be inserted
    def insert(self, t, name):
        query = "INSERT INTO " + name + "(" + str([o[0] for o in t.userFields])[1:-1].replace("'", "")
        query += ", robotName, executionId, lastExtracted, objectKey) "
        query += "VALUES(" + str(["?" for o in t.userFields])[1:-1].replace("'", "") + ", ?, ?, ?, ?)"
        v = [o[1] for o in t.userFields]
        v.extend([t.housekeeping.get("robotName"), t.housekeeping.get("executionId"),
                  t.housekeeping.get("lastExtracted"), t.housekeeping.get("objectKey")])
        self.cursor.execute(query, v)

    # Update a record of a database table.
    # t: the type that defines the record that contains the update
    # name: name of the table where a record will be updated
    def update(self, t, name):
        query = "UPDATE " + name + " SET " + str([(o[0] + " = ?") for o in t.userFields])[1:-1].replace("'", "")
        query += ", robotName = ?, executionId = ?, lastExtracted = ? WHERE objectKey = ? "
        v = [o[1] for o in t.userFields]
        v.extend([t.housekeeping.get("robotName"), t.housekeeping.get("executionId"),
                  t.housekeeping.get("lastExtracted"), t.housekeeping.get("objectKey")])
        self.cursor.execute(query, v)

    # Returns a list containing the result of a SQL "select" query.
    # query: query to execute
    # w: any "where" parameters of the query
    def select(self, query, w=None):
        if w is None: l = list(self.cursor.execute(query))
        else: l = list(self.cursor.execute(query, w))
        return l

    # Store a record in a database table.  When this function is called, the "objectKey" of type "t" is computed.
    # Now check the database table where "t" should be saved.  If t's "objectKey" already exists as the objectKey of some other
    #       record in the table, update that record with t's values.  Otherwise, simply insert a new record defined by t.
    # t: the type that defines the record to be stored
    def storeInDb(self, t):
        t.generate()
        name = str(type(t)).split(".")[1][0:-2]
        if self.server == "MySQL": name = name.lower()
        self.cursor.execute("SELECT * FROM " + name + " WHERE objectKey = ?", [t.housekeeping.get("objectKey")])
        row = self.cursor.fetchone()
        if row:
            self.update(t, name)
        else:
            self.insert(t, name)

    # Close the database connection.
    def close(self):
        self.conn.close()