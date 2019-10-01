# Interface to a database connected via ODBC

import pyodbc
from .db_int import DatabaseInterface


class DatabaseInterfaceOdbc(DatabaseInterface):

    def __init__(self, dsn, logger):
        super().__init__(logger)
        self._conn = pyodbc.connect(f"DSN={dsn}", autocommit=True)

    def execute(self, script, params=None, returnrs=False, fetchone=False):
        if self._logger:
            self._logger.debug(f"script: {script}")
        cursor = self._conn.cursor()
        if params:
            self._logger.debug(f"params: {params}")
            rs = cursor.execute(script, params)
        else:
            rs = cursor.execute(script)

        if fetchone:
            return rs.fetchone() is not None

        if returnrs:
            return rs

    def query(self, script, params=None):
        rs = self.execute(script, params, returnrs=True)
        l = []
        cols = [e[0] for e in rs.description]
        for row in rs:
            d = dict(zip(cols, row))
            l.append(d)
        return l

    def find(self, dbtype):
        dbtype.set_private_fields()
        script, params = dbtype.get_select_clause()
        return self.execute(script, params, fetchone=True)

    def delete(self, dbtype):
        dbtype.set_private_fields()
        script, params = dbtype.get_delete_clause()
        self.execute(script, params)

    def store(self, dbtype):
        if self.find(dbtype):
            script, params = dbtype.get_update_clause()
        else:
            script, params = dbtype.get_insert_clause()
        self.execute(script, params)


    def create(self, dbtype):
        raise NotImplementedError
