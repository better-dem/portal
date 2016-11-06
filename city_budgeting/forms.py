from django import forms
from city_budgeting.models import TMCQ, Question
from core import forms as cf
import json

class CreateProjectForm(forms.Form):
    place_name = cf.tag_aac.get_new_form_field()    
    fiscal_year_end_date = forms.DateField(widget=forms.SelectDateWidget)
    total_expected_revenue = forms.IntegerField(help_text="(Approximate value (2 significant figures), USD)")
    total_expected_expenditure = forms.IntegerField(help_text="(Approximate value (2 significant figures), USD)")
    mayor_name = forms.CharField(max_length=100)
    council_members = forms.CharField(widget=forms.widgets.Textarea, help_text="comma separated names of council memebers") 
    budget_url = forms.URLField()

class QuizResponseForm(forms.Form):
    def __init__(self, project, *args, **kwargs):
        super(QuizResponseForm, self).__init__(*args, **kwargs)

        ans = project.name+ ":"
        i = 1
        for question in project.get_questions():
            try:
                tmcq = question.tmcq
                label = str(i)
                help_text = question.question_text
                var_name = "field_prf_" + str(question.id)
                choices = []

                if not tmcq.option1 == "":
                    choices.append(("1", tmcq.option1))
                if not tmcq.option2 == "":
                    choices.append(("2", tmcq.option2))
                if not tmcq.option3 == "":
                    choices.append(("3", tmcq.option3))
                if not tmcq.option4 == "":
                    choices.append(("4", tmcq.option4))
                if not tmcq.option5 == "":
                    choices.append(("5", tmcq.option5))

                self.fields[var_name] = forms.ChoiceField(label = label, help_text=help_text, required=False, choices = choices )
                i += 1
            except:
                raise Exception("Invalid question type. Only TMCQ supported")
