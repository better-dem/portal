from django.shortcuts import render
from django.http import HttpResponse
import sys
from dummy_participation_project.models import DummyProject, DummyItem

def new_project(request):
    return HttpResponse("dummy app's new project view -- not yet implemented")

def administer_project(request, project_id):
    return HttpResponse("dummy app's administer project view -- not yet implemented")

def participate(request, item_id):
    sys.stdout.write("dummy project views.participate called\n")
    sys.stdout.flush()
    
    return HttpResponse("dummy app's participate view"+str(item_id)+" -- not yet implemented")

