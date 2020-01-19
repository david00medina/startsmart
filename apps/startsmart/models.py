from datetime import datetime
from djongo import models
from django import forms
import uuid
import os


def upload(instance, filename):
    new_filename = '%s%s' % \
               (uuid.uuid3(uuid.NAMESPACE_DNS, filename + datetime.now().__str__()),
                os.path.splitext(filename)[-1])
    if isinstance(instance, Image):
        return 'images/' + new_filename
    else:
        return 'videos/' + new_filename



class JointContainer(models.Model):
    name = models.TextField()
    indexes = models.ListField(models.PositiveIntegerField(), max_length=2)

    class Meta:
        abstract = True


class JointContainerForm(forms.ModelForm):
    class Meta:
        models = JointContainer
        fields = '__all__'


class FeatureContainer(models.Model):
    name = models.TextField()
    indexes = models.ListField(models.PositiveIntegerField())

    class Meta:
        abstract = True


class FeatureContainerForm(forms.ModelForm):
    class Meta:
        models = FeatureContainer
        fields = '__all__'


class KeypointContainer(models.Model):
    name = models.TextField() # Pose, hand or face?
    dimension = models.CharField(max_length=2)
    data = models.ListField(models.FloatField())
    confidence = models.ListField(models.FloatField())

    class Meta:
        abstract = True


class KeypointContainerForm(forms.ModelForm):
    class Meta:
        models = KeypointContainer
        fields = '__all__'


class BoundingBoxContainer(models.Model):
    dimension = models.CharField(max_length=2)
    min_x = models.FloatField()
    min_y = models.FloatField()
    min_z = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    depth = models.FloatField()

    class Meta:
        abstract = True


class BoundingBoxContainerForm(forms.ModelForm):
    class Meta:
        models = BoundingBoxContainer
        fields = '__all__'


class Template(models.Model):
    name = models.CharField(max_length=100)  # Front, side-left, side-right, up-view, low-view?
    bounding_box = models.ArrayModelField(model_container=BoundingBoxContainer,
                                          model_form_class=BoundingBoxContainerForm, null=True)
    keypoints_name = models.ListField(models.TextField(), null=True)
    keypoints_style = models.ListField(models.TextField(), null=True)
    keypoints = models.ArrayModelField(model_container=KeypointContainer,
                                       model_form_class=KeypointContainerForm,
                                       null=True)
    joints = models.ArrayModelField(model_container=JointContainer,
                                    model_form_class=JointContainerForm,
                                    null=True)
    features = models.ArrayModelField(model_container=FeatureContainer,
                                      model_form_class=FeatureContainerForm,
                                      null=True)
    objects = models.DjongoManager()


class Model(models.Model):
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True)
    name = models.TextField()


class Category(models.Model):
    model = models.ForeignKey(Model, on_delete=models.SET_NULL, null=True)
    name = models.TextField()
    supercategory = models.TextField()


class RegionOfInterest(models.Model):
    name = models.TextField()
    style = models.TextField(default='#FFFFFF')
    frame_range = models.ListField(models.PositiveIntegerField(), max_length=2)
    vertices = models.ListField(models.DecimalField(max_digits=19, decimal_places=10))


class License(models.Model):
    right_holder = models.TextField(blank=True)
    home_page = models.URLField(blank=True)
    email = models.ListField(models.EmailField(blank=True), blank=True)
    license = models.TextField(blank=True)
    copyright = models.PositiveIntegerField(blank=True)


class Image(models.Model):
    license = models.ForeignKey(License, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    roi = models.ForeignKey(RegionOfInterest, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    uri = models.ImageField(upload_to=upload)


class Video(models.Model):
    license = models.ForeignKey(License, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    uri = models.FileField(upload_to=upload)
    total_frames = models.PositiveIntegerField(null=True)


class Frame(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, blank=True)
    roi = models.ForeignKey(RegionOfInterest, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    frame_no = models.PositiveIntegerField()
    image = models.ImageField()


class Project(models.Model):
    name = models.TextField()


class Dataset(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    video = models.ArrayReferenceField(Video, on_delete=models.SET_NULL, null=True)
    image = models.ArrayReferenceField(Image, on_delete=models.SET_NULL, null=True)
    name = models.TextField()


class Annotation(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, default=None)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=None)
    image = models.ForeignKey('Image', on_delete=models.CASCADE, default=None)
    frame = models.ForeignKey('Frame', on_delete=models.CASCADE, default=None)
    keypoints = models.ArrayModelField(model_container=KeypointContainer,
                                       model_form_class=KeypointContainerForm,
                                       null=True)
    bounding_box = models.ArrayModelField(model_container=BoundingBoxContainer,
                                          model_form_class=BoundingBoxContainerForm,
                                          null=True)
