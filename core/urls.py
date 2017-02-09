from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views
from . import forms

urlpatterns = [
    url(r'^donate/$', views.donate, name="donate"),
    url(r'^nonpartisanship/$', views.nonpartisanship, name="nonpartisanship"),
    url(r'^report_issues/$', views.report_issues, name="report_issues"),
    url(r'^report_issues/apps/(?P<app_name>.+)/(?P<action_name>.+)/(?P<object_id>.+)$', views.report_issues, name="report_issues"),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^accounts/profile/$', views.show_profile, name="profile"),
    url(r'^$', views.splash_if_anon, name="home"),
    url(r'^feed/$', views.feed, name="feed"),
    url(r'^upload_dataset/$', views.upload_dataset, name="upload_dataset"),
    url(r'^testgeo/$', views.test_geo, name="test_geo"),
    url(r'^tags/$', views.tags, name="tags"),
    url(r'^update_tags/$', views.update_profile_tags, name="update_tags"),
    url(r'^apps/(?P<app_name>.+)/(?P<action_name>.+)/(?P<object_id>.+)$', views.app_view_relay, name="app_view_relay"),
    url(forms.tag_aac.get_url_pattern(), forms.tag_aac.ajax_autocomplete_view, name=""),
    url(r'^create_shortcut/$', views.create_shortcut, name="create_shortcut"),
    url(r'^(?P<shortcut_str>.+)/$', views.shortcut, name="shortcut")
]
