from src.io.writer.AbstractWriter import AbstractWriter
import cv2 as cv


class ImageWriter(AbstractWriter):
    def __init__(self, image, dimension=2, out_path=None, draw_options=None):
        self.__image = image
        self.__dimension = dimension
        self.__draw_options = draw_options
        self.__out_path = out_path

    @property
    def dimension(self):
        return self.__dimension

    @property
    def out_path(self):
        return self.__out_path

    @property
    def image(self):
        return self.__image

    @property
    def params(self):
        return self.__draw_options

    def set_dimension(self, dimension):
        self.__dimension = dimension

    def set_out_path(self, out_path):
        self.__out_path = out_path

    def set_draw_options(self, radius=None, color=None, thickness=None):
        if radius is None and 'radius' in self.__draw_options.keys():
            del self.__draw_options['radius']
        elif radius is not None:
            self.__draw_options['radius'] = radius

        if color is None and 'color' in self.__draw_options.keys():
            del self.__draw_options['color']
        elif color is not None:
            self.__draw_options['color'] = color

        if thickness is None and 'thickness' in self.__draw_options.keys():
            del self.__draw_options['thickness']
        elif thickness is not None:
            self.__draw_options['thickness'] = thickness

    def mark_landmarks_2d(self, keypoints, radius=5, color=(0,0,255), thickness=-1):
        point = list()
        for i, k in enumerate(keypoints):
            point.append(int(k))
            if (i+1) % 2 == 0:
                cv.circle(self.image, tuple(point), radius, color, thickness)
                point = list()

    def write(self, data):
        if self.__dimension == 2:
            if self.__draw_options is None:
                self.mark_landmarks_2d(data)
            else:
                self.mark_landmarks_2d(data, **self.params)

        cv.imwrite(self.out_path, self.image)

    def release(self):
        self.__image = None