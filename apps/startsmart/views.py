from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .serializers import *
from .models import *
import io


class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def list(self, request, *args, **kwargs):
        if 'id' in self.request.GET.keys() or 'name' in self.request.GET.keys():
            self.get_queryset()

        serializer = self.serializer_class(self.queryset, context={'request': request}, many=True)
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
        serializer = self.serializer_class(get_object_or_404(Template, pk=kwargs['pk']), data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            result = serializer.create(serializer.validated_data)
            serializer = self.serializer_class(result, context={'request': request})
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, **kwargs):
        template = get_object_or_404(Template, pk=pk)
        serializer = self.serializer_class(template, data=request.data, context={'request': request})
        data = request.data.copy()
        data.update({'id': pk})
        if serializer.is_valid():
            result = serializer.update(template, data)
            serializer = self.serializer_class(result, context={'request': request})
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

    def get_queryset(self):
        query_params = self.request.query_params
        dataset = query_params.get('dataset')

        if dataset is not None:
            datasetParam = int(dataset)

        if dataset is not None:
            queryset = self.queryset.filter(dataset_id__exact=datasetParam)
            return queryset

    def list(self, request, *args, **kwargs):
        if self.request.query_params:
            serializer = self.serializer_class(self.get_queryset(), context={'request': request}, many=True)
        else:
            serializer = self.serializer_class(self.queryset, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            serializer = self.serializer_class(serializer.instance, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        object = get_object_or_404(self.queryset, pk=kwargs['pk'])
        serializer = self.serializer_class(object, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.update(object, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        query_params = self.request.query_params
        dataset = query_params.get('dataset')

        if dataset is not None:
            datasetParam = int(dataset)

        if dataset is not None:
            queryset = self.queryset.filter(dataset_id__exact=datasetParam)
            return queryset

    def list(self, request, *args, **kwargs):
        if self.request.query_params:
            serializer = self.serializer_class(self.get_queryset(), context={'request': request}, many=True)
        else:
            serializer = self.serializer_class(self.queryset, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            serializer = self.serializer_class(serializer.instance, data=request.data, context={'request': request})
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        object = get_object_or_404(self.queryset, pk=kwargs['pk'])
        serializer = self.serializer_class(object, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.update(object, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FrameViewSet(viewsets.ModelViewSet):
    queryset = Frame.objects.all()
    serializer_class = FrameSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        stream = io.BytesIO(request.data['json'].encode())
        json = JSONParser().parse(stream)
        request.data.pop('json')
        request.data['video'] = json['video']
        request.data['roi'] = json['roi']
        request.data['frame_no'] = json['frame_no']
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        object = get_object_or_404(self.queryset, pk=kwargs['pk'])
        serializer = self.serializer_class(object, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.update(object, serializer.validated_data)
            serializer = self.serializer_class(object, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    def get_queryset(self):
        if 'id' in self.request.GET.keys() \
                and 'project' in self.request.GET.keys() \
                and 'name' in self.request.GET.keys():
            return self.queryset.filter(Q(id__exact=self.request.GET.get("id")))\
                .filter(Q(project_id__exact=self.request.GET.get("project")))\
                .filter(Q(name__icontains=self.request.GET.get("name")))
        if 'id' in self.request.GET.keys():
            return self.queryset.filter(Q(id__exact=self.request.GET.get("id")))
        if 'project' in self.request.GET.keys():
            return self.queryset.filter(Q(project_id__exact=self.request.GET.get("project")))
        if 'name' in self.request.GET.keys():
            return self.queryset.filter(Q(name__icontains=self.request.GET.get("name")))

    def list(self, request, *args, **kwargs):
        if 'id' in self.request.GET.keys() \
                or 'project' in self.request.GET.keys() \
                or 'name' in self.request.GET.keys():
            serializer = self.serializer_class(self.get_queryset(), context={'request': request}, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.serializer_class(self.queryset, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(get_object_or_404(Dataset, pk=kwargs['pk']), context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            serializer = self.serializer_class(serializer.instance, data=request.data, context={'request': request})
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        object = get_object_or_404(self.queryset, pk=kwargs['pk'])
        serializer = self.serializer_class(object, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.update(object, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnnotationViewSet(viewsets.ModelViewSet):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        if 'id' in self.request.GET.keys() and 'project' in self.request.GET.keys()\
                and 'image' in self.request.GET.keys() \
                and 'frame' in self.request.GET.keys():
            return self.queryset.filter(Q(id__exact=self.request.GET.get("id")))\
                .filter(project__id=self.request.GET.get("project"))\
                .filter(image__id=self.request.GET.get("image"))\
                .filter(frame__id=self.request.GET.get("frame"))
        if 'id' in self.request.GET.keys():
            return self.queryset.filter(Q(id=self.request.GET.get("id")))
        if 'project' in self.request.GET.keys():
            query = Annotation.objects.filter(Q(project__exact=self.request.GET.get('project')))
            return query
        if 'image' in self.request.GET.keys():
            return self.queryset.filter(Q(image__exact=self.request.GET.get('image')))
        if 'frame' in self.request.GET.keys():
            return self.queryset.filter(Q(frame__exact=self.request.GET.get('frame')))

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(get_object_or_404(Annotation, pk=kwargs['pk']), data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            serializer = self.serializer_class(serializer.instance, data=request.data, context={'request': request})
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, **kwargs):
        object = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(object, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.update(object, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LibraryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    permission_classes = [
        permissions.AllowAny
    ]
