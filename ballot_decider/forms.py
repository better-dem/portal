from django import forms
from django.forms.widgets import Textarea, DateInput
from core import forms as cf
from core import models as cm
from widgets import forms as wf

class CreateProjectForm(forms.Form):
    measure_name = forms.CharField()
    ballot_text = forms.CharField(widget = Textarea)
    election_date = forms.DateField(widget = wf.DatePickerJQueryWidget)
    election_website = forms.URLField()
    
    participation_item_number_1 = forms.IntegerField(min_value = 0, required=False)
    participation_item_number_2 = forms.IntegerField(min_value = 0, required=False)
    participation_item_number_3 = forms.IntegerField(min_value = 0, required=False)

    pov_quote_1 = forms.CharField(widget=Textarea, required=False)
    pov_citation_url_1 = forms.URLField(required=False)
    pov_favorability_1 = forms.FloatField(min_value=0.0, max_value=1.0, required = False)

    pov_quote_2 = forms.CharField(widget=Textarea, required=False)
    pov_citation_url_2 = forms.URLField(required=False)
    pov_favorability_2 = forms.FloatField(min_value=0.0, max_value=1.0, required = False)

    pov_quote_3 = forms.CharField(widget=Textarea, required=False)
    pov_citation_url_3 = forms.URLField(required=False)
    pov_favorability_3 = forms.FloatField(min_value=0.0, max_value=1.0, required = False)

    tag1 = cf.tag_aac.get_new_form_field(required=False)
    tag2 = cf.tag_aac.get_new_form_field(required=False)
    tag3 = cf.tag_aac.get_new_form_field(required=False)

    def clean(self):
        cleaned_data = super(CreateProjectForm, self).clean()

        # ensure pov's are completely filled in or not at all
        for i in range(1,4):
            quote = cleaned_data.get("pov_quote_"+str(i))
            citation = cleaned_data.get("pov_citation_url_"+str(i))
            favorability = cleaned_data.get("pov_favorability_"+str(i))
            if any([quote, citation, favorability]) and not all([quote, citation, favorability]):
                raise forms.ValidationError("Each POV must either be left blank or filled in completely")

    # Ensure participation items are valid
    def clean_participation_item_number_1(self):
        data = self.cleaned_data['participation_item_number_1']
        if data is None or data == "":
            return
        try:
            ref = cm.ParticipationItem.objects.get(id=data, is_active=True)
        except:
            raise forms.ValidationError("There is no active participation item with that ID")
        return data

    def clean_participation_item_number_2(self):
        data = self.cleaned_data['participation_item_number_2']
        if data is None or data == "":
            return
        try:
            ref = cm.ParticipationItem.objects.get(id=data, is_active=True)
        except:
            raise forms.ValidationError("There is no active participation item with that ID")
        return data

    def clean_participation_item_number_3(self):
        data = self.cleaned_data['participation_item_number_3']
        if data is None or data == "":
            return
        try:
            ref = cm.ParticipationItem.objects.get(id=data, is_active=True)
        except:
            raise forms.ValidationError("There is no active participation item with that ID")
        return data
