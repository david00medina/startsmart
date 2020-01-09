from rest_framework.fields import empty
from rest_framework import serializers
from djongo import models
from .models import *


class JointContainerSerializer(serializers.Serializer):
    name = serializers.CharField()
    indexes = serializers.ListSerializer(child=serializers.FloatField())

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
        model = BoundingBoxContainer()
        fields = '__all__'


class TemplateSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    bounding_box = BoundingBoxContainerSerializer(many=True, required=False)
    keypoints_name = serializers.ListSerializer(child=serializers.CharField())
    keypoints_style = serializers.ListSerializer(child=serializers.CharField())
    keypoints = KeypointContainerSerializer(many=True, required=False)
    joints = JointContainerSerializer(many=True, required=False)
    features = FeatureContainerSerializer(many=True, required=False)

    def set_template(self, validated_data):
        self.name = validated_data['name']

        if 'bounding_box' in validated_data:
            self.bounding_box = validated_data['bounding_box']

        self.keypoints_name = validated_data['keypoints_name']
        self.keypoints_style = validated_data['keypoints_style']

        if 'keypoints' in validated_data:
            self.keypoints = validated_data['keypoints']

        if 'joints' in validated_data:
            self.joints = validated_data['joints']

        if 'features' in validated_data:
            self.features = validated_data['features']

    def create(self, validated_data):
        template = Template(**validated_data)
        template.save()
        return template

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
