import os

from apps.startsmart.annotator.io.reader.AbstractReader import AbstractReader
from apps.startsmart.annotator.io.reader.JSONReader import JSONReader


class OpenposeReader(AbstractReader):
    def __init__(self, path=None, index=None):
        self.__directory = path
        self.__filename = None
        self.__json_handler = None
        self.__result_files = list()
        self.__populate_with_results()

        if path is not None:
            self.select_result_file(1 if index else 2)

    @property
    def directory(self):
        return self.__directory

    @property
    def filename(self):
        return self.__filename

    @property
    def result_files(self):
        return self.__result_files

    @property
    def json_handler(self):
        return self.__json_handler

    @property
    def total_results(self):
        return len(self.__result_files)

    def __populate_with_results(self):
        for root, dirs, files in os.walk(os.path.relpath(self.__directory)):
            for file in files:
                self.__images_list.append(os.path.join(root, file))

    def select_result_file(self, index):
        self.__filename = self.__result_files[index]

        if self.__json_handler:
            self.__json_handler.release()

        self.__json_handler = JSONReader(self.__filename)

    def read(self):
        json = self.__json_handler.read()

        print(json)