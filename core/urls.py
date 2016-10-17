from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^accounts/profile', views.show_profile, name="profile")
    # url('', include('django.contrib.auth.urls')),
]
