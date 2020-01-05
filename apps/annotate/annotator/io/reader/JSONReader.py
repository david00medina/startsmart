from src.io.reader.AbstractReader import AbstractReader
import json


class JSONReader(AbstractReader):
    def __init__(self, path):
        self.__file = None
        self.open(path)
        self.__data = None

    @property
    def data(self):
        return self.__data

    def open(self, path):
        if self.__file is not None and not self.__file.closed:
            self.release()
        self.__file = open(path, 'r')

    def read(self):
        return json.load(self.__file)

    def release(self):
        self.__file.close()
