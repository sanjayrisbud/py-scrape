# ODBC interface to Potgres database

from .db_odbc import DatabaseInterfaceOdbc


class DatabaseInterfaceOdbcPostgres(DatabaseInterfaceOdbc):
    def create(self, dbtype):
        sql = dbtype.get_create_script()
        sql = (
            sql.replace("<objkey>", "character varying(100)")
            .replace("<rname>", "character varying(50)")
            .replace("<exid>", "character varying(50)")
            .replace("<string>", "character varying(255)")
            .replace("<integer>", "integer")
            .replace("<number>", "numeric")
            .replace("<datetime>", "timestamp without time zone")
            .replace("<text>", "text")
        )
        print(sql)
        self.execute(sql)
