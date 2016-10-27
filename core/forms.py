from django import forms
from s3direct.widgets import S3DirectWidget

class UploadGeoTagset(forms.Form):
    format_id = forms.CharField(max_length=30)
    data_file = forms.URLField(widget=S3DirectWidget(dest="csv_upload"))
