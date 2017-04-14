from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from legislators.models import LegislatorsProject, LegislatorsItem
import os
import sys
import core.models as cm
import core.views as cv
import core.forms as cf
import core.tasks as ct
import json

def new_project(request):
    raise Exception("Legislator projects are created automatically, not through the web interface")

def administer_project(request, project_id):
    project = get_object_or_404(LegislatorsProject, pk=project_id) 
    items = LegislatorsItem.objects.filter(participation_project=project, is_active=True).distinct()
    return render(request, 'core/project_admin_base.html', {"items": [cv.get_item_details(i, True) for i in items if i.is_active], "project":project, 'site': os.environ["SITE"]})

def participate(request, item_id):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)
    item = LegislatorsItem.objects.get(pk=item_id)
    context = cv.get_default_og_metadata(request, item)
    project = item.participation_project.legislatorsproject
    context.update({'site': os.environ["SITE"], "item": item, "project":project})
    return render(request, "legislators/participate.html", context)

def overview(request):
    items = LegislatorsItem.objects.filter(is_active=True)[:100]
    return render(request, 'legislators/overview.html', {"items": [cv.get_item_details(i, True) for i in items if i.is_active], 'site':os.environ["SITE"]})
