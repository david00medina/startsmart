import numpy as np
import cv2 as cv


class FrameHandler:
    @staticmethod
    def adjust_scale(in_size, out_size=(800,600)):
        w, h = in_size

        if w > out_size[0]:
            scaling = out_size[0] / w
            w = int(w * scaling)
            h = int(h * scaling)

        if h > out_size[1]:
            scaling = out_size[1] / h
            w = int(w * scaling)
            h = int(h * scaling)

        return w, h

    @staticmethod
    def resize_frame(frame, in_size, out_size=(800, 600)):
        dim = FrameHandler.adjust_scale(in_size, out_size)

        resized = cv.resize(frame, dim, interpolation=cv.INTER_AREA)

        return resized

    @staticmethod
    def zoom(frame, dSize=None, fx=0, fy=0, zoom_in=False):
        interpolation = None
        if zoom_in:
            interpolation = cv.INTER_LINEAR
        else:
            interpolation = cv.INTER_AREA

        return cv.resize(frame, dSize, fx, fy, interpolation)

    @staticmethod
    def translate(frame, dSize, x, y, transparent_border=True, border_color=0):
        border_mode = None
        if transparent_border:
            border_mode = cv.BORDER_TRANSPARENT
        else:
            border_mode = cv.BORDER_CONSTANT

        M = np.float32([1,0,x], [0,1,y])

        return cv.warpAffine(frame, M, dSize, borderMode=border_mode, borderValue=border_color)

    @staticmethod
    def get_total_frames(video):
        return int(video.get(cv.CAP_PROP_FRAME_COUNT))

    @staticmethod
    def get_size(frame):
        return int(frame.get(cv.CAP_PROP_FRAME_WIDTH)), int(frame.get(cv.CAP_PROP_FRAME_HEIGHT))

    @staticmethod
    def get_fps(video):
        return int(video.get(cv.CAP_PROP_FPS))

    @staticmethod
    def get_video_frame(video):
        return video.get(cv.CAP_PROP_POS_FRAMES)

    @staticmethod
    def set_video_frame(video, frame):
        video.set(cv.CAP_PROP_POS_FRAMES, frame)

    @staticmethod
    def create_video_writer(video, video_file, out_path, size):
        return cv.VideoWriter(out_path + video_file + "/" + "video/" + video_file,
                                cv.VideoWriter_fourcc(*'mp4v'),
                                FrameHandler.get_fps(video),
                                FrameHandler.adjust_scale(FrameHandler.get_size(video), size))