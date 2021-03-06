from apps.startsmart.annotator.tools.FrameHandler import FrameHandler
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from typing import List, Dict, Type

from startsmart.settings import PREDICTION_ROOT
from .annotator.io.reader.OpenposeReader import OpenposeReader
from .annotator.predictor.OpenposePredictor import OpenposePredictor
from .annotator.tools.MemoryMonitor import MemoryMonitor
from .models import *
import cv2 as cv


class CUDNestedMixin(object):
    @staticmethod
    def cud_nested(data: List[Dict],
                   serializer: Type[serializers.Serializer]):

        insert_list = list()
        update_list = list()
        for item in data:
            item_id = item.get('id')
            if item_id:
                update_list.append(serializer(data=item))
            else:
                insert_list.append(serializer(data=item))

        if len(insert_list) > 0:
            for obj in insert_list:
                obj.is_valid(raise_exception=True)
            return insert_list

        return insert_list


class PredictorSerializer:
    def __init__(self, instance, output, predictor, mode, size, **kwargs):
        if predictor == 'Openpose':

            params = dict()
            for k, v in kwargs.items():
                params[k] = v

            path = instance.uri.url
            self.__predictor = OpenposePredictor(path, PREDICTION_ROOT + output,
                                                 size, params, mode)

    def get_results(self, index):
        monitor = None
        json_path = self.__predictor.project.project_json_path
        if not os.path.exists(json_path) or not os.listdir(json_path):
            monitor = MemoryMonitor(10)
            self.__predictor.infer()
            monitor.stop()

        op_handler = OpenposeReader(self.__predictor.project.project_json_path)
        op_handler.select_result_file(index)

        return op_handler.read(), monitor


class JointContainerSerializer(serializers.Serializer):
    name = serializers.CharField()
    indexes = serializers.ListSerializer(child=serializers.FloatField())

    def create(self, validated_data):
        joint_container = JointContainer(**validated_data)
        return joint_container

    def validate(self, attrs):
        if not isinstance(attrs['name'], str):
            raise serializers.ValidationError("'name' attribute should be str")
        if not isinstance(attrs['indexes'], list):
            raise serializers.ValidationError("'indexes' attribute should be list")

        return attrs

    class Meta:
        model = JointContainer
        fields = '__all__'


class FeatureContainerSerializer(serializers.Serializer):
    name = serializers.CharField()
    indexes = serializers.ListSerializer(child=serializers.FloatField())

    def create(self, validated_data):
        feature_container = FeatureContainer(**validated_data)
        return feature_container

    def validate(self, attrs):
        if not isinstance(attrs['name'], str):
            raise serializers.ValidationError("'name' attribute should be str")
        if not isinstance(attrs['indexes'], list):
            raise serializers.ValidationError("'indexes' attribute should be list")

        return attrs

    class Meta:
        model = FeatureContainer
        fields = '__all__'


class KeypointContainerSerializer(serializers.Serializer):
    name = serializers.CharField()
    dimension = serializers.CharField()
    data = serializers.ListSerializer(child=serializers.FloatField())
    confidence = serializers.ListSerializer(child=serializers.FloatField())

    def create(self, validated_data):
        keypoint_container = KeypointContainer(**validated_data)
        return keypoint_container

    def validate(self, attrs):
        if not isinstance(attrs['name'], str):
            raise serializers.ValidationError("'name' attribute should be str")
        if attrs['dimension'] != '2d' and attrs['dimension'] != '3d':
            raise serializers.ValidationError("'dimension' attribute should be '2d' or '3d'")
        if not isinstance(attrs['data'], list):
            raise serializers.ValidationError("'data' attribute should be list")
        if not isinstance(attrs['confidence'], list):
            raise serializers.ValidationError("'confidence' attribute should be list")

        return attrs

    class Meta:
        model = KeypointContainer
        fields = '__all__'


