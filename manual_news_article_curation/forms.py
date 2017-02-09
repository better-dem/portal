from django import forms
from manual_news_article_curation.models import NewsArticleItem, ManualNewsCurationProject
from s3direct.widgets import S3DirectWidget
from django.forms.widgets import Textarea
from core import forms as cf

class CreateProjectForm(forms.Form):
    name = forms.CharField(max_length=500)
    url = forms.URLField()
    screenshot = forms.URLField(widget=S3DirectWidget(dest="file_upload"))
    first_paragraph = forms.CharField(widget=Textarea)
    tag1 = cf.tag_aac.get_new_form_field(required=False)
    tag2 = cf.tag_aac.get_new_form_field(required=False)
    tag3 = cf.tag_aac.get_new_form_field(required=False)

class EditProjectForm(forms.Form):
    name = forms.CharField(max_length=500)
    url = forms.URLField()
    # screenshot = forms.URLField(widget=S3DirectWidget(dest="file_upload"))
    first_paragraph = forms.CharField(widget=Textarea)
    tag1 = cf.tag_aac.get_new_form_field(required=False)
    tag2 = cf.tag_aac.get_new_form_field(required=False)
    tag3 = cf.tag_aac.get_new_form_field(required=False)

