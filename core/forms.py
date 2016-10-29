from django import forms
from s3direct.widgets import S3DirectWidget

class UploadGeoTagset(forms.Form):
    small_test = forms.BooleanField(required=False)
    format_id = forms.CharField(max_length=30)
    data_file = forms.URLField(widget=S3DirectWidget(dest="data_upload"))


class AddTagForm(forms.Form):
    place_name = forms.CharField(max_length=100)
