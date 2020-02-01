from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('projects', views.index),
    path('datasets', views.index),
    path('annotator', views.index),
]
