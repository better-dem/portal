from django import forms
from s3direct.widgets import S3DirectWidget
from django.forms.widgets import Textarea, DateInput, NumberInput
from core import forms as cf
from core import models as cm
from widgets import forms as wf
from .models import Fallacy
import sys

class CreateProjectForm(forms.Form):
    name = forms.CharField()
    topic_overview = forms.CharField(widget = Textarea(attrs={"rows": 2}))

    def __init__(self, *args, **kwargs):
        super(CreateProjectForm, self).__init__(*args, **kwargs)
        for i in range(1,4):
            # quote and fallacy fields
            self.fields["quote"+str(i)] = forms.CharField(widget=Textarea(attrs={"rows": 2}), required=False)
            self.fields["speaker_name"+str(i)] = forms.CharField(max_length=500, required=False)
            self.fields["reference"+str(i)] = forms.URLField(required = False)
            self.fields["screenshot_filename"+str(i)] = forms.URLField(widget=S3DirectWidget(dest="file_upload"), required=False)
            self.fields["youtube_video_id"+str(i)] = forms.CharField(max_length=100, required=False)
            self.fields["fallacy"+str(i)] = forms.ModelChoiceField(queryset=Fallacy.objects.all(), required=False)
            self.fields["fallacy_association_explanation"+str(i)] = forms.CharField(widget = Textarea(attrs={"rows": 2}), required=False)
            self.fields["fallacy_association_improvement"+str(i)] = forms.CharField(widget = Textarea(attrs={"rows": 2}), required=False)
        for i in range(1,4):     # separate loops for field ordering
            # tags
            self.fields["tag"+str(i)] = cf.tag_aac.get_new_form_field(required=False)

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
            if any(quote_vars+[cleaned_data.get("youtube_video_id"+str(i))]) and not all(quote_vars):
                raise forms.ValidationError("Each quote must either be left blank or filled in completely: " + str(i))

class EditProjectForm(CreateProjectForm):
    def __init__(self, project, *args, **kwargs):
        super(EditProjectForm, self).__init__(*args, **kwargs)
        quotes = project.quote_set.all()
        for q in quotes:
            self.fields["delete_quote_"+str(q.id)] = forms.BooleanField(help_text=str(q.quote_string), required=False)
        for i in range(1,4):
            self.fields.pop("screenshot_filename"+str(i)) # don't include screenshots in edit form, too complicated
        self.order_fields(["name", "topic_overview"]+["delete_quote_"+str(q.id) for q in quotes])
