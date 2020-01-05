from src.io.reader.AbstractReader import AbstractReader
import cv2 as cv
import os


class VideoReader(AbstractReader):
    def __init__(self, path):
        self.path = path
        self.__videos = VideoReader.read(self.path)

    @property
    def video_dict(self):
        return VideoReader.read(self.path)

    @staticmethod
    def read(path):
        videos = list()
        for root, dirs, files in os.walk(os.path.relpath(path)):
            for file in files:
                videos.append(os.path.join(root, file))

        rVideo = VideoReader.__generate_video_capture(videos)

        if None in rVideo:
            return None

        return rVideo

    @staticmethod
    def __generate_video_capture(filename):
        videos = {os.path.basename(k): cv.VideoCapture(cv.samples.findFileOrKeep(v))
                  for (k, v) in zip(filename, filename)}

        for k, v in videos.items():
            if not v.isOpened():
                print('Unable to open: \'' + k + '\'')
                return None

        return videos

    def get_video_capture(self, filename=None):
        if filename is None:
            return self.__videos

        return self.__videos[os.path.basename(filename)]
