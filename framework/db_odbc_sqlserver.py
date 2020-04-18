# ODBC interface to SQL Server database

from .db_odbc import DatabaseInterfaceOdbc


class DatabaseInterfaceOdbcSQLServer(DatabaseInterfaceOdbc):
    def create(self, dbtype):
        sql = dbtype.get_create_script()
        sql = (
            sql.replace("<objkey>", "varchar(100)")
            .replace("<rname>", "varchar(50)")
            .replace("<exid>", "varchar(50)")
            .replace("<string>", "nvarchar(255)")
            .replace("<integer>", "int")
            .replace("<number>", "real")
            .replace("<datetime>", "datetime")
            .replace("<text>", "text")
        )
        print(sql)
        self.execute(sql)
