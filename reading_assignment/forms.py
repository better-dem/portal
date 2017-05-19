from django import forms
from reading_assignment.models import OrderedAssignmentItem
from core.forms import InlineParticipationItemField, InlineParticipationItemWidget

class CreateProjectForm(forms.Form):
    project_name = forms.CharField(max_length=100)
    polygon_field = EditablePolygonField(label="Region of interest")
    
    def __init__(self,  *args, **kwargs):
        super(CreateProjectForm, self).__init__(*args, **kwargs)
        goals = FeedbackGoal.objects.all()
        for goal in goals:
            var_name = goal.name + "_pref"
            label = goal.name.replace("_", " ").title()
            help_text = goal.description
            self.fields[var_name] = forms.BooleanField(label = label, help_text=help_text, required=False)

class SubmitAssignmentForm(forms.Form):
    def __init__(self, project, *args, **kwargs):
        super(ItemResponseForm, self).__init__(*args, **kwargs)

        ans = project.name+ ":"
        i = 1
        assignment_items = project.orderedassignmentitem_set.all()
        sorted_assignment_items = sorted(assignment_items, key=lambda x: x.number)
        for assignment_item in sorted_assignment_items:
            if not assignment_item.text_question is None:
                var_name = "text_question_{}".format(assignment_item.id)
                self.fields[var_name] = forms.TextField(label=str(i))
            elif not assignment_item.participation_item is None:
                var_name = "participation_item_{}".format(assignment_item.participation_item.id)
                self.fields[var_name] = InlineParticipationItemField(item_id=assignment_item.participation_item.id)
            i += 1
