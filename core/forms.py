from django import forms

class UploadGeoTagset(forms.Form):
    format_id = forms.CharField(max_length=30)
    data_file = forms.FileField()
