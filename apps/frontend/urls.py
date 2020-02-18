from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('', views.index),
    path('projects', views.index),
    path('<int:project_id>/datasets', views.index),
    path('<int:project_id>/<int:dataset_id>/annotator', views.index),
]
