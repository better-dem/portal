from django import forms
from django.forms.widgets import Textarea
from core import forms as cf

def get_choices(item):
    choices = []
    project = item.participation_project.singlequizproject
    for j in range(1,6):
        if not project.__dict__["option"+str(j)] is None and not project.__dict__["option"+str(j)] == "":
            choices.append((str(j), project.__dict__["option"+str(j)]))
    return choices

class ParticipateForm(forms.Form):
    def __init__(self, item, *args, **kwargs):
        super(ParticipateForm, self).__init__(*args, **kwargs)
        choices = get_choices(item)
        self.fields["choice"] = forms.ChoiceField(label="", choices=choices)

class CreateProjectForm(forms.Form):
    question_text = forms.CharField(max_length=500)
    option1 = forms.CharField(max_length = 100)
    option2 = forms.CharField(max_length = 100)
    option3 = forms.CharField(max_length = 100, required=False)
    option4 = forms.CharField(max_length = 100, required=False)
    option5 = forms.CharField(max_length = 100, required=False)
    correct_answer_index = forms.IntegerField(max_value=5, min_value=1)
    citation_url = forms.URLField()
    explanation = forms.CharField(widget=Textarea)
    tag1 = cf.tag_aac.get_new_form_field(required=False)
    tag2 = cf.tag_aac.get_new_form_field(required=False)
    tag3 = cf.tag_aac.get_new_form_field(required=False)

    def clean(self):
        cleaned_data = super(CreateProjectForm, self).clean()
        op3 = cleaned_data.get("option3")
        op4 = cleaned_data.get("option4")
        op5 = cleaned_data.get("option5")
        ans = cleaned_data.get("correct_answer_index")

        if (op4 and not op3) or (op5 and not op4):
            raise forms.ValidationError(
                "Add options to the lower-numbered fields first (don't give an option for option5 while leaving option4 blank)"
            )

        if ans:
            if ans == 5 and not op5:
                raise forms.ValidationError("Option 5 can't be the correct answer if it is left blank")
            if ans == 4 and not op4:
                raise forms.ValidationError("Option 4 can't be the correct answer if it is left blank")
            if ans == 3 and not op3:
                raise forms.ValidationError("Option 3 can't be the correct answer if it is left blank")


