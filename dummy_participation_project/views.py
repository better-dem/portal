from django.shortcuts import render
from django.http import HttpResponse

def new_project(request):
    return HttpResponse(request, "dummy app's new project view -- not yet implemented")

def show_project_results(request, project_id):
    return HttpResponse(request, "dummy app's project results view -- not yet implemented")

def administer_project(request, project_id):
    return HttpResponse(request, "dummy app's administer project view -- not yet implemented")

def participate(request, item_id):
    return HttpResponse(request, "dummy app's participate view"+str(item_id)+" -- not yet implemented")

