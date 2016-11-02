from django.conf.urls import url

from . import views
from . import forms

urlpatterns = [
    url(r'^demo_map$', views.demo_map, name = 'demo_map'),
    url(r'^demo_poly_mark$', views.demo_poly_mark, name = 'demo_poly_mark'),
    url(r'^simple_test_widget$', views.simple_test_widget, name = 'simple_test_widget'),
    # url(r'^autocomplete/$', forms.aac.ajax_autocomplete_view, name="autocomplete")
    url(forms.state_aac.get_url_pattern(), forms.state_aac.ajax_autocomplete_view, name="state_autocomplete")
]
