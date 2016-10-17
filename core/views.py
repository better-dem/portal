from django.shortcuts import render
from django.http import HttpResponse
from core.models import UserProfile

def show_profile(request):
    user = request.user
    profile = user.userprofile
    return HttpResponse("user email: "+str(user.email))

