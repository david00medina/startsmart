from apps.startsmart.annotator.predictor.AbstractPredictor import AbstractPredictor
from apps.startsmart.annotator.archiver.ProjectOrganizer import ProjectOrganizer
from apps.startsmart.annotator.io.reader.VideoReader import VideoReader
from apps.startsmart.annotator.io.writer.VideoWriter import VideoWriter
from apps.startsmart.annotator.tools.FrameHandler import FrameHandler
import dlib
import json
import time
import os


class DLIBPredictor(AbstractPredictor):
    __predictor = 'DLIB'

    def __init__(self, in_path, out_path, net_size=(800, 600), params=dict()):
        super().__init__(ProjectOrganizer(out_path, self.__predictor), net_size)
        self.__videos = VideoReader.read(in_path)
        self.__params = params
        self.__face_detector = None
        self.__face_predictor = None
        self.__time_lapse = 0
        self.__mean_time = 0

    @property
    def params(self):
        return self.__params

    @property
    def predictor(self):
        return self.predictor

    def setup(self, face_detector='models/face/mmod_human_face_detector.dat',
              face_predictor='models/face/shape_predictor_68_face_landmarks.dat',
              upsampling = 1):
        if face_detector is None and 'face_detector' in self.__params.keys():
            del self.__params['face_detector']
        elif face_detector is not None:
            self.__params['face_detector'] = face_detector

        if face_predictor is None and 'face_predictor' in self.__params.keys():
            del self.__params['face_predictor']
        elif face_predictor is not None:
            self.__params['face_predictor'] = face_predictor

        self.__params['upsampling'] = upsampling

    def infer(self):
        self.process()

        for i, (k, v) in enumerate(self.__videos.items()):
            ProjectOrganizer.mkdir(self.project.project_json_path, os.path.splitext(k)[0])
            ProjectOrganizer.mkdir(self.project.project_video_path, os.path.splitext(k)[0])

            total_frames, wVideo = super().video_writer_initializer(k, v)

            self.__mean_time.update({k: 0})

            for j in range(total_frames):
                ret, frame = v.read()
                rFrame = FrameHandler.resize_frame(frame, FrameHandler.get_size(v), self.net_size)

                faces = self.infer_region(rFrame)

                start = time.time()
                data = self.infer_keypoints(frame, faces)
                end = time.time()
                self.__time_lapse = end - start
                data['time_lapse'] = self.__time_lapse
                self.__mean_time[k] += self.__time_lapse

                json_name = f'{self.__predictor}_{os.path.splitext(k)[0]}_{j:09}.json'

                with open(self.project.project_json_path + os.path.splitext(k)[0] + "/" + json_name, "w") as wFile:
                    json.dump(data, wFile)

            self.__mean_time[k] = self.__mean_time[k] / total_frames
            print(k + ': ' + str(self.mean_time[k]) + ' ms')

            with open(self.project.project_results_path + 'mean_time.json', 'w') as file:
                json.dump(self.__mean_time, file)

    def process(self):
        self.project.build_project_dir()

        if 'face_predictor' not in self.__params or 'face_detector' not in self.__params:
            self.setup()

        if 'face_detector' in self.__params.keys():
            self.__face_detector = dlib.cnn_face_detection_model_v1(self.__params['face_detector'])

        if 'face_predictor' in self.__params.keys():
            self.__face_predictor = dlib.shape_predictor(self.__params['face_predictor'])

    def infer_region(self, frame):
        return self.__face_detector(frame, self.__params['upsampling'])

    def infer_keypoints(self, frame, faces):
        data = {'people': list()}

        for i, face in enumerate(faces):
            kp = self.__face_predictor(frame, face.rect)
            data['people'].append({'face_keypoints_2d': list()})

            for j in range(kp.num_parts):
                data['people'][i]['face_keypoints_2d'].extend([kp.part(j).x, kp.part(j).y])

        return data

    @property
    def mean_time(self):
        return self.__mean_time
