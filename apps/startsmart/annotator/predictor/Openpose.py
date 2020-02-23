from apps.startsmart.annotator.predictor.AbstractPredictor import AbstractPredictor
from apps.startsmart.annotator.archiver.ProjectOrganizer import ProjectOrganizer
from apps.startsmart.annotator.io.reader.VideoReader import VideoReader
from apps.startsmart.annotator.io.reader.ImageReader import ImageReader
from apps.startsmart.annotator.io.writer.ImageWriter import ImageWriter
from apps.startsmart.annotator.io.writer.JSONWriter import JSONWriter
from apps.startsmart.annotator.io.reader.JSONReader import JSONReader
from apps.startsmart.annotator.tools.FrameHandler import FrameHandler
from openpose import pyopenpose as op
import time
import os


class Openpose(AbstractPredictor):
    __predictor = 'openpose'

    def __init__(self, input, output, net_size=(800, 600), params=None, mode='video', draw_params=None, max_coco=None):
        super().__init__(ProjectOrganizer(output, self.__predictor), net_size)
        if params is None:
            params = dict()

        self.__params = params
        self.__draw_params = draw_params
        self.__max_coco_images = max_coco

        self.__rVideo = None
        self.__rImage = None
        self.__coco = None
        if mode == 'video':
            self.__rVideo = VideoReader.read(input)
        elif mode == 'image':
            self.__rImage = ImageReader(input)
        elif mode == 'cocoapi':
            self.__coco = input

        self.__time_lapse = 0
        self.__mean_time = dict()

    @property
    def predictor(self):
        return self.__predictor

    @property
    def params(self):
        return self.__params

    @property
    def draw_params(self):
        return self.__draw_params

    @property
    def video_handler(self):
        return self.__rVideo

    @property
    def image_handler(self):
        return self.__rImage

    @property
    def coco_handler(self):
        return self.__coco

    @property
    def mean_time(self):
        return self.__mean_time

    def setup(self, write_json=None, model_folder='models', render_pose=2, body=1,
              face=True, face_detector=1, face_render=-1,
              hand=True, hand_detector=3, hand_render=-1):
        if write_json is None and 'write_json' in self.__params.keys():
            del self.__params['write_json']
        elif write_json is not None:
            self.__params['write_json'] = write_json

        if model_folder is None and 'model_folder' in self.__params.keys():
            del self.__params['model_folder']
        elif model_folder is not None:
            self.__params['model_folder'] = model_folder

        if render_pose is None and 'render_pose' in self.__params.keys():
            del self.__params['render_pose']
        elif render_pose is not None:
            self.__params['render_pose'] = render_pose

        if body is None and 'body' in self.__params.keys():
            del self.__params['body']
        elif body is not None:
            self.__params['body'] = body

        if face is None and 'face' in self.__params.keys():
            del self.__params['face']
        elif face is not None:
            self.__params['face'] = face

        if face_detector is None and 'face_detector' in self.__params.keys():
            del self.__params['face_detector']
        elif face_detector is not None:
            self.__params['face_detector'] = face_detector

        if face_render is None and 'face_render' in self.__params.keys():
            del self.__params['face_render']
        elif face_render is not None:
            self.__params['face_render'] = face_render

        if hand is None and 'hand' in self.__params.keys():
            del self.__params['hand']
        elif hand is not None:
            self.__params['hand'] = hand

        if hand_detector is None and 'hand_detector' in self.__params.keys():
            del self.__params['hand_detector']
        elif hand_detector is not None:
            self.__params['hand_detector'] = hand_detector

        if hand_render is None and 'hand_render' in self.__params.keys():
            del self.__params['hand_render']
        elif hand_render is not None:
            self.__params['hand_render'] = hand_render

    def infer(self):
        self.process()

        if self.video_handler is not None:
            self.__video_processing()
        elif self.image_handler is not None:
            self.mean_time.update({self.image_handler.directory: 0})
            self.__image_processing(self.image_handler.directory)
            self.__mean_time_recorder(self.image_handler.directory,
                                      str(self.image_handler.total_images) + '_'
                                      + os.path.basename(self.image_handler.directory) + '_mean_time.json',
                                      self.image_handler.total_images)

        elif self.coco_handler is not None:
            self.mean_time.update({'coco_api': 0})
            self.__cocoapi_process('coco_api')
            self.__mean_time_recorder('coco_api', 'coco_mean_time.json', self.coco_handler.total_images)

    def __launch_job(self, title, datum, handler):
        start = time.time()
        handler.emplaceAndPop([datum])
        end = time.time()
        self.__time_lapse = end - start
        self.__mean_time[title] += self.__time_lapse

    def __cocoapi_process(self, title):
        total_images = self.coco_handler.total_images
        if self.__max_coco_images is not None:
            total_images = self.__max_coco_images

        for i in range(total_images):
            self.coco_handler.select_image(i)
            datum, handler = self.__initializer('')

            datum.cvInputData = FrameHandler.resize_frame(self.coco_handler.image,
                                                          tuple(self.coco_handler.image.shape[:2]),
                                                          self.net_size)
            datum.id = i
            name = self.coco_handler.image_info['file_name']
            datum.name = f'{self.__predictor}_{name}'

            self.__launch_job(title, datum, handler)

            self.__time_lapse_recorder(datum)

            self.__write_image_output(datum, self.coco_handler.image_info['file_name'])

    def __image_processing(self, title):
        for i in range(self.image_handler.total_images):
            self.image_handler.select_image(i)
            self.image_handler.read()
            datum, handler = self.__initializer('')

            datum.cvInputData = FrameHandler.resize_frame(self.image_handler.image,
                                                          tuple(self.image_handler.image.shape[:2]),
                                                          self.net_size)
            datum.id = i
            datum.name = f'{self.__predictor}_{os.path.splitext(self.image_handler.filename)[0]}'

            self.__launch_job(title, datum, handler)

            self.__time_lapse_recorder(datum)

            self.__write_image_output(datum, self.image_handler.filename)

    def __write_image_output(self, datum, filename):
        wImage = ImageWriter(datum.cvInputData, 2,
                             self.project.project_image_path + filename,
                             self.draw_params)
        rjson = JSONReader(self.project.project_json_path + '/' + datum.name + '_keypoints.json')
        data = rjson.read()
        for i in range(len(data['people'])):
            del data['people'][i]['pose_keypoints_2d'][2::3]
            wImage.write(data['people'][i]['pose_keypoints_2d'])
        wImage.release()

    def __video_processing(self):
        for i, (k, v) in enumerate(self.__rVideo.items()):
            datum, handler = self.__initializer(k)

            self.mean_time.update({k: 0})

            total_frames, wVideo = self.video_writer_initializer(k, v)

            for j in range(total_frames):
                ret, frame = v.read()
                datum.cvInputData = FrameHandler.resize_frame(frame, FrameHandler.get_size(v), self.net_size)

                datum.id = j
                datum.name = f'{self.__predictor}_{os.path.splitext(k)[0]}_{datum.id:010}'

                self.__launch_job(k, datum, handler)

                self.__time_lapse_recorder(datum, k)

                wVideo.write(datum.cvOutputData)

            self.__mean_time_recorder(k, 'mean_time.json', total_frames)

        wVideo.release()
        handler.stop()

    def __mean_time_recorder(self, title, out_filename, total):
        self.__mean_time[title] = self.mean_time[title] / total
        print(title + ': ' + str(self.mean_time[title]) + ' s')
        wjson = JSONWriter(self.project.project_results_path + out_filename)
        wjson.write(self.mean_time)
        wjson.release()

    def __time_lapse_recorder(self, datum, in_filename=''):
        rjson = JSONReader(
            self.project.project_json_path + os.path.splitext(in_filename)[0] + '/' + datum.name + '_keypoints.json')
        data = rjson.read()
        data.update({'time_lapse': self.__time_lapse})
        rjson.release()
        wjson = JSONWriter(
            self.project.project_json_path + os.path.splitext(in_filename)[0] + '/' + datum.name + '_keypoints.json')
        wjson.write(data)
        wjson.release()

    def __initializer(self, in_filename):
        handler = op.WrapperPython()
        self.__params['write_json'] = os.path.abspath(self.project.project_json_path + os.path.splitext(in_filename)[0])
        handler.configure(self.__params)
        handler.start()
        datum = op.Datum()
        return datum, handler

    def process(self):
        self.project.build_project_dir()

        if self.__params is None:
            self.setup(write_json=self.project.project_json_path)
