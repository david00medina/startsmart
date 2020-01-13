from rest_framework import viewsets, permissions, status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import *
from .models import *


class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def create(self, request, **kwargs):
        serializer = TemplateSerializer(data=request.data)
        if serializer.is_valid():
            template = serializer.create(request.data)
            serializer = TemplateSerializer(template)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, **kwargs):
        serializers = TemplateSerializer(data=request.data)
        if serializers.is_valid():
            a = 2
            return Response(serializers.validated_data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ModelViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [
        permissions.AllowAny
    ]


class RegionOfInterestViewSet(viewsets.ModelViewSet):
    queryset = RegionOfInterest.objects.all()
    serializer_class = RegionOfInterestSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class LicenseViewSet(viewsets.ModelViewSet):
    queryset = License.objects.all()
    serializer_class = LicenseSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Frame.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class FrameViewSet(viewsets.ModelViewSet):
    queryset = Frame.objects.all()
    serializer_class = FrameSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class AnnotationViewSet(viewsets.ModelViewSet):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    permission_classes = [
        permissions.AllowAny
    ]
