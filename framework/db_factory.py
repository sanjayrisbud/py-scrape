# Object factory to create different database interfaces

from .db_odbc_postgres import DatabaseInterfaceOdbcPostgres


class DatabaseFactory:

    classdict = {
        "odbc-postgres": DatabaseInterfaceOdbcPostgres,
    }
    
    @staticmethod
    def getdb(name, logger=None):
        if name in DatabaseFactory.classdict:
            return DatabaseFactory.classdict[name]("dvd", logger)
        else:
            if logger:
                logger.info(f"No database interface '{name}' found")
            return None
