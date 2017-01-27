from django import forms
from django.forms.widgets import Textarea
from core import forms as cf

class CreateProjectForm(forms.Form):
    visualization_title = forms.CharField(max_length=500)
    
    methodology_note = forms.CharField(widget=Textarea)
    methodology_url = forms.URLField()

    csv_data = forms.CharField(widget=Textarea)

    switch_variable = forms.CharField(max_length = 50)
    switch_title = forms.CharField(max_length = 50)
    switch_note = forms.CharField(widget=Textarea)

    pie1_variable = forms.CharField(max_length = 50)
    pie1_title = forms.CharField(max_length = 50)

    pie2_variable = forms.CharField(max_length = 50)
    pie2_title = forms.CharField(max_length = 50)

    bar1_variable = forms.CharField(max_length = 50)
    bar1_title = forms.CharField(max_length = 50)
    bar1_x_label = forms.CharField(max_length = 50)
    bar1_y_label = forms.CharField(max_length = 50)

    bar2_variable = forms.CharField(max_length = 50)
    bar2_title = forms.CharField(max_length = 50)
    bar2_x_label = forms.CharField(max_length = 50)
    bar2_y_label = forms.CharField(max_length = 50)

    tag1 = cf.tag_aac.get_new_form_field(required=False)
    tag2 = cf.tag_aac.get_new_form_field(required=False)
    tag3 = cf.tag_aac.get_new_form_field(required=False)



