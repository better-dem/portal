from django import forms
from s3direct.widgets import S3DirectWidget
from widgets import forms as wf
from core.models import Tag

class UploadGeoTagset(forms.Form):
    small_test = forms.BooleanField(required=False)
    format_id = forms.CharField(max_length=30)
    data_file = forms.URLField(widget=S3DirectWidget(dest="data_upload"))


# create aac in advance
# form is imported by urls, 
def pre_process_query(q):
    q = q.replace("%2c", ",")
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
        return Tag.objects.filter(name__istartswith=name).filter(detail__istartswith=detail)
    else:
        return Tag.objects.filter(name__istartswith=name)

matching_object_query = get_matching_tags
suggestion_function = lambda item: item.get_name()
ajax_url = "autocomplete_tags/"
tag_aac = wf.AjaxAutocomplete(matching_object_query, suggestion_function, ajax_url)


class AddTagForm(forms.Form):
    place_name = tag_aac.get_new_form_field()
