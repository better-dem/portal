from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^create_project[/|]$', views.new_project, name = 'create_project'),
    url(r'^show_projects$', views.show_projects, name = 'show_projects'),
    url(r'^show_project/(?P<project_id>\d+)$', views.show_project, name = 'show_project'),
    url(r'^project_response/(?P<project_id>\d+)$', views.project_response, name = 'project_response')
]
