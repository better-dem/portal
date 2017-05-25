from django import forms
from reading_assignment.models import OrderedAssignmentItem
from core.forms import InlineParticipationItemField, InlineParticipationItemWidget
from django.forms.widgets import Textarea

class CreateProjectForm(forms.Form):
    assignment_name = forms.CharField()

class AssignmentItemForm(forms.Form):
    def __init__(self, *args, **kwargs):
        profile = kwargs.pop('userprofile')
        super(AssignmentItemForm, self).__init__(*args, **kwargs)
        self.fields["participation_item"] = forms.ChoiceField(choices=((i.id, i.name[:30] + "..." if len(i.name) > 30 else i.name) for i in profile.bookmarks.all()), required=False)
        self.fields["text_question"] = forms.CharField(widget=Textarea, required=False)

class SubmitAssignmentForm(forms.Form):
    def __init__(self, project, *args, **kwargs):
        super(SubmitAssignmentForm, self).__init__(*args, **kwargs)
        assignment_items = project.orderedassignmentitem_set.all()
        sorted_assignment_items = sorted(assignment_items, key=lambda x: x.number)
        for assignment_item in sorted_assignment_items:
            if not assignment_item.text_question is None:
                var_name = "text_question_{}".format(assignment_item.text_question.id)
                self.fields[var_name] = forms.CharField(widget = Textarea(attrs={'style':"width:100%;", 'rows': 4, 'cols':2}), label="{}".format(assignment_item.text_question.question_text))
            elif not assignment_item.participation_item is None:
                var_name = "participation_item_{}".format(assignment_item.participation_item.id)
                self.fields[var_name] = InlineParticipationItemField(initial=assignment_item.participation_item.id, label="")
