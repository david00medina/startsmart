from rest_framework import serializers
from django.db.models.query import QuerySet
from typing import List, Dict, Type
from .models import *


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
    dimension = serializers.CharField(required=True, max_length=2)
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
        if attrs['dimension'] != '2d' and attrs['dimension'] != '3d':
            raise serializers.ValidationError("'dimension' attribute should be '2d' or '3d'")
        if not isinstance(attrs['min_x'], float):
            raise serializers.ValidationError("'min_x' attribute should be float")
        if not isinstance(attrs['min_y'], float):
            raise serializers.ValidationError("'min_y' attribute should be float")
        if 'min_z' in attrs.keys() and not isinstance(attrs['min_z'], float):
            raise serializers.ValidationError("'min_z' attribute should be float")
        if not isinstance(attrs['width'], float):
            raise serializers.ValidationError("'width' attribute should be float")
        if not isinstance(attrs['height'], float):
            raise serializers.ValidationError("'height' attribute should be float")
        if 'depth' in attrs.keys() and not isinstance(attrs['depth'], float):
            raise serializers.ValidationError("'depth' attribute should be float")

        return attrs

    class Meta:
        model = BoundingBoxContainer
        fields = '__all__'


class TemplateSerializer(serializers.ModelSerializer, CUDNestedMixin):
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


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class RegionOfInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionOfInterest
        fields = '__all__'


class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frame
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class FrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frame
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = '__all__'


class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = '__all__'
