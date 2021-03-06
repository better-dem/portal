from django import forms
from s3direct.widgets import S3DirectWidget
from widgets import forms as wf
from core import models as cm

class UploadDataset(forms.Form):
    FORMAT_CHOICES = (("states_v1", "States"), ("uscitieslist_csv_v0","Cities"), ("openstates_subjects_v1", "Openstates Subjects"))
    small_test = forms.BooleanField(required=False)
    format_id = forms.ChoiceField(choices=FORMAT_CHOICES)
    data_file = forms.URLField(widget=S3DirectWidget(dest="data_upload"))

class CreateShortcutForm(forms.Form):
    item_id = forms.IntegerField()
    shortcut_string = forms.CharField(max_length=500, validators=[cm.validate_shortcut_string])

    def clean_item_id(self):
        data = self.cleaned_data['item_id']
        if data is None or data == "":
            return
        try:
            ref = cm.ParticipationItem.objects.get(id=data, is_active=True)
        except:
            raise forms.ValidationError("There is no active participation item with that ID")
        return data

class ManageGroupForm(forms.Form):
    new_invitation_name = forms.CharField(required=True)
    new_invitation_email = forms.EmailField(required=False)
    
class RegisterGroupForm(forms.Form):
    course_registration_code = forms.CharField(required=True)

class AddBookmarkForm(forms.Form):
    item_id = forms.IntegerField(required=True)

# create aac in advance
# form is imported by urls, 
def pre_process_query(q):
    q = q.replace("%2c", ",").lower()
    name = None
    detail = None
    if "," in q:
        name = q.split(',')[0].strip()
        detail = ','.join(q.split(',')[1:]).strip()
    else:
        name = q.strip()
    return name, detail

def get_matching_tags(q):
    name, detail = pre_process_query(q)
    if not detail is None:
        return cm.Tag.objects.filter(name__istartswith=name).filter(detail__istartswith=detail)[:100]
    else:
        return cm.Tag.objects.filter(name__istartswith=name)[:100]

def get_best_final_matching_tag(q):
    if len(q) == 0:
        return None
    possible_matches = get_matching_tags(q)
    if len(possible_matches) == 1:
        return possible_matches[0]
    if len(possible_matches) == 0:
        return None
    name, detail = pre_process_query(q)
    exact_name_matches = [m for m in possible_matches if m.name.strip().lower()==name]
    exact_detail_matches = [m for m in possible_matches if m.detail.strip().lower()==detail]
    perfect_matches = [m for m in exact_detail_matches if m in exact_name_matches]
    if len(perfect_matches) > 0:
        return perfect_matches[0]
    if len(exact_name_matches) > 0:
        return exact_name_matches[0]
    if len(exact_detail_matches) > 0:
        return exact_detail_matches[0]
    return possible_matches[0]

matching_object_query = get_matching_tags
suggestion_function = lambda item: {"value": item.get_name(), "data": {"id": item.id, "category": cm.get_tag_category(item)}}
ajax_url = "/autocomplete_tags/"
tag_aac = wf.AjaxAutocomplete(matching_object_query, suggestion_function, ajax_url)


class AddTagForm(forms.Form):
    place_name = tag_aac.get_new_form_field()

class DeleteProjectConfirmationForm(forms.Form):
    pass

class IssueReportForm(forms.Form):
    event_id = forms.IntegerField(min_value=0, label="", widget=forms.widgets.HiddenInput, required=True)
    issue_title = forms.CharField(max_length = 100)
    issue_type = forms.ChoiceField(label = "What type of issue are you reporting?", choices=(("PC", "Propaganda, campaigning, or biased content"), ("BR", "Bug or website error"), ("IA", "Inaccurate content"), ("FR", "Request a feature"), ))
    description = forms.CharField(widget=forms.widgets.Textarea)

class StripePaymentForm(forms.Form):
    stripeToken = forms.CharField(max_length=500)
    donation_amount=forms.CharField(max_length=10)
    recurring=forms.CharField(max_length=10)
    email=forms.EmailField(max_length=500)


class InlineParticipationItemWidget(forms.Widget):
    """
    Widget to display a participation item inline inside a form
    """
    def render(self, name, value, *args, **kwargs):
        """
        value is participation_item_id
        """
        participation_item_id = value
        app = cm.get_app_for_model(cm.ParticipationItem.objects.get(id=participation_item_id).get_inherited_instance().__class__)
        app_name = app.name
        is_custom_template = "true" if getattr(app, "custom_feed_item_template", False) else "false" # javascript bools
        div_id = 'inline_form_field_item_' + kwargs['attrs']['id']
        input_name = name
        input_id = kwargs['attrs']['id']

        render_html = """
        <div id="{}"></div>
        <input type='hidden' name='{}' id='{}' value='' />

        <script type="text/javascript">
        display_feed_item({},"{}","{}",{})
        </script>
        """
        render_html_with_id = render_html.format(div_id, input_name, input_id,
                                                 participation_item_id, div_id, app_name, is_custom_template)
        return render_html_with_id

    def __init__(self, *args, **kwargs):
        super(InlineParticipationItemWidget, self).__init__(*args, **kwargs)

class InlineParticipationItemField(forms.Field):
    def __init__(self,
        required= False,
        widget=InlineParticipationItemWidget,          
        label=None,
        initial=None,
        help_text="",
        validators=[],
        *args,
        **kwargs):
        super(InlineParticipationItemField, self).__init__(required=required,
            widget=widget,
            label=label,
            initial=initial,
            help_text=help_text,
            validators=validators,
            *args,
            **kwargs)
        self.disabled = True

    def to_python(self, value):
        return None

    def validate(self, value):
        super(InlineParticipationItemField, self).validate(value)

    def widget_attrs(self, widget):
        attrs = super(InlineParticipationItemField, self).widget_attrs(widget)
        return attrs