class BoundingBoxContainerSerializer(serializers.Serializer):
    dimension = serializers.CharField(max_length=2)
    min_x = serializers.FloatField()
    min_y = serializers.FloatField()
    min_z = serializers.FloatField(required=False)
    width = serializers.FloatField()
    height = serializers.FloatField()
    depth = serializers.FloatField(required=False)

    def create(self, validated_data):
        bounding_box_container = BoundingBoxContainer(**validated_data)
        return bounding_box_container

    def validate(self, attrs):
        if 'dimension' in attrs.keys() and attrs['dimension'] != '2d' and attrs['dimension'] != '3d':
            raise serializers.ValidationError("'dimension' attribute should be '2d' or '3d'")
        if 'min_x' in attrs.keys() and not isinstance(attrs['min_x'], float):
            raise serializers.ValidationError("'min_x' attribute should be float")
        if 'min_y' in attrs.keys() and not isinstance(attrs['min_y'], float):
            raise serializers.ValidationError("'min_y' attribute should be float")
        if 'min_z' in attrs.keys() and not isinstance(attrs['min_z'], float):
            raise serializers.ValidationError("'min_z' attribute should be float")
        if 'width' in attrs.keys() and not isinstance(attrs['width'], float):
            raise serializers.ValidationError("'width' attribute should be float")
        if 'height' in attrs.keys() and not isinstance(attrs['height'], float):
            raise serializers.ValidationError("'height' attribute should be float")
        if 'depth' in attrs.keys() and not isinstance(attrs['depth'], float):
            raise serializers.ValidationError("'depth' attribute should be float")

        return attrs

    class Meta:
        model = BoundingBoxContainer
        fields = '__all__'


class TemplateSerializer(serializers.HyperlinkedModelSerializer, CUDNestedMixin):
    name = serializers.CharField(required=False)
    bounding_box = BoundingBoxContainerSerializer(many=True, required=False)
    keypoints_name = serializers.ListSerializer(child=serializers.CharField(), required=False)
    keypoints_style = serializers.ListSerializer(child=serializers.CharField(), required=False)
    keypoints = KeypointContainerSerializer(many=True, required=False)
    joints = JointContainerSerializer(many=True, required=False)
    features = FeatureContainerSerializer(many=True, required=False)

    def __set_template(self, validated_data=None):
        self.name = None
        self.keypoints_name = None
        self.keypoints_style = None
        self.bounding_box = None
        self.keypoints = None
        self.joints = None
        self.features = None

        if 'name' in validated_data.keys():
            self.name = validated_data['name']
        if 'keypoints_name' in validated_data.keys():
            self.keypoints_name = validated_data['keypoints_name']
        if 'keypoints_style' in validated_data.keys():
            self.keypoints_style = validated_data['keypoints_style']
        if 'bounding_box' in validated_data.keys():
            self.bounding_box = self.cud_nested(validated_data['bounding_box'], BoundingBoxContainerSerializer)
        if 'keypoints' in validated_data.keys():
            self.keypoints = self.cud_nested(validated_data['keypoints'], KeypointContainerSerializer)
        if 'joints' in validated_data.keys():
            self.joints = self.cud_nested(validated_data['joints'], JointContainerSerializer)
        if 'features' in validated_data.keys():
            self.features = self.cud_nested(validated_data['features'], FeatureContainerSerializer)

    def create(self, validated_data):
        template = Template(**validated_data)
        self.__set_template(validated_data)
        if self.bounding_box is not None:
            template.bounding_box = [BoundingBoxContainer(**bbox.data) for bbox in self.bounding_box]
        if self.keypoints is not None:
            template.keypoints = [KeypointContainer(**keypoints.data) for keypoints in self.keypoints]
        if self.joints is not None:
            template.joints = [JointContainer(**joints.data) for joints in self.joints]
        if self.features is not None:
            template.features = [FeatureContainer(**features.data) for features in self.features]
        template.save()
        return template

    def update(self, instance, validated_data):
        self.__set_template(validated_data)
        if self.name is not None:
            instance.name = self.name
        if self.keypoints_name is not None:
            instance.keypoints_name = self.keypoints_name
        if self.keypoints_style is not None:
            instance.keypoints_style = self.keypoints_style
        if self.bounding_box is not None:
            instance.bounding_box = [BoundingBoxContainer(**bbox.data) for bbox in self.bounding_box]
        if self.keypoints is not None:
            instance.keypoints = [KeypointContainer(**keypoints.data) for keypoints in self.keypoints]
        if self.joints is not None:
            instance.joints = [JointContainer(**joints.data) for joints in self.joints]
        if self.features is not None:
            instance.features = [FeatureContainer(**features.data) for features in self.features]
        instance.save()
        return instance

    class Meta:
        model = Template
        fields = '__all__'


class ModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class RegionOfInterestSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='roi-detail',
        lookup_field='pk'
    )
    class Meta:
        model = RegionOfInterest
        fields = '__all__'


class LicenseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = License
        fields = '__all__'


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='image-detail',
        lookup_field='pk'
    )
    dataset = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='dataset-detail'
    )
    license = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='license-detail'
    )
    roi = serializers.HyperlinkedRelatedField(
        required=False,
        allow_null=True,
        read_only=True,
        view_name='roi-detail'
    )

    def save(self, **kwargs):
        self.instance = self.create(self.validated_data)

    def create(self, validated_data):
        image = Image()
        image.dataset = get_object_or_404(Dataset, pk=self.initial_data['dataset'])
        if 'license' in self.initial_data and self.initial_data['license'] != 'null':
            image.license = get_object_or_404(License, pk=self.initial_data['license'])
        if 'roi' in self.initial_data and self.initial_data['roi'] != 'null':
            image.roi = get_object_or_404(RegionOfInterest, pk=self.initial_data['roi'])
        image.filename = validated_data['filename']
        image.uri = validated_data['uri']
        image.save()
        cap = cv.VideoCapture('http://' + self.context['request'].get_host() + image.uri.url)
        ret, img = cap.read()
        image.height = img.shape[0]
        image.width = img.shape[1]
        image.channels = img.shape[2]
        image.save()
        cap.release()
        return image

    def update(self, instance, validated_data):
        instance.dataset = get_object_or_404(Dataset, pk=self.initial_data['dataset'])
        if 'license' in self.initial_data and self.initial_data['license'] != 'null':
            instance.license = get_object_or_404(License, pk=self.initial_data['license'])
        if 'roi' in self.initial_data and self.initial_data['roi'] != 'null':
            instance.roi = get_object_or_404(RegionOfInterest, pk=self.initial_data['roi'])
        if 'filename' in self.validated_data and self.initial_data['filename'] != 'null':
            instance.filename = validated_data['filename']
        if 'uri' in self.validated_data and self.initial_data['uri'] != 'null':
            instance.uri = validated_data['uri']
        instance.save()
        cap = cv.VideoCapture('http://' + self.context['request'].get_host() + instance.uri.url)
        ret, img = cap.read()
        instance.height = img.shape[0]
        instance.width = img.shape[1]
        instance.channels = img.shape[2]
        instance.save()
        cap.release()

    class Meta:
        model = Image
        fields = '__all__'


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='video-detail',
        lookup_field='pk'
    )
    dataset = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='roi-detail'
    )
    license = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='license-detail'
    )

    def save(self, **kwargs):
        self.instance = self.create(self.validated_data)

    def create(self, validated_data):
        video = Video()
        video.dataset = get_object_or_404(Dataset, pk=self.initial_data['dataset'])
        if 'license' in self.initial_data and self.initial_data['license'] != 'null':
            video.license = get_object_or_404(License, pk=self.initial_data['license'])
        video.filename = validated_data['filename']
        video.uri = validated_data['uri']
        video.save()
        cVideo = cv.VideoCapture('http://' + self.context['request'].get_host() + video.uri.url)
        video.total_frames = FrameHandler.get_total_frames(cVideo)
        ret, img = cVideo.read()
        video.height = img.shape[0]
        video.width = img.shape[1]
        video.channels = img.shape[2]
        video.save()
        return video

    def update(self, instance, validated_data):
        instance.dataset = get_object_or_404(Dataset, pk=self.initial_data['dataset'])
        if 'license' in self.initial_data and self.initial_data['license'] != 'null':
            instance.license = get_object_or_404(License, pk=self.initial_data['license'])
        if 'filename' in self.validated_data and self.initial_data['filename'] != 'null':
            instance.filename = validated_data['filename']
        if 'uri' in self.validated_data and self.initial_data['uri'] != 'null':
            instance.uri = validated_data['uri']
        instance.save()
        cVideo = cv.VideoCapture('http://' + self.context['request'].get_host() + instance.uri.url)
        instance.total_frames = FrameHandler.get_total_frames(cVideo)
        ret, img = cVideo.read()
        instance.height = img.shape[0]
        instance.width = img.shape[1]
        instance.channels = img.shape[2]
        instance.save()

    def get_frame(self, instance, frame_no):
        cVideo = cv.VideoCapture(instance.uri.url[1:])
        cVideo.set(cv.CAP_PROP_POS_FRAMES, int(frame_no))
        ret, frame = cVideo.read()
        cv.imwrite(instance.id + frame_no, frame)
        return frame


    class Meta:
        model = Video
        fields = '__all__'


class FrameSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='frame-detail',
        lookup_field='pk'
    )
    video = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='video-detail'
    )
    roi = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='roi-detail'
    )

    def save(self, **kwargs):
        self.instance = self.create(self.validated_data)

    def create(self, validated_data):
        frame = Frame()
        frame.video = get_object_or_404(Video, pk=self.initial_data['video'])
        if 'roi' in self.initial_data:
            frame.roi = get_object_or_404(RegionOfInterest, pk=self.initial_data['roi'])
        if 'frame_no' in validated_data:
            frame.frame_no = validated_data['frame_no']
        frame.uri = validated_data['uri']
        frame.save()
        cap = cv.VideoCapture('http://' + self.context['request'].get_host() + frame.uri.url)
        ret, img = cap.read()
        frame.height = img.shape[0]
        frame.width = img.shape[1]
        frame.channels = img.shape[2]
        frame.save()
        cap.release()
        return frame

    def update(self, instance, validated_data):
        instance.video = get_object_or_404(Video, pk=self.initial_data['video'])
        if 'roi' in self.initial_data:
            instance.roi = get_object_or_404(RegionOfInterest, pk=self.initial_data['roi'])
        if 'uri' in self.validated_data:
            instance.uri = validated_data['uri']
        if 'frame_no' in validated_data:
            instance.frame_no = validated_data['frame_no']
        instance.save()
        cap = cv.VideoCapture('http://' + self.context['request'].get_host() + instance.uri.url)
        ret, img = cap.read()
        instance.height = img.shape[0]
        instance.width = img.shape[1]
        instance.channels = img.shape[2]
        instance.save()
        cap.release()

    class Meta:
        model = Frame
        fields = '__all__'


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class DatasetSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='dataset-detail',
        lookup_field='pk'
    )
    project = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='project-detail'
    )

    def save(self, **kwargs):
        self.instance = self.create(self.validated_data)

    def create(self, validated_data):
        dataset = Dataset()
        dataset.project = get_object_or_404(Project, pk=self.initial_data['project'])
        dataset.name = validated_data['name']
        dataset.save()
        return dataset

    def update(self, instance, validated_data):
        instance.project = get_object_or_404(Project, pk=self.initial_data['project'])
        instance.name = validated_data['name']
        instance.save()

    class Meta:
        model = Dataset
        fields = '__all__'


class AnnotationSerializer(serializers.HyperlinkedModelSerializer, CUDNestedMixin):
    url = serializers.HyperlinkedIdentityField(
        view_name='dataset-detail',
        lookup_field='pk'
    )
    category = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='category-detail'
    )
    image = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='image-detail'
    )
    frame = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='frame-detail'
    )
    keypoints = KeypointContainerSerializer(many=True, required=False)
    bounding_box = BoundingBoxContainerSerializer(many=True, required=False)

    def save(self, **kwargs):
        self.instance = self.create(self.validated_data)

    def create(self, validated_data):
        annotation = Annotation()
        if 'category' in self.initial_data.keys():
            annotation.category = get_object_or_404(Category, pk=self.initial_data['category'])
        if 'entity_id' in validated_data:
            annotation.entity_id = validated_data['entity_id']
        if 'predictor' in validated_data:
            annotation.predictor = validated_data['predictor']
        if 'image' in self.initial_data.keys():
            annotation.image = get_object_or_404(Image, pk=self.initial_data['image'])
        if 'video' in self.initial_data.keys():
            if 'frame' in self.initial_data.keys():
                frame = self.initial_data['frame']
            else:
                frame = self.initial_data['result'].frame
                frame.video = get_object_or_404(Video, pk=self.initial_data['video'])
                cVideo = cv.VideoCapture(frame.video.uri.url[1:])
                cVideo.set(cv.CAP_PROP_POS_FRAMES, frame.frame_no)
                ret, out = cVideo.read()
                cv.imwrite('media/frames/' + str(frame.video.dataset.id)
                           + '/' + frame.video.md5sum + '/' + str(frame.frame_no) + '.jpg',
                           out)
                frame.save()

            annotation.frame = frame

        annotation.keypoints = self.initial_data['result'].keypoints
        annotation.bounding_box = self.initial_data['result'].bounding_box
        annotation.save()

        return annotation

    def update(self, instance, validated_data):
        if 'category' in self.initial_data.keys():
            instance.category = get_object_or_404(Category, pk=self.initial_data['category'])
        if 'entity_id' in validated_data:
            instance.entity_id = validated_data['entity_id']
        if 'predictor' in validated_data:
            instance.entity_id = validated_data['predictor']
        if 'image' in self.initial_data.keys():
            instance.image = get_object_or_404(Image, pk=self.initial_data['image'])
        if 'frame' in self.initial_data.keys():
            instance.frame = get_object_or_404(Frame, pk=self.initial_data['frame'])
        if 'bounding_box' in self.initial_data.keys():
            serializer = self.cud_nested(validated_data['bounding_box'], BoundingBoxContainerSerializer)
            instance.bounding_box = [BoundingBoxContainer(**bounding_box.data) for bounding_box in serializer]
        if 'keypoints' in self.initial_data.keys():
            serializer = self.cud_nested(validated_data['keypoints'], KeypointContainerSerializer)
            instance.keypoints = [KeypointContainer(**keypoint.data) for keypoint in serializer]
        instance.save()

    class Meta:
        model = Annotation
        fields = '__all__'


class LibrarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'
