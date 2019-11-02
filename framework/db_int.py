# An interface which must be implemented by all classes that act as database interfaces

class DatabaseInterface:
    
    _conn = None
    _logger = None

    def __init__(self, logger):
        if logger:
            self.set_logger(logger)

    def set_logger(self, logger):
        self._logger = logger

    def query(self, script, params=None):
        raise NotImplementedError

    def find(self, dbtype):
        raise NotImplementedError

    def delete(self, dbtype):
        raise NotImplementedError

    def store(self, dbtype):
        raise NotImplementedError

    def create(self, dbtype):
        raise NotImplementedError

    def close(self):
        self._conn.close()
        self._logger = None