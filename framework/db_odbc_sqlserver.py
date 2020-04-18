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
            .replace("pk_", f"{dbtype.__class__.__name__}_pk_")
        )
        print(sql)
        self.execute(sql)
