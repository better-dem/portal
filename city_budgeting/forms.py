from django import forms
from django.forms.widgets import Textarea, DateInput, NumberInput
from core import forms as cf
import json
import sys
from widgets import forms as wf
from city_budgeting.models import validate_budget_json

class CreateProjectForm(forms.Form):
    fiscal_period_start = forms.DateField(widget = wf.DatePickerJQueryWidget)
    fiscal_period_end = forms.DateField(widget = wf.DatePickerJQueryWidget)
    budget_json = forms.CharField(widget=Textarea, validators=[validate_budget_json])
    budget_url = forms.URLField()
    city = cf.tag_aac.get_new_form_field(required=False)


