from django import forms
from tool_review.models import ToolReviewProject, ToolReviewItem
from s3direct.widgets import S3DirectWidget
from django.forms.widgets import Textarea

class CreateProjectForm(forms.Form):
    tool_name = forms.CharField(max_length=100)
    screenshot = forms.URLField(widget=S3DirectWidget(dest="file_upload"))
    summary = forms.CharField(widget=Textarea)
