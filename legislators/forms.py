from django import forms
from django.forms.widgets import Textarea
from core import forms as cf

class SearchQueryForm(forms.Form):
    query_text = forms.CharField(max_length=500, required=False)
    state_id = forms.IntegerField()


