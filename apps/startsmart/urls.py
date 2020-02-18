from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('template', TemplateViewSet, 'template')
router.register('model', ModelViewSet, 'model')
router.register('category', CategoryViewSet, 'category')
router.register('roi', RegionOfInterestViewSet, 'roi')
router.register('license', LicenseViewSet, 'license')
router.register('image', ImageViewSet, 'image')
router.register('video', VideoViewSet, 'video')
router.register('frame', FrameViewSet, 'frame')
router.register('project', ProjectViewSet, 'project')
router.register('dataset', DatasetViewSet, 'dataset')
router.register('annotation', AnnotationViewSet, 'annotation')
router.register('library', LibraryViewSet, 'library')

urlpatterns = router.urls
