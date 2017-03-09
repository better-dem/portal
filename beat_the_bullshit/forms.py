from django import forms
from django.forms.widgets import Textarea, DateInput, NumberInput
from core import forms as cf
from core import models as cm
from widgets import forms as wf

class ParticipateForm(forms.Form):
    def __init__(self, item, *args, **kwargs):
        super(ParticipateForm, self).__init__(*args, **kwargs)
        povs = item.participation_project.ballotdeciderproject.points_of_view.all()
        for pov in povs:
            self.fields["pov_weight_"+str(pov.id)] = forms.IntegerField(widget = NumberInput(attrs={'type': 'range', 'step': '1'}))

class CreateProjectForm(forms.Form):
    measure_name = forms.CharField()
    ballot_text = forms.CharField(widget = Textarea)
    election_date = forms.DateField(widget = wf.DatePickerJQueryWidget)
    election_website = forms.URLField()

    pov_quote_1 = forms.CharField(widget=Textarea, required=False)
    pov_is_favorable_1 = forms.BooleanField(required = False)

    pov_quote_2 = forms.CharField(widget=Textarea, required=False)
    pov_is_favorable_2 = forms.BooleanField(required = False)

    pov_quote_3 = forms.CharField(widget=Textarea, required=False)
    pov_is_favorable_3 = forms.BooleanField(required = False)

    tag1 = cf.tag_aac.get_new_form_field(required=False)
    tag2 = cf.tag_aac.get_new_form_field(required=False)
    tag3 = cf.tag_aac.get_new_form_field(required=False)

    def clean(self):
        cleaned_data = super(CreateProjectForm, self).clean()

        # ensure pov's are completely filled in or not at all
        for i in range(1,4):
            quote = cleaned_data.get("pov_quote_"+str(i))
            is_favorable_defined = not (cleaned_data.get("pov_is_favorable_"+str(i)) is None)
            if any([quote]) and not all([quote, is_favorable_defined]):
                raise forms.ValidationError("Each POV must either be left blank or filled in completely: " + str(i))

class EditProjectForm(CreateProjectForm):
    def __init__(self, project, *args, **kwargs):
        super(CreateProjectForm, self).__init__(*args, **kwargs)
        povs = project.points_of_view.all()
        for pov in povs:
            self.fields["delete_pov_"+str(pov.id)] = forms.BooleanField(help_text=str(pov.quote), required=False)

