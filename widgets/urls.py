from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^demo_map$', views.demo_map, name = 'demo_map'),
    url(r'^demo_poly_mark$', views.demo_poly_mark, name = 'demo_poly_mark'),
    url(r'^simple_test_widget$', views.simple_test_widget, name = 'simple_test_widget')
]
