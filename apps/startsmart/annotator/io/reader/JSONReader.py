from apps.startsmart.annotator.io.reader.AbstractReader import AbstractReader
import json
import os


class JSONReader(AbstractReader):
    def __init__(self, path):
        self.__path = path
        self.filename = path
        self.__file = None
        self.open(path)

    @property
    def filename(self):
        return self.__filename

    @filename.setter
    def filename(self, path):
        self.__filename = os.path.basename(path)

    def open(self, path):
        if self.__file is not None and not self.__file.closed:
            self.release()
        self.__file = open(path, 'r')

    def read(self):
        return json.load(self.__file)

    def release(self):
        self.__file.close()
