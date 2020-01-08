from rest_framework.fields import empty
from rest_framework import serializers
from .models import *


class JointContainerSerializer(serializers.ModelSerializer):
    dimension = serializers.CharField(max_length=2)
    min_x = serializers.FloatField()
    min_y = serializers.FloatField()
    min_z = serializers.FloatField()
    width = serializers.FloatField()
    height = serializers.FloatField()
    depth = serializers.FloatField()

    class Meta:
        model = JointContainer
        fields = '__all__'


class FeatureContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureContainer
        fields = '__all__'


class KeypointContainerSerializer(serializers.ModelSerializer):
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
    bounding_box = BoundingBoxContainerSerializer(many=True)

    class Meta:
        model = Template
        fields = '__all__'

    def get_bounding_box_method(self, obj):
        return_data = None
        if type(obj['bounding_box']) == list:
            bounding_box_list = []
            for item in obj['bounding_box']:
                bounding_box_dict = item
                for key in list(bounding_box_dict.keys()):
                    if key.startswith('_'):
                        bounding_box_dict.pop(key)
                bounding_box_list.append(bounding_box_dict)
            return_data = bounding_box_list
        else:
            bounding_box_dict = obj['bounding_box']
            for key in list(bounding_box_dict.keys()):
                if key.startswith('_'):
                    bounding_box_dict.pop(key)
            return_data = bounding_box_dict

        self.data.update({'bounding_box': return_data})



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
