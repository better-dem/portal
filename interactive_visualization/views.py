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
            project = InteractiveVisualizationProject()
            project.owner_profile = profile
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
                    t = cf.get_best_final_matching_tag(form.cleaned_data[key])
                    if not t is None:
                        project.tags.add(t)

            return render(request, 'core/thanks.html', {"action_description": "creating a new interactive visualization", "link": "/apps/interactive_visualization/administer_project/"+str(project.id)})
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path})
    else:
        form = CreateProjectForm()
        return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path })

def propagate_project_changes(project, change_set):
    sys.stderr.write("changes:"+str(change_set)+"\n")
    sys.stderr.flush()

    if "tags" in change_set or "name" in change_set:
        sys.stderr.write("changes are significant, we have to de-activate and re-create items for this project")
        sys.stderr.flush()
        # de-activate all existing items and re-create items for this project
        InteractiveVisualizationItem.objects.filter(participation_project=project, is_active=True).update(is_active=False)
        project.update_items()

def edit_project(request, project_id):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)
    project = get_object_or_404(InteractiveVisualizationProject, pk=project_id) 

    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        changes = set()
        if form.is_valid():
            for key, val in form.cleaned_data.items():
                if key == "visualization_title":
                    if not project.name == val:
                        changes.add("name")
                        project.name = val
                elif not key.startswith("tag"):
                    if not project.__dict__[key] == val:
                        project.__dict__[key] = val
                        changes.add(key)
            project.save()

            current_tags = set(project.tags.all())
            new_tags = set()
            for key, val in form.cleaned_data.items():
                if key.startswith("tag"):
                    t = cf.get_best_final_matching_tag(val)
                    if not t is None:
                        new_tags.add(t)
            
            if len(new_tags.symmetric_difference(current_tags)) > 0:
                project.tags.clear()
                project.tags.add(*new_tags)
                changes.add("tags")

            propagate_project_changes(project, changes)

            return render(request, 'core/thanks.html', {"action_description": "editing your interactive visualization", "link": "/apps/interactive_visualization/administer_project/"+str(project.id)})
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path})

    else:
        data = {i: project.__dict__[i] for i in ["methodology_note", "methodology_url", "csv_data", "switch_variable", "switch_title", "switch_note", "pie1_variable", "pie1_title", "pie2_variable", "pie2_title", "bar1_variable", "bar1_title", "bar1_x_label", "bar1_y_label", "bar2_variable", "bar2_title", "bar2_x_label", "bar2_y_label"]}
        data["visualization_title"] = project.name
        current_tags = list(project.tags.all())
        for i, t in enumerate(current_tags):
            if i > 2:
                break
            data["tag"+str(i+1)] = t.get_name()
        form = CreateProjectForm(data)
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
