from abc import ABC, abstractmethod


class DatabaseHandler(ABC):
    _client = None
    _database = None
    _write_requests = list()
    _PROTOCOL = ''
    _DEFAULT_PORT = int()
    _uri = ''

    def __init__(self):
        super(DatabaseHandler, self).__init__()

    @property
    def PROTOCOL(self):
        return self._PROTOCOL

    @property
    def DEFAULT_PORT(self):
        return self._DEFAULT_PORT

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, connection_data):
        if not isinstance(connection_data, tuple) and not isinstance(connection_data, str):
            raise TypeError('Connection data should be of type \'tuple\' or a \'str\'')

        if isinstance(connection_data, tuple):
            if len(connection_data) == 5:
                user, pwd, host, port, db = connection_data
                self._uri = self._PROTOCOL + '://%s:%s@%s:%s/%s' % (user, pwd, host, port, db)
            elif len(connection_data) == 4:
                user, pwd, host, port = connection_data
                self._uri = self._PROTOCOL + '://%s:%s@%s:%s' % (user, pwd, host, port)
            elif len(connection_data) == 3:
                host, port, db = connection_data
                self._uri = self._PROTOCOL + '://%s:%s/%s' % (host, port, db)
            elif len(connection_data) == 2:
                host, port = connection_data
                self._uri = self._PROTOCOL + '://%s:%s' % (host, port)
            else:
                self._uri = self._PROTOCOL + '://%s:%s' % (connection_data[0], self._DEFAULT_PORT)

        if isinstance(connection_data, str):
            self._uri = connection_data

    @property
    @abstractmethod
    def client(self):
        pass

    @client.setter
    @abstractmethod
    def client(self, connection_data):
        pass

    @property
    @abstractmethod
    def database(self):
        pass

    @database.setter
    @abstractmethod
    def database(self, db_name):
        pass

    @property
    @abstractmethod
    def write_requests(self):
        return

    @write_requests.setter
    @abstractmethod
    def write_requests(self, requests):
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def query(self, table, select, where):
        pass

    @abstractmethod
    def insert(self, table, values, bulk_write=False):
        pass

    @abstractmethod
    def update(self, table, where, values, bulk_write=False):
        pass

    @abstractmethod
    def replace(self, table, where, values, bulk_write=False):
        pass

    @abstractmethod
    def delete(self, table, where, bulk_write=False):
        pass

    @abstractmethod
    def execute_write_requests(self, table):
        pass

    @abstractmethod
    def list_databases(self):
        pass

    @abstractmethod
    def list_tables(self):
        pass

    @abstractmethod
    def count(self, table):
        self.databasea[table].count()
