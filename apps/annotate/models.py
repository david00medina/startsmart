from datetime import datetime
from djongo import models
from django import forms
import uuid


def upload(instance, filename):
    return 'uploads/%s_%s/%s' % \
           (instance.user, instance.user.id, uuid.uuid3(uuid.NAMESPACE_DNS, filename + datetime.now().__str__()))


class JointContainer(models.Model):
    name = models.TextField()
    joint_index_1 = models.PositiveIntegerField()
    joint_index_2 = models.PositiveIntegerField()

    class Meta:
        abstract = True


class JointContainerForm(forms.ModelForm):
    class Meta:
        model = JointContainer
        fields = '__all__'


class FeatureContainer(models.Model):
    name = models.TextField()
    features_index = models.ArrayModelField(model_container=models.IntegerField, model_form_class=forms.IntegerField)

    class Meta:
        abstract = True


class FeatureContainerForm(forms.ModelForm):
    class Meta:
        model = FeatureContainer
        fields = '__all__'


class KeypointModel(models.Model):
    name = models.TextField()
    keypoints_name = models.ArrayModelField(model_container=models.TextField)
    keypoints_style = models.ArrayModelField(blank=True, model_container=models.TextField)
    joints_index = models.EmbeddedModelField(blank=True,
                                             model_container=JointContainer,
                                             model_form_class=JointContainerForm)
    features = models.EmbeddedModelField(blank=True,
                                         model_container=FeatureContainer,
                                         model_form_class=FeatureContainerForm)


class KeypointData(models.Model):
    keypointmodel_id = models.ForeignKey(KeypointModel, on_delete=models.CASCADE, blank=True)
    keypoints = models.ArrayModelField(model_container=models.DecimalField(max_digits=19, decimal_places=10),
                                       model_form_class=forms.DecimalField)

    class Meta:
        abstract = True


class KeypointDataForm(forms.ModelForm):
    class Meta:
        model = KeypointData
        fields = '__all__'


class KeypointContainer(models.Model):
    name = models.TextField()
    keypoint_data = models.EmbeddedModelField(model_container=KeypointData,
                                              model_form_class=KeypointDataForm)

    class Meta:
        abstract = True


class KeypointContainerForm(forms.ModelForm):
    class Meta:
        model = KeypointContainer
        fields = '__all__'


class Template(models.Model):
    name = models.TextField()
    keypoints_data = models.EmbeddedModelField(model_container=KeypointContainer,
                                               model_form_class=KeypointContainerForm)

    class Meta:
        abstract = True


class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = '__all__'


class Category(models.Model):
    keypointmodel_id = models.ForeignKey(KeypointModel, on_delete=models.CASCADE, blank=True)
    name = models.TextField()
    supercategory = models.TextField(blank=True)
    templates = models.EmbeddedModelField(blank=True,
                                          model_container=Template,
                                          model_form_class=TemplateForm)


class License(models.Model):
    right_holder = models.TextField(blank=True)
    license = models.TextField(blank=True)
    copyright = models.PositiveIntegerField(blank=True)


class Image(models.Model):
    license_id = models.ForeignKey(License, on_delete=models.CASCADE, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    filename = models.TextField()
    uri = [
        (models.URLField(), 'URL'),
        (models.FileField(upload_to=upload), 'FILE')
    ]
    image = models.ImageField()
    channel_no = models.PositiveIntegerField()


class Video(models.Model):
    license_id = models.ForeignKey(License, on_delete=models.CASCADE, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    filename = models.TextField()
    total_frames = models.PositiveIntegerField()
    uri = [
        (models.URLField(), 'URL'),
        (models.FileField(upload_to=upload), 'FILE')
    ]
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    channel_no = models.PositiveIntegerField()


class Annotation(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    image_id = models.ForeignKey(Image, on_delete=models.CASCADE, blank=True)
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE, blank=True)
    frame = models.PositiveIntegerField(blank=True)
    keypoints_container = models.EmbeddedModelField(model_container=KeypointContainer,
                                                    model_form_class=KeypointContainerForm)
