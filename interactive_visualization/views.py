from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
# from interactive_visualization.models import *
import sys
import core.models as cm
import core.views as cv
import core.forms as cf
import json

def new_project(request):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)
    return render(request, 'interactive_visualization/participate.html')
