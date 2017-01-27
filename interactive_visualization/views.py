from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from interactive_visualization.models import InteractiveVisualizationProject, InteractiveVisualizationItem
from interactive_visualization.forms import CreateProjectForm
import sys
import core.models as cm
import core.views as cv
import core.forms as cf
import json

def new_project(request):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)
    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            project = SingleQuizProject()
            project.name = form.cleaned_data["visualization_title"]
            # first time through, create the project
            for key, val in form.cleaned_data.items():
                if key == "visualization_title":
                    project.name = val
                elif not key.startswith("tag"):
                    project.__dict__[key] = val
            project.save()

            # second time, add tags to the project
            for key, val in form.cleaned_data.items():
                if key.startswith("tag"):
                    t = cf.get_best_final_matching_tag(form.cleaned_data["tag1"])
                    if not t is None:
                        project.tags.add(t)

            return render(request, 'core/thanks.html', {"action_description": "creating a new interactive visualization", "link": "/apps/interactive_visualization/administer_project/"+str(project.id)})
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path})
    else:
        form = CreateProjectForm()
        return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path })

def participate(request, item_id):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)
    item = InteractiveVisualizationItem.objects.get(pk=item_id)
    context = cv.get_default_og_metadata(request, item)
    project = item.participation_project.interactivevisualizationproject
    context["project"] = project
    return render(request, 'interactive_visualization/participate.html', context)

def administer_project(request, project_id):
    project = get_object_or_404(InteractiveVisualizationProject, pk=project_id) 
    items = InteractiveVisualizationItem.objects.filter(participation_project=project)
    return render(request, 'core/project_admin_base.html', {"items": [cv.get_item_details(i, True) for i in items if i.is_active], "project": project})
