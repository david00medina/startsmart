from rest_framework import viewsets, permissions, status
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .serializers import *
from .models import *


class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def list(self, request, *args, **kwargs):
        if 'id' in self.request.GET.keys() or 'name' in self.request.GET.keys():
            self.get_queryset()

        serializer = TemplateSerializer(self.queryset, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        if 'id' in self.request.GET.keys() and 'name' in self.request.GET.keys():
            return self.queryset.filter(Q(id__exact=self.request.GET.get("id")))\
                .filter(Q(name__icontains=self.request.GET.get("name")))
        if 'id' in self.request.GET.keys():
            return self.queryset.filter(Q(id__exact=self.request.GET.get("id")))
        if 'name' in self.request.GET.keys():
            return self.queryset.filter(Q(name__icontains=self.request.GET.get("name")))

    def retrieve(self, request, *args, **kwargs):
        serializer = TemplateSerializer(get_object_or_404(Template, pk=kwargs['pk']), data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, **kwargs):
        serializer = TemplateSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.create(serializer.validated_data)
            serializer = TemplateSerializer(result)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, **kwargs):
        try:
            template = Template.objects.get(id=pk)
        except Template.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = TemplateSerializer(template, data=request.data)
        data = request.data.copy()
        data.update({'id': pk})
        if serializer.is_valid():
            result = serializer.update(template, data)
            serializer = TemplateSerializer(result)
            return Response(serializer.data)
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
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def list(self, request, *args, **kwargs):
        if 'roi' in self.request.GET.keys():
            self.get_queryset()

        serializer = ImageSerializer(self.queryset, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        if 'roi' in self.request.GET.keys():
            query = self.request.GET.get('roi')
            return self.queryset.filter(Q(roi__exact=query))

    def retrieve(self, request, *args, **kwargs):
        image = get_object_or_404(Image, pk=kwargs['pk'])
        if image:
            serializer = ImageSerializer(image, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        image = get_object_or_404(self.queryset, pk=kwargs['pk'])
        serializer = ImageSerializer(image, data=request.data)
        if serializer.is_valid():
            serializer.update(image, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def create(self, request, *args, **kwargs):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

# TODO: Test this out!
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

    def get_queryset(self):
        if 'id' in self.request.GET.keys() and 'project' in self.request.GET.keys():
            return self.queryset.filter(Q(id__exact=self.request.GET.get("id")))\
                .filter(project__id=self.request.GET.get("project"))
        if 'id' in self.request.GET.keys():
            return self.queryset.filter(Q(id=self.request.GET.get("id")))
        if 'project' in self.request.GET.keys():
            query = Annotation.objects.filter(Q(project__exact=self.request.GET.get('project')))
            return query

    def retrieve(self, request, *args, **kwargs):
        serializer = AnnotationSerializer(get_object_or_404(Annotation, pk=kwargs['pk']), data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, **kwargs):
        serializer = AnnotationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            result = serializer.create(serializer.initial_data)
            serializer = AnnotationSerializer(result, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, **kwargs):
        annotation = get_object_or_404(Annotation, pk=pk)
        serializer = AnnotationSerializer(annotation, data=request.data, context={'request': request})
        data = request.data.copy()
        data.update({'id': pk})
        if serializer.is_valid():
            result = serializer.update(annotation, serializer.data)
            serializer = AnnotationSerializer(result)
            return Response(serializer.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
