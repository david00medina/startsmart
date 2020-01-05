from pymongo import MongoClient, InsertOne, ReplaceOne, UpdateMany, DeleteMany, CursorType
from .DatabaseHandler import DatabaseHandler
from bson.objectid import ObjectId


class MongoDBHandler(DatabaseHandler):
    def __init__(self, connection_data, database=None):
        super(MongoDBHandler, self).__init__()
        self._PROTOCOL = 'mongodb'
        self._DEFAULT_PORT = 27017
        self.client = connection_data
        self.database = database

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, connection_data):
        self.uri = connection_data
        self._client = MongoClient(self.uri)

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, db):
        if db is not None and isinstance(db, str):
            self._database = self._client[db]
        else:
            self._database = self.client.get_default_database()

    @property
    def write_requests(self):
        return self._write_requests

    @write_requests.setter
    def write_requests(self, requests):
        self._write_requests = requests

    def connect(self):
        self._client = MongoClient(self.uri)

    def disconnect(self):
        self.client.close()

    def query(self, table, select=None, where=None, limit=0, return_cursor=False, cursor_type='non_tailable', batch_size=500):
        if cursor_type == 'non_tailable':
            cursor_type = CursorType.NON_TAILABLE
        elif cursor_type == 'tailable':
            cursor_type = CursorType.TAILABLE
        elif cursor_type == 'tailable_await':
            cursor_type = CursorType.TAILABLE_AWAIT
        elif cursor_type == 'exhaust':
            cursor_type = CursorType.EXHAUST

        if return_cursor:
            cursor = self.database[table].find(where, select, 0, limit, cursor_type=cursor_type, batch_size=batch_size)
            return cursor

        else:
            result = list()
            for query in self.database[table].find(where, select, 0, limit):
                result.append(query)

            return result

    def insert(self, table, values, bulk_write=False):
        if bulk_write:
            self.write_requests.append(InsertOne(values))
            return None
        else:
            return self.database[table].insert_many(values)

    def update(self, table, where, values, bulk_write=False):
        if bulk_write:
            self.write_requests.append(UpdateMany(where, values))
            return None
        else:
            return self.database[table].update_many(where, values)

    def replace(self, table, where, values, bulk_write=False):
        if bulk_write:
            self.write_requests.append(ReplaceOne(where, values))
            return None
        else:
            return self.database[table].replace_one(where, values)

    def delete(self, table, where, bulk_write=False):
        if bulk_write:
            self.write_requests.append(DeleteMany(where))
            return None
        else:
            return self.database[table].delete_many(where)

    def execute_write_requests(self, table):
        result = self.database[table].bulk_write(self.write_requests)
        self.write_requests = list()
        return result

    def list_databases(self):
        databases = list()
        for db in self.client.list_databases():
            databases.append(db['name'])
        return databases

    def list_tables(self, include_system_collections=False):
        return self.database.list_collection_names(include_system_collections=include_system_collections)

    def count(self, table):
        return self.database[table].estimated_document_count()
