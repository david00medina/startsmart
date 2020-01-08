from src.io.writer.AbstractWriter import AbstractWriter
import json


class JSONWriter(AbstractWriter):
    def __init__(self, path, append=False):
        mode = 'w'
        if append:
            mode = 'r+'

        self.__file = None
        self.open(path, mode)

    def open(self, path, mode):
        if self.__file is not None and not self.__file.closed:
            self.release()
        self.__file = open(path, mode)

    def write(self, data):
        json.dump(data, self.__file)

    def release(self):
        self.__file.close()