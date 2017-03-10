from django import forms
from s3direct.widgets import S3DirectWidget
from django.forms.widgets import Textarea, DateInput, NumberInput
from core import forms as cf
from core import models as cm
from widgets import forms as wf
from .models import Fallacy

class CreateProjectForm(forms.Form):
    name = forms.CharField()
    topic_overview = forms.CharField(widget = Textarea)

    quote1 = forms.CharField(widget=Textarea, required=False)
    speaker_name1 = forms.CharField(max_length=500, required=False)
    reference1 = forms.URLField(required = False)
    screenshot_filename1 = forms.URLField(widget=S3DirectWidget(dest="file_upload"), required=False)
    fallacy1 = forms.ModelChoiceField(queryset=Fallacy.objects.all(), required=False)
    fallacy_association_explanation1 = forms.CharField(widget = Textarea, required=False)
    fallacy_association_improvement1 = forms.CharField(widget = Textarea, required=False)

    quote2 = forms.CharField(widget=Textarea, required=False)
    speaker_name2 = forms.CharField(max_length=500, required=False)
    reference2 = forms.URLField(required = False)
    screenshot_filename2 = forms.URLField(widget=S3DirectWidget(dest="file_upload"), required=False)
    fallacy2 = forms.ModelChoiceField(queryset=Fallacy.objects.all(), required=False)
    fallacy_association_explanation2 = forms.CharField(widget = Textarea, required=False)
    fallacy_association_improvement2 = forms.CharField(widget = Textarea, required=False)

    quote3 = forms.CharField(widget=Textarea, required=False)
    speaker_name3 = forms.CharField(max_length=500, required=False)
    reference3 = forms.URLField(required = False)
    screenshot_filename3 = forms.URLField(widget=S3DirectWidget(dest="file_upload"), required=False)
    fallacy3 = forms.ModelChoiceField(queryset=Fallacy.objects.all(), required=False)
    fallacy_association_explanation3 = forms.CharField(widget = Textarea, required=False)
    fallacy_association_improvement3 = forms.CharField(widget = Textarea, required=False)

    tag1 = cf.tag_aac.get_new_form_field(required=False)
    tag2 = cf.tag_aac.get_new_form_field(required=False)
    tag3 = cf.tag_aac.get_new_form_field(required=False)

    def clean(self):
        cleaned_data = super(CreateProjectForm, self).clean()

        # ensure pov's are completely filled in or not at all
        for i in range(1,4):
            quote = cleaned_data.get("quote"+str(i))
            speaker = cleaned_data.get("speaker_name"+str(i))
            ref = cleaned_data.get("speaker_name"+str(i))
            scsht = cleaned_data.get("speaker_name"+str(i))
            fall = cleaned_data.get("speaker_name"+str(i))
            fae = cleaned_data.get("speaker_name"+str(i))
            fai = cleaned_data.get("speaker_name"+str(i))
            quote_vars = [quote, speaker, ref, scsht, fall, fae, fai] 
            if any(quote_vars) and not all(quote_vars):
                raise forms.ValidationError("Each quote must either be left blank or filled in completely: " + str(i))

class EditProjectForm(CreateProjectForm):
    def __init__(self, project, *args, **kwargs):
        super(CreateProjectForm, self).__init__(*args, **kwargs)
        quotes = project.quotes.all()
        for q in quotes:
            self.fields["delete_quote_"+str(pov.id)] = forms.BooleanField(help_text=str(quote.quote_string), required=False)

