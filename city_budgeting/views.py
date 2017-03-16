from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from city_budgeting.models import CityBudgetingProject, CityBudgetingItem
from .forms import CreateProjectForm
import os
import sys
import core.views as cv
import core.forms as cf
import core.models as cm
import core.tasks as ct
import json

def new_project(request):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)

    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            project = CityBudgetingProject()
            project.city = cf.get_best_final_matching_tag(form.cleaned_data["place_name"]).geotag
            project.fiscal_period_start = form.cleaned_data["fiscal_period_start"]
            project.fiscal_period_end = form.cleaned_data["fiscal_period_end"]
            project.budget_json = form.cleaned_data["budget_json"]
            project.name = "City Budget Outreach Project for "+project.city.get_name()
            project.budget_url = form.cleaned_data["budget_url"]
            project.owner_profile = profile
            project.save()

            ct.finalize_project(project)
            
            return render(request, 'core/thanks.html', {"action_description": "creating a new city budget project", "link": "/apps/city_budgeting/administer_project/"+str(project.id)})
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path})
    else:
        form = CreateProjectForm()
        return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path })


def administer_project(request, project_id):
    project = get_object_or_404(CityBudgetingProject, pk=project_id)
    items = CityBudgetQuiz.objects.filter(participation_project=project,  is_active=True).distinct()
    return render(request, 'core/project_admin_base.html', {"items": [cv.get_item_details(i, True) for i in items if i.is_active], "project":project, 'site': os.environ["SITE"]})


def participate(request, item_id):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)
    item = CityBudgetingItem.objects.get(pk=item_id)
    context = cv.get_default_og_metadata(request, item)
    project = item.participation_project.citybudgetingproject
    context.update({"project": project, "data":json.loads(project.budget_json), "site": os.environ["SITE"]})
    return render(request, "city_budgeting/participate.html", context)
