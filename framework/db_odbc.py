# Interface to a database connected via ODBC

import pyodbc
from .db_int import DatabaseInterface


class DatabaseInterfaceOdbc(DatabaseInterface):

    def __init__(self, dsn, logger):
        super().__init__(logger)
        self._conn = pyodbc.connect(f"DSN={dsn}", autocommit=True)

    def execute(self, script, params=None, return_rs=False):
        if self._logger:
            self._logger.debug(f"script: {script}")
        cursor = self._conn.cursor()
        if params:
            self._logger.debug(f"params: {params}")
            rs = cursor.execute(script, params)
        else:
            rs = cursor.execute(script)

        if return_rs:
            return rs

    def query(self, script, params=None):
        rs = self.execute(script, params, return_rs=True)
        l = []
        cols = [e[0] for e in rs.description]
        for row in rs:
            d = dict(zip(cols, row))
            l.append(d)
        return l

    def find(self, dbtype):
        pass

    def delete(self, dbtype):
        pass

    def store(self, dbtype):
        dbtype.set_private_fields()
        script, params = dbtype.get_insert_clause()
        self.execute(script, params)


    def create(self, dbtype):
        raise NotImplementedError
