from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views
from . import forms

urlpatterns = [
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^accounts/profile', views.show_profile, name="profile"),
    url(r'^$', views.feed, name="feed"),
    url(r'^upload_dataset$', views.upload_dataset, name="upload_dataset"),
    url(r'^testgeo$', views.test_geo, name="test_geo"),
    url(r'^tags$', views.tags, name="tags"),
    url(r'^update_tags$', views.update_profile_tags, name="update_tags"),
    url(r'^apps/(?P<app_name>.+)/(?P<action_name>.+)/(?P<project_id>.+)/(?P<item_id>.+)$', views.app_view_relay, name="app_view_relay"),
    url(forms.tag_aac.get_url_pattern(), forms.tag_aac.ajax_autocomplete_view, name="")

    # url('', include('django.contrib.auth.urls')),
]
