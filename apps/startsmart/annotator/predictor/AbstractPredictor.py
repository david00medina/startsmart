from apps.startsmart.annotator.archiver.ProjectOrganizer import ProjectOrganizer
from apps.startsmart.annotator.io.writer.VideoWriter import VideoWriter
from apps.startsmart.annotator.io.writer.ImageWriter import ImageWriter
from apps.startsmart.annotator.tools.FrameHandler import FrameHandler
from abc import ABC, abstractmethod
import os

class AbstractPredictor(ABC):
    def __init__(self, project, net_size):
        self.__project = project
        self.__net_size = net_size

    @property
    def project(self):
        return self.__project

    @property
    def net_size(self):
        return self.__net_size

    @abstractmethod
    def infer(self):
        pass

    @abstractmethod
    def process(self):
        pass

    def set_net_size(self, net_size):
        self.__net_size = net_size

    def render_video(self):
        pass

    def video_writer_initializer(self, in_filename, cVideo):
        total_frames = FrameHandler.get_total_frames(cVideo)
        FrameHandler.set_video_frame(cVideo, 0)
        video_folder = ProjectOrganizer.mkdir(self.__project.project_video_path, os.path.splitext(in_filename)[0])
        wVideo = VideoWriter(cVideo, os.path.abspath(video_folder + '/' + in_filename), 'mp4v', self.__net_size)
        return total_frames, wVideo
