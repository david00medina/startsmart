from rest_framework import serializers
from django.db.models.query import QuerySet
from typing import List, Dict, Type
from .models import *


class CUDNestedMixin(object):
    @staticmethod
    def cud_nested(queryset: QuerySet,
                   data: List[Dict],
                   serializer: Type[serializers.Serializer],
                   context: Dict):

        updated_ids = list()
        for_create = list()
        for item in data:
            item_id = item.get('id')
            if item_id:
                instance = queryset.get(id=item_id)
                update_serializer = serializer(
                    instance=instance,
                    data=item,
                    context=context
                )
                update_serializer.is_valid(raise_exception=True)
                update_serializer.save()
                updated_ids.append(instance.id)
            else:
                for_create.append(item)

        if queryset is not None:
            delete_queryset = queryset.exclude(id__in=updated_ids)
            delete_queryset.delete()
        if len(for_create) > 0:
            create_serializer = serializer(
                data=for_create,
                many=True,
                context=context
            )
            create_serializer.is_valid(raise_exception=True)
            return create_serializer


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
    name = serializers.CharField()
    bounding_box = BoundingBoxContainerSerializer(many=True, required=False)
    keypoints_name = serializers.ListSerializer(child=serializers.CharField())
    keypoints_style = serializers.ListSerializer(child=serializers.CharField())
    keypoints = KeypointContainerSerializer(many=True, required=False)
    joints = JointContainerSerializer(many=True, required=False)
    features = FeatureContainerSerializer(many=True, required=False)

    def create(self, validated_data):
        template = Template(**validated_data)

        if 'bounding_box' in validated_data.keys():
            model_list = list()
            for item in validated_data['bounding_box']:
               model_list.append(BoundingBoxContainer(**item))

        template.bounding_box = model_list

        if 'keypoints' in validated_data.keys():
            model_list = list()
            for item in validated_data['keypoints']:
                model_list.append(KeypointContainer(**item))

        template.keypoints = model_list

        if 'joints' in validated_data.keys():
            model_list = list()
            for item in validated_data['joints']:
                model_list.append(JointContainer(**item))

        template.joints = model_list

        if 'features' in validated_data.keys():
            model_list = list()
            for item in validated_data['features']:
                model_list.append(FeatureContainer(**item))

        template.features = model_list
        template.save()
        return template

    def update(self, instance, validated_data):
        KeypointContainer.objects.all()
        self.cud_nested(
            queryset=instance.phone_set.all(),
            data=validated_data,
            serializer=BoundingBoxContainerSerializer,
            context=self.context
        )

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
