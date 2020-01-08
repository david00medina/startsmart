from src.io.reader.AbstractReader import AbstractReader
import cv2 as cv
import os


class ImageReader(AbstractReader):
    def __init__(self, path):
        self.__directory = path
        self.__images_list = list()
        for root, dirs, files in os.walk(os.path.relpath(path)):
            for file in files:
                self.__images_list.append(os.path.join(root, file))
        self.__image = None
        self.__filename = None

    @property
    def image(self):
        return self.__image

    @property
    def total_images(self):
        return len(self.__images_list)

    @property
    def directory(self):
        return self.__directory

    @property
    def filename(self):
        return self.__filename

    def select_image(self, indx):
        self.__filename = os.path.basename(self.__images_list[indx])

    def read(self):
        self.__image = cv.imread(self.directory + '/' + self.filename)
        return self.__image
