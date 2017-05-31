from django import forms
from django.forms.widgets import Textarea, DateInput, NumberInput
from s3direct.widgets import S3DirectWidget
from core import forms as cf
import json
import sys
from widgets import forms as wf
from city_budgeting.models import validate_budget_json

class CreateProjectForm(forms.Form):
    name = forms.CharField(label="Project Name")
    fiscal_period_start = forms.DateField(widget = wf.DatePickerJQueryWidget)
    fiscal_period_end = forms.DateField(widget = wf.DatePickerJQueryWidget)
    
    budget_description = forms.CharField(widget = Textarea(attrs={'style':"width:100%;", 'rows': 4, 'cols':2}))
    revenues_description = forms.CharField(widget = Textarea(attrs={'style':"width:100%;", 'rows': 4, 'cols':2}))
    funds_description = forms.CharField(widget = Textarea(attrs={'style':"width:100%;", 'rows': 4, 'cols':2}))
    expenses_description = forms.CharField(widget = Textarea(attrs={'style':"width:100%;", 'rows': 4, 'cols':2}))

    download_link_1 = wf.InlineLinkField(required=False, label="Example Budget Excel File")
    budget_excel_file = forms.URLField(widget=S3DirectWidget(dest="file_upload"))
    budget_url = forms.URLField()
    city = cf.tag_aac.get_new_form_field(required=False)


class EditProjectForm(forms.Form):
    
    name = forms.CharField(label="Project Name")
    fiscal_period_start = forms.DateField(widget = wf.DatePickerJQueryWidget)
    fiscal_period_end = forms.DateField(widget = wf.DatePickerJQueryWidget)
    
    budget_description = forms.CharField(widget = Textarea(attrs={'style':"width:100%;", 'rows': 4, 'cols':2}))
    revenues_description = forms.CharField(widget = Textarea(attrs={'style':"width:100%;", 'rows': 4, 'cols':2}))
    funds_description = forms.CharField(widget = Textarea(attrs={'style':"width:100%;", 'rows': 4, 'cols':2}))
    expenses_description = forms.CharField(widget = Textarea(attrs={'style':"width:100%;", 'rows': 4, 'cols':2}))

    download_link_1 = wf.InlineLinkField(required=False, label="Example Budget Excel File")
    download_link_2 = wf.InlineLinkField(required=False, label="Current Budget Excel File")
    budget_excel_file = forms.URLField(label="Replacement Budget Excel File (Optional)", required=False, widget=S3DirectWidget(dest="file_upload"))
    budget_url = forms.URLField()
    city = cf.tag_aac.get_new_form_field(required=False)


