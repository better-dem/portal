from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from legislators.models import LegislatorsProject, LegislatorsItem, BillsProject, BillsItem
from legislators.forms import SearchQueryForm
import os
import sys
import core.models as cm
import core.views as cv
import core.forms as cf
import core.tasks as ct
import json

def new_project(request, group=None):
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
    context=dict()
    try:
        item = LegislatorsItem.objects.get(pk=item_id)
        project = item.participation_project.legislatorsproject
        item_type = "legislators"
    except LegislatorsItem.DoesNotExist:
        item = BillsItem.objects.get(pk=item_id)
        state = [s for s in cm.GeoTag.objects.filter(feature_type = "SP") if s.tag_ptr in item.tags.all()][0]
        context["state"] = {"id": state.tag_ptr.id, "name":state.name}
        project = item.participation_project.billsproject
        item_type = "bills"
    context.update(cv.get_default_og_metadata(request, item))
    context.update({'site': os.environ["SITE"], "item": item, "project":project})
    return render(request, "legislators/{}_participate.html".format(item_type), context)

def overview(request, item_id):
    context = {}
    states = cm.GeoTag.objects.filter(feature_type = "SP")
    context["states"] = [{"id": s.tag_ptr.id, "name": s.name} for s in states]
    context["action_path"] = request.path
    if item_id == "-1":
        # Legislators Overview
        if request.method == "POST":
            form = SearchQueryForm(request.POST)
            if form.is_valid():
                state = [s for s in states if s.tag_ptr.id == form.cleaned_data["state_id"]][0]
                results = LegislatorsItem.objects.filter(is_active=True, tags__in=[state.tag_ptr]).distinct()
                context["results"] = [r for r in results if not r.participation_project.legislatorsproject.district is None and not r.participation_project.legislatorsproject.chamber is None]
                context["query_description"] = "State of {}".format(state.name)
                return render(request, "legislators/overview.html", context)
            else:
                raise Exception("error in form, this shouldn't happen through normal usage of the site")

        else:
            return render(request, "legislators/overview.html", context)

    elif item_id == "-2":
        # Bills Overview
        if request.method == "POST":
            form = SearchQueryForm(request.POST)
            if form.is_valid():
                state = [s for s in states if s.tag_ptr.id == form.cleaned_data["state_id"]][0]
                vector = SearchVector('name')
                query = SearchQuery(form.cleaned_data['query_text'])
                results = BillsItem.objects.filter(is_active=True, tags__in=[state.tag_ptr]).annotate(rank=SearchRank(vector, query)).distinct().order_by('-rank')[:100]
                context["results"] = results
                context["query_description"] = "\"{}\" in the state of {}".format(form.cleaned_data["query_text"], state.name)
                return render(request, "legislators/bills_overview.html", context)
            else:
                raise Exception("error in form, this shouldn't happen through normal usage of the site")

        else:
            return render(request, "legislators/bills_overview.html", context)
