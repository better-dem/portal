from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from legislators.models import LegislatorsProject, LegislatorsItem, BillsProject, BillsItem
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
    item = None
    project = None
    item_type = None
    try:
        item = LegislatorsItem.objects.get(pk=item_id)
        project = item.participation_project.legislatorsproject
        item_type = "legislators"
    except LegislatorsItem.DoesNotExist:
        item = BillsItem.objects.get(pk=item_id)
        project = item.participation_project.billsproject
        item_type = "bills"
    context = cv.get_default_og_metadata(request, item)
    context.update({'site': os.environ["SITE"], "item": item, "project":project})
    return render(request, "legislators/{}_participate.html".format(item_type), context)

def overview(request, item_id):
    if item_id == "-1":
        items = LegislatorsItem.objects.filter(is_active=True)[:100]
        return render(request, 'legislators/overview.html', {"items": [cv.get_item_details(i, True) for i in items if i.is_active], 'site':os.environ["SITE"]})
    elif item_id == "0":
        items = BillsItem.objects.filter(is_active=True)[:100]
        return render(request, 'legislators/bills_overview.html', {"items": [cv.get_item_details(i, True) for i in items if i.is_active], 'site':os.environ["SITE"]})
