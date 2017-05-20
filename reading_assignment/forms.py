from django import forms
from reading_assignment.models import OrderedAssignmentItem
from core.forms import InlineParticipationItemField, InlineParticipationItemWidget
from django.forms.widgets import Textarea

class CreateProjectForm(forms.Form):
    assignment_name = forms.CharField(max_length=100)
    participation_item_1 = forms.IntegerField(min_value = 0, required=False)
    text_question_1 = forms.CharField(widget=Textarea, required=False)
    
class SubmitAssignmentForm(forms.Form):
    def __init__(self, project, *args, **kwargs):
        super(SubmitAssignmentForm, self).__init__(*args, **kwargs)

        ans = project.name+ ":"
        i = 1
        assignment_items = project.orderedassignmentitem_set.all()
        sorted_assignment_items = sorted(assignment_items, key=lambda x: x.number)
        for assignment_item in sorted_assignment_items:
            if not assignment_item.text_question is None:
                var_name = "text_question_{}".format(assignment_item.id)
                self.fields[var_name] = forms.CharField(widget = Textarea, label="{}:{}".format(i, assignment_item.text_question.question_text))
            elif not assignment_item.participation_item is None:
                var_name = "participation_item_{}".format(assignment_item.participation_item.id)
                self.fields[var_name] = InlineParticipationItemField(initial=assignment_item.participation_item.id, label=str(i))
            i += 1
