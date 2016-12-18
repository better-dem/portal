from django import forms
from city_budgeting.models import TMCQ, Question, Service
from core import forms as cf
import json
import sys
from widgets.forms import ShowPointField

class CreateProjectForm(forms.Form):
    place_name = cf.tag_aac.get_new_form_field()    
    fiscal_year_end_date = forms.DateField(widget=forms.SelectDateWidget)
    total_expected_revenue = forms.IntegerField(help_text="(Approximate value (2 significant figures), USD)")
    total_expected_expenditure = forms.IntegerField(help_text="(Approximate value (2 significant figures), USD)")
    mayor_name = forms.CharField(max_length=100)
    council_members = forms.CharField(widget=forms.widgets.Textarea, help_text="comma separated names of council memebers") 
    budget_url = forms.URLField()

    def __init__(self, *args, **kwargs):
        super(CreateProjectForm, self).__init__(*args, **kwargs)
        for st in Service.SERVICE_TYPES:
            self.fields[st[0]+"_source"] = forms.ChoiceField(label = st[1]+" Services", help_text="How are "+st[1]+" services provided?", required=True, choices =  Service.SOURCE_CHOICES)
            self.fields[st[0]+"_expenditure"] = forms.IntegerField(label = st[1]+" Budget", help_text="What is the projected expenditure for "+st[1]+" services?", required=False)



class QuizResponseForm(forms.Form):
    def __init__(self, item, *args, **kwargs):
        super(QuizResponseForm, self).__init__(*args, **kwargs)
        city_tag = item.participation_project.citybudgetingproject.city
        self.fields["map_field"] = ShowPointField(label="City of "+str(city_tag.get_name()), initial=json.dumps([city_tag.point.y, city_tag.point.x]))

        i = 1
        questions = Question.objects.filter(item=item).distinct()
        for question in questions:
            try:
                tmcq = question.tmcq
                label = str(i)
                help_text = question.question_text
                var_name = "field_prf_" + str(question.id)
                choices = []

                for j in range(1,6):
                    if not tmcq.__dict__["option"+str(j)] == "":
                        choices.append((str(j), tmcq.__dict__["option"+str(j)]))

                self.fields[var_name] = forms.ChoiceField(label = label, help_text=help_text, required=False, choices = choices )
                i += 1
            except:
                raise Exception("Invalid question type. Only TMCQ supported")
