from django.shortcuts import get_object_or_404

from apps.startsmart.models import Annotation, Category, Image, Frame, KeypointContainer, BoundingBoxContainer


class Openpose:
    def __init__(self):
        self.__annotation = Annotation()

    @property
    def category(self):
        return self.__annotation.category

    @category.setter
    def category(self, id):
        self.__annotation.category = get_object_or_404(Category, pk=id)

    @property
    def predictor(self):
        return self.__annotation.predictor

    @predictor.setter
    def predictor(self, predictor):
        self.__annotation.predictor = predictor

    @property
    def image(self):
        return self.__annotation.image

    @image.setter
    def image(self, id):
        self.__annotation.image = get_object_or_404(Image, pk=id)

    @property
    def frame(self):
        return self.__annotation.frame

    @frame.setter
    def frame(self, id):
        self.__annotation.frame = get_object_or_404(Frame, pk=id)

    @property
    def keypoints(self):
        return self.__annotation.keypoints

    @keypoints.setter
    def keypoints(self, **kwargs):
        keypoints = KeypointContainer()
        for k, v in kwargs.items():
            if k == 'name':
                keypoints.name = v
            elif k == 'dimension':
                keypoints.dimension = v
            elif k == 'data':
                keypoints.data = v
            elif k == 'confidence':
                keypoints.confidence = v

    @property
    def bounding_box(self):
        return self.__annotation.bounding_box

    @bounding_box.setter
    def bounding_box(self, **kwargs):
        bounding_box = BoundingBoxContainer()
        for k, v in kwargs.items():
            if k == 'dimension':
                bounding_box.dimension = v
            elif k == 'min_x':
                bounding_box.min_x = v
            elif k == 'min_y':
                bounding_box.min_y = v
            elif k == 'min_z':
                bounding_box.min_z = v
            elif k == 'width':
                bounding_box.width = v
            elif k == 'height':
                bounding_box.height = v
            elif k == 'depth':
                bounding_box.depth = v
