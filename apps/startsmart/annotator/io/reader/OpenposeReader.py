from collections import Counter
import os

from apps.startsmart.annotator.io.reader.AbstractReader import AbstractReader
from apps.startsmart.annotator.io.reader.JSONReader import JSONReader
from apps.startsmart.annotator.models.Openpose import Openpose
from apps.startsmart.models import Frame


class OpenposeReader(AbstractReader):
    def __init__(self, path=None, index=None):
        self.__directory = path
        self.__filename = None
        self.__json_handler = None
        self.__result_files = list()
        self.__populate_with_results()
        self.__people = list()

        if path is not None:
            self.select_result_file(index if index else 0)

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

    @property
    def time_lapse(self):
        return self.__time_lapse

    def __populate_with_results(self):
        for root, dirs, files in os.walk(os.path.relpath(self.__directory)):
            for file in files:
                self.__result_files.append(os.path.join(root, file))

    def __load_keypoints(self, person, key_words, dimension):
        keypoint_data = Counter()
        keypoint_data['dimension'] = str(dimension) + 'd'

        if len(key_words) == 3:
            keypoint_data['name'] = key_words[0]
        elif len(key_words) == 4:
            keypoint_data['name'] = key_words[0] + "_" + key_words[1]

        keypoint_data['data'] = list()
        keypoint_data['confidence'] = list()

        for i, point in enumerate(person[keypoint_data['name'] + '_keypoints_' + keypoint_data['dimension']]):
            if (i + 1) % (dimension + 1) == 0:
                keypoint_data['confidence'].append(point)
            else:
                keypoint_data['data'].append(point)

        return keypoint_data

    def __load_bounding_box(self, key, points, dimension):
        if key == 'pose_keypoints_' + str(dimension) + 'd':
            data = list(filter(lambda num: num != 0, points))

            if len(data) == 0:
                return None

            x = data[::dimension]
            y = data[1::dimension]

            bbox_data = Counter()
            bbox_data['dimension'] = dimension
            bbox_data['min_x'] = min(x)
            bbox_data['min_y'] = min(y)
            bbox_data['width'] = max(x) - min(x)
            bbox_data['height'] = max(y) - min(y)

            if dimension == 3:
                z = data[2::dimension]
                bbox_data['min_z'] = min(z)
                bbox_data['depth'] = max(z) - min(z)

            return bbox_data

    def select_result_file(self, frame_no):
        self.__filename = self.__result_files[self.__find_frame_index(frame_no)]
        self.__people = list()

        if self.__json_handler:
            self.__json_handler.release()

        self.__json_handler = JSONReader(self.__filename)

    def read(self):
        json = self.__json_handler.read()

        filename = self.json_handler.filename

        frame = Frame()
        frame.frame_no = int(os.path.splitext(filename)[0].split('_')[-2])
        frame.time_lapse = json['time_lapse']

        people = json['people']

        for person in people:
            annotation = Openpose()
            annotation.frame = frame
            self.__people.append(annotation)

            annotation.predictor = 'Openpose'
            keypoints = list()
            bounding_box = list()

            for k, v in person.items():

                key_words = k.split('_')

                try:
                    dimension = int(key_words[-1][0])

                    keypoint_data = self.__load_keypoints(person, key_words, dimension)

                    if len(keypoint_data['data']) > 0:
                        keypoints.append(keypoint_data)

                    bbox = self.__load_bounding_box(k, keypoint_data['data'], dimension)
                    if bbox:
                        bounding_box.append(bbox)

                except ValueError:
                    continue

            annotation.keypoints = keypoints
            annotation.bounding_box = bounding_box

        return self.__people

    def __find_frame_index(self, frame_no):
        for i, filename in enumerate(self.__result_files):
            current_frame = int(os.path.splitext(filename)[0].split('_')[-2])

            if current_frame == frame_no:
                return i