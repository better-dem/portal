from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from city_budgeting.models import CityBudgetingProject, CityBudgetingItem
from city_budgeting.forms import CreateProjectForm
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
            project.city = cf.get_best_final_matching_tag(form.cleaned_data["city"]).geotag
            project.fiscal_period_start = form.cleaned_data["fiscal_period_start"]
            project.fiscal_period_end = form.cleaned_data["fiscal_period_end"]
            project.budget_json = form.cleaned_data["budget_json"]
            project.set_name()
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

def edit_project(request, project_id):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)
    project = get_object_or_404(CityBudgetingProject, pk=project_id) 
    simple_fields = ["fiscal_period_start", "fiscal_period_end", "budget_json", "budget_url"]
    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        changes = set()
        if form.is_valid():
            for k in simple_fields:
                if not project.__dict__[k] == form.cleaned_data[k]:
                    project.__dict__[k] = form.cleaned_data[k]
                    changes.add(k)

            form_city = cf.get_best_final_matching_tag(form.cleaned_data["city"]).geotag
            if not project.city == form_city:
                project.city = form_city
                changes.add("city")
                project.set_name()
                changes.add("name")
            project.save()

            if "name" in changes or "city" in changes:
                ct.finalize_project(project)
            return render(request, 'core/thanks.html', {"action_description": "editing your city budget project", "link": "/apps/city_budgeting/administer_project/"+str(project.id)})
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path})

    else:
        data = {k: project.__dict__[k] for k in simple_fields}
        data["city"] = project.city.get_name()
        form = CreateProjectForm(data)
        return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path })


def administer_project(request, project_id):
    project = get_object_or_404(CityBudgetingProject, pk=project_id)
    items = CityBudgetingItem.objects.filter(participation_project=project,  is_active=True).distinct()
    return render(request, 'core/project_admin_base.html', {"items": [cv.get_item_details(i, True) for i in items if i.is_active], "project":project, 'site': os.environ["SITE"]})


def participate(request, item_id):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)
    item = CityBudgetingItem.objects.get(pk=item_id)
    context = cv.get_default_og_metadata(request, item)
    project = item.participation_project.citybudgetingproject
    data = json.loads(project.budget_json)
    fund_map = {i["id"]: i for i in data["funds"]["items"]}
    revenue_categories = {i[0]: i[1] for i in enumerate(set([x["category"] for x in data["revenues"]["items"]]))}
    expense_categories = {i[0]: i[1] for i in enumerate(set([x["category"] for x in data["expenses"]["items"]]))}
    context.update({"project": project, "data":data, "site": os.environ["SITE"], "item":item, "fund_map":fund_map, "revenue_categories": revenue_categories, "expense_categories": expense_categories})
    return render(request, "city_budgeting/participate.html", context)
