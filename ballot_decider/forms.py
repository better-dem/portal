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
    
    basics_notes = forms.CharField(widget = Textarea, required=False)
    basics1 = forms.IntegerField(min_value = 0, required=False)
    basics2 = forms.IntegerField(min_value = 0, required=False)
    basics3 = forms.IntegerField(min_value = 0, required=False)

    effects_notes = forms.CharField(widget = Textarea, required=False)
    effects1 = forms.IntegerField(min_value = 0, required=False)
    effects2 = forms.IntegerField(min_value = 0, required=False)
    effects3 = forms.IntegerField(min_value = 0, required=False)

    pov_quote_1 = forms.CharField(widget=Textarea, required=False)
    pov_citation_url_1 = forms.URLField(required=False)
    pov_is_favorable_1 = forms.BooleanField(required = False)

    pov_quote_2 = forms.CharField(widget=Textarea, required=False)
    pov_citation_url_2 = forms.URLField(required=False)
    pov_is_favorable_2 = forms.BooleanField(required = False)

    pov_quote_3 = forms.CharField(widget=Textarea, required=False)
    pov_citation_url_3 = forms.URLField(required=False)
    pov_is_favorable_3 = forms.BooleanField(required = False)

    tag1 = cf.tag_aac.get_new_form_field(required=False)
    tag2 = cf.tag_aac.get_new_form_field(required=False)
    tag3 = cf.tag_aac.get_new_form_field(required=False)

    def clean(self):
        cleaned_data = super(CreateProjectForm, self).clean()

        # ensure pov's are completely filled in or not at all
        for i in range(1,4):
            quote = cleaned_data.get("pov_quote_"+str(i))
            citation = cleaned_data.get("pov_citation_url_"+str(i))
            is_favorable_defined = not (cleaned_data.get("pov_is_favorable_"+str(i)) is None)
            if any([quote, citation]) and not all([quote, citation, is_favorable_defined]):
                raise forms.ValidationError("Each POV must either be left blank or filled in completely: " + str(i))

    # Ensure participation items are valid
    def clean_basics1(self):
        data = self.cleaned_data['basics1']
        if data is None or data == "":
            return
        try:
            ref = cm.ParticipationItem.objects.get(id=data, is_active=True)
        except:
            raise forms.ValidationError("There is no active participation item with that ID")
        return data

    def clean_basics2(self):
        data = self.cleaned_data['basics2']
        if data is None or data == "":
            return
        try:
            ref = cm.ParticipationItem.objects.get(id=data, is_active=True)
        except:
            raise forms.ValidationError("There is no active participation item with that ID")
        return data

    def clean_basics3(self):
        data = self.cleaned_data['basics3']
        if data is None or data == "":
            return
        try:
            ref = cm.ParticipationItem.objects.get(id=data, is_active=True)
        except:
            raise forms.ValidationError("There is no active participation item with that ID")
        return data

    def clean_effects1(self):
        data = self.cleaned_data['effects1']
        if data is None or data == "":
            return
        try:
            ref = cm.ParticipationItem.objects.get(id=data, is_active=True)
        except:
            raise forms.ValidationError("There is no active participation item with that ID")
        return data

    def clean_effects2(self):
        data = self.cleaned_data['effects2']
        if data is None or data == "":
            return
        try:
            ref = cm.ParticipationItem.objects.get(id=data, is_active=True)
        except:
            raise forms.ValidationError("There is no active participation item with that ID")
        return data

    def clean_effects3(self):
        data = self.cleaned_data['effects3']
        if data is None or data == "":
            return
        try:
            ref = cm.ParticipationItem.objects.get(id=data, is_active=True)
        except:
            raise forms.ValidationError("There is no active participation item with that ID")
        return data

class EditProjectForm(CreateProjectForm):
    def __init__(self, project, *args, **kwargs):
        super(CreateProjectForm, self).__init__(*args, **kwargs)
        povs = project.points_of_view.all()
        for pov in povs:
            self.fields["delete_pov_"+str(pov.id)] = forms.BooleanField(help_text=str(pov.quote), required=False)

