from django import forms
from s3direct.widgets import S3DirectWidget
from django.forms.widgets import Textarea
from core import forms as cf
from tool_review.models import TOOL_CATEGORIES, PROJECT_CATEGORIES

class CreateProjectForm(forms.Form):
    tool_name = forms.CharField(max_length=100)
    tool_url = forms.URLField(max_length=200)
    tool_category = forms.ChoiceField(choices=TOOL_CATEGORIES)
    project_category = forms.ChoiceField(choices=PROJECT_CATEGORIES)
    tag1 = cf.tag_aac.get_new_form_field(required=False)
    tag2 = cf.tag_aac.get_new_form_field(required=False)
    tag3 = cf.tag_aac.get_new_form_field(required=False)
    youtube_video_id = forms.CharField(max_length=100, required=False)
    screenshot = forms.URLField(widget=S3DirectWidget(dest="file_upload"))
    summary = forms.CharField(widget=Textarea)

class EditProjectForm(forms.Form):
    tool_name = forms.CharField(max_length=100)
    tool_url = forms.URLField(max_length=200)
    tool_category = forms.ChoiceField(choices=TOOL_CATEGORIES)
    project_category = forms.ChoiceField(choices=PROJECT_CATEGORIES)
    tag1 = cf.tag_aac.get_new_form_field(required=False)
    tag2 = cf.tag_aac.get_new_form_field(required=False)
    tag3 = cf.tag_aac.get_new_form_field(required=False)
    youtube_video_id = forms.CharField(max_length=100, required=False)
    # screenshot = forms.URLField(widget=S3DirectWidget(dest="file_upload"))
    summary = forms.CharField(widget=Textarea)


