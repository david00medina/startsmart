import os
from datetime import date


class ProjectOrganizer:
    def __init__(self, path, predictor=''):
        self.__path = path
        self.__predictor = predictor
        self.__today = date.today().strftime("%d-%m-%Y")

    @property
    def output_path(self):
        return self.__path

    @property
    def project_root_path(self):
        return self.__path + '/' + self.__predictor + '_' + self.__today + '/'

    @property
    def project_json_path(self):
        return self.project_root_path + 'json/'

    @property
    def project_video_path(self):
        return self.project_root_path + 'videos/'

    @property
    def project_image_path(self):
        return self.project_root_path + 'images/'

    @property
    def project_results_path(self):
        return self.project_root_path + 'results/'

    def build_project_dir(self):
        if not os.path.exists(self.project_root_path):
            os.mkdir(self.project_root_path)

        if not os.path.exists(self.project_json_path):
            os.mkdir(self.project_json_path)

        if not os.path.exists(self.project_video_path):
            os.mkdir(self.project_video_path)

        if not os.path.exists(self.project_image_path):
            os.mkdir(self.project_image_path)

        if not os.path.exists(self.project_results_path):
            os.mkdir(self.project_results_path)

    @staticmethod
    def mkdir(path, folder_name):
        folder_path = path + '/' + folder_name
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        return folder_path