# Object factory to create different database interfaces

from .db_odbc_postgres import DatabaseInterfaceOdbcPostgres
from .db_raw_mongodb import DatabaseInterfaceRawMongoDB


class DatabaseFactory:

    classdict = {
        "odbc-postgres": (DatabaseInterfaceOdbcPostgres, "dvd"),
        "mongodb": (
            DatabaseInterfaceRawMongoDB,
            "mongodb+srv://root:root@cluster0-pdn1x.mongodb.net/test?retryWrites=true&w=majority",
        ),
    }

    @staticmethod
    def getdb(name, logger=None):
        if name in DatabaseFactory.classdict:
            db = DatabaseFactory.classdict[name]
            return db[0](db[1], logger)
        else:
            if logger:
                logger.info(f"No database interface '{name}' found")
            return None
