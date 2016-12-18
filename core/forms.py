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
        return Tag.objects.filter(name__istartswith=name).filter(detail__istartswith=detail)
    else:
        return Tag.objects.filter(name__istartswith=name)

def get_best_final_matching_tag(q):
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
suggestion_function = lambda item: item.get_name()
ajax_url = "/autocomplete_tags/"
tag_aac = wf.AjaxAutocomplete(matching_object_query, suggestion_function, ajax_url)


class AddTagForm(forms.Form):
    place_name = tag_aac.get_new_form_field()
