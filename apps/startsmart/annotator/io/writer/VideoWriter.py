from apps.startsmart.annotator.io.writer.AbstractWriter import AbstractWriter
from apps.startsmart.annotator.tools.FrameHandler import FrameHandler
import os
import cv2 as cv


class VideoWriter(AbstractWriter):
    def __init__(self, cVideo, out_file, video_format='mp4v', size=(800, 600)):
        self.wVideo = VideoWriter.__create_video_writer(cVideo, out_file, video_format, size)

    @staticmethod
    def __create_video_writer(cVideo, out_file, video_format, size):
        return cv.VideoWriter(out_file,
                              cv.VideoWriter_fourcc(*video_format),
                              FrameHandler.get_fps(cVideo),
                              FrameHandler.adjust_scale(FrameHandler.get_size(cVideo), size))

    def write(self, img):
        self.wVideo.write(img)

    def release(self):
        self.wVideo.release()
