from django import forms
from django.core.exceptions import ValidationError
import os
import sys
import json
import traceback
from django.http import HttpResponse

api_key = os.environ["GOOGLE_MAPS_API_KEY"]


def validate_polygon(point_array):
    if point_array is None:
        raise ValidationError("Error parsing point array", code="invalid")
    for point in point_array:
        if(len(point) != 2):
            raise ValidationError("Point must compose of latitude and longitude",
                code="invalid")
        for p in point:
            if not type(p) is float:
                raise ValidationError("One of the coordinates is not float",
                    code='invalid')

    if len(point_array) < 3:
        raise ValidationError("At least three points required for polygon",
            code='invalid')

def is_polygon(point_array_string):
    try:
        point_array = json.loads(point_array_string)
        validate_polygon(point_array)
        return True
    except:
        return False


class ShowPolygonWidget(forms.Widget):
    """
    Widget to display a polygon on a map.
    The polygon is not editable.
    The form field is disabled and should not be required.
    """
    class Media:
        css = {
            'all' : ('css/poly_style.css',)
        }
        js = ("js/maps_utils.js",
              "js/show_polygon.js",
              "https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js",
              "https://maps.googleapis.com/maps/api/js?key={}".format(api_key),)

    def render(self, name, value, *args, **kwargs):
        div_id = 'poly_map_' + kwargs['attrs']['id']
        input_name = name
        input_id = kwargs['attrs']['id']
        if value is None or not is_polygon(value):
            raise Exception("ShowPolygonWidget requires the polygon to be defined" + str(value))

        render_html = """
        <div class='map_widget' id="{}"></div>
        <input type='hidden' name='{}' id='{}' value='' />

        <script type="text/javascript">
        google.maps.event.addDomListener(window, 'load', show_polygon_map('{}', '{}', {}));
        </script>
        """
        render_html_with_id = render_html.format(div_id,
            input_name,
            input_id,
            div_id,
            input_id, value)
        return render_html_with_id

    def __init__(self, *args, **kwargs):
        super(ShowPolygonWidget, self).__init__(*args, **kwargs)


class ShowPolygonField(forms.Field):
    def __init__(self,
        required= True,
        widget=ShowPolygonWidget,
        label=None,
        initial=None,
        help_text="",
        validators=[validate_polygon],
        *args,
        **kwargs):
        super(ShowPolygonField, self).__init__(required=required,
            widget=widget,
            label=label,
            initial=initial,
            help_text=help_text,
            validators=validators,
            *args,
            **kwargs)
        self.disabled = True

    def to_python(self, value):
        # Convert to expected python value (list of lists of latlngs)
        value = super(ShowPolygonField, self).to_python(value)
        try:
            json_array = json.loads(value)
        except:
            raise ValidationError("Unable to parse input: '{}'".format(value),
                code="invalid")
        return json_array

    def validate(self, value):
        super(ShowPolygonField, self).validate(value)

    def widget_attrs(self, widget):
        attrs = super(ShowPolygonField, self).widget_attrs(widget)
        return attrs

class EditablePolygonWidget(forms.Widget):
    """
    Widget for a user-editable Polygon form field
    """
    class Media:
        css = {
            'all' : ('css/poly_style.css',)
        }
        js = ("js/maps_utils.js",
              "js/demo_poly_draw.js",
              "https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js",
              "https://maps.googleapis.com/maps/api/js?key={}".format(api_key),)
        
    def render(self, name, value, *args, **kwargs):
        div_id = 'poly_map_' + kwargs['attrs']['id']
        input_name = name
        input_id = kwargs['attrs']['id']
        if value is None or not is_polygon(value):
            value = 'null'

        render_html = """
        <div class='map_widget' id="{}"></div>
        <input type='hidden' name='{}' id='{}' value='' />

        <script type="text/javascript">
        google.maps.event.addDomListener(window, 'load', show_editable_map('{}', '{}', {}));
        </script>
        """
        render_html_with_id = render_html.format(div_id,
            input_name,
            input_id,
            div_id,
            input_id, value)
        return render_html_with_id

    def __init__(self, *args, **kwargs):
        super(EditablePolygonWidget, self).__init__(*args, **kwargs)


class EditablePolygonField(forms.Field):
    def __init__(self,
        required= True,
        widget=EditablePolygonWidget,
        label=None,
        initial=None,
        help_text="",
        validators=[validate_polygon],
        *args,
        **kwargs):
        super(EditablePolygonField, self).__init__(required=required,
            widget=widget,
            label=label,
            initial=initial,
            help_text=help_text,
            validators=validators,
            *args,
            **kwargs)

    def to_python(self, value):
        # Convert to expected python value (list of lists of latlngs)
        value = super(EditablePolygonField, self).to_python(value)
        try:
            json_array = json.loads(value)
        except:
            raise ValidationError("Unable to parse input: '{}'".format(value),
                code="invalid")
        return json_array

    def validate(self, value):
        super(EditablePolygonField, self).validate(value)

    def widget_attrs(self, widget):
        attrs = super(EditablePolygonField, self).widget_attrs(widget)
        return attrs


#### Ajax string lookup utitlities

class AjaxStringLookupWidget(forms.Widget):
    """
    Widget for a string lookup with suggestions
    """
    class Media:
        css = {
            'all' : ("css/autocomplete.css",)
        }

        js = ("https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js",
              "js/jquery.autocomplete.min.js",
              "js/setup_ajax.js",
              "js/ajax_string_lookup.js",)
        
    def render(self, name, value, *args, **kwargs):
        div_id = 'ajax_text_field_' + kwargs['attrs']['id']
        input_name = name
        input_id = kwargs['attrs']['id']
        if value is None:
            value = 'null'
        render_html = "<input type='text' name='"+str(input_name)+"' id='"+str(input_id)+"' value='' />\n"
        render_html += '<script type="text/javascript">\n'
        render_html += "attach_ajax_string_listener(\""+self.ajax_url+"\", \""+str(input_id)+"\")\n"
        render_html += "</script>\n"

        return render_html

    def __init__(self, ajax_url, *args, **kwargs):
        self.ajax_url = ajax_url
        super(AjaxStringLookupWidget, self).__init__(*args, **kwargs)





class AjaxStringLookupField(forms.Field):
    def __init__(self,
        ajax_url,
        required= True,
        label=None,
        initial=None,
        help_text="",
        validators=[],
        *args,
        **kwargs):
        self.ajax_url = ajax_url
        # widget needs to be initialized every time, so it can't be done in the signature
        widget = AjaxStringLookupWidget(self.ajax_url)
        super(AjaxStringLookupField, self).__init__(required=required,
            widget=widget,
            label=label,
            initial=initial,
            help_text=help_text,
            validators=validators,
            *args,
            **kwargs)

    def widget_attrs(self, widget):
        attrs = super(AjaxStringLookupField, self).widget_attrs(widget)
        attrs["ajax_url"] = self.ajax_url
        return attrs


class AjaxAutocomplete:
    def __init__(self, matching_object_query, suggestion_function, ajax_url):
        # function taking the query string as input and returning a query set
        self.matching_object_query = matching_object_query
        # function taking an item and returning the string suggestion to be displayed to the user
        self.suggestion_function = suggestion_function
        self.ajax_url = ajax_url

    def get_url_pattern(self):
        return "^"+self.ajax_url.lstrip("/")+"$"

    def ajax_autocomplete_view(self, request):
        if request.is_ajax():
            v = request.body
            k, v = request.body.split('=')
            if k.strip() == "query":
                query_string = v.strip().replace('+',' ').lower()
                suggestion_set = self.matching_object_query(query_string)
                suggestions = [self.suggestion_function(x) for x in suggestion_set]
                ans = json.dumps({"query": query_string, "suggestions": suggestions})
                return HttpResponse(ans, content_type="application/json")
            else:
                return HttpResponse("I can't handle that type of input:"+str(k))
        else:
            return HttpResponse("this should be an ajax post")

    def get_new_form_field(self):
        return AjaxStringLookupField(self.ajax_url)



# create aac in advance
# form is imported by urls, 
states = {'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Deleware', 'Florida', 'Georgia'}
matching_object_query = lambda query: [i for i in states if i.lower().startswith(query)]
suggestion_function = lambda item: "How about:"+item
ajax_url = "autocomplete/"
state_aac = AjaxAutocomplete(matching_object_query, suggestion_function, ajax_url)



class SimpleTestWidgetForm(forms.Form):
    widget_a = forms.CharField(max_length=100)
    widget_b = state_aac.get_new_form_field()


    # widget_b = forms.CharField(max_length=100)
    # editable_polygon_field = EditablePolygonField(label="Test Polygon Field")
    # # editable_polygon_field_2 = EditablePolygonField(label="Test Polygon Field 2")
    # polygon_field = ShowPolygonField(label="Test Polygon Field", initial="[[1.0,2.0],[4.0,5.0],[7.0,1.0]]")
    # # polygon_field2 = ShowPolygonField(label="Test Polygon Field", initial="[[11.0,2.0],[41.0,5.0],[-7.0,1.0]]")

