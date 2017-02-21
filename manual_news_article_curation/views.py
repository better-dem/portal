from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from manual_news_article_curation.forms import CreateProjectForm, EditProjectForm
from manual_news_article_curation.models import ManualNewsCurationProject, NewsArticleItem
import core.views as cv
import core.models as cm
import core.tasks as ct
import core.forms as cf
import sys
from urlparse import urlsplit
import os

def new_project(request):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)

    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            project = ManualNewsCurationProject()
            project.name = form.cleaned_data["name"]
            project.url = form.cleaned_data["url"]
            project.first_paragraph = form.cleaned_data["first_paragraph"]
            screenshot_url = form.cleaned_data["screenshot"]
            path_with_bucket_and_leading_slash = urlsplit(screenshot_url)[2]
            path_without_bucket = "/".join(path_with_bucket_and_leading_slash.split("/")[2:])
            project.screenshot_filename = path_without_bucket
            project.owner_profile = profile
            project.save()

            # iterate through form adding tags
            for key, val in form.cleaned_data.items():
                if key.startswith("tag"):
                    t = cf.get_best_final_matching_tag(val)
                    if not t is None:
                        project.tags.add(t)
            
            ct.finalize_project(project)
            
            return render(request, 'core/thanks.html', {"action_description": "creating a new news article project", "link": "/apps/manual_news_article_curation/administer_project/"+str(project.id)})
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path})
    else:
        form = CreateProjectForm()
        return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path })

def propagate_project_changes(project, change_set):
    if "tags" in change_set or "name" in change_set:
        sys.stderr.write("changes are significant, we have to de-activate and re-create items for this project")
        sys.stderr.flush()
        # de-activate all existing items and re-create items for this project
        NewsArticleItem.objects.filter(participation_project=project, is_active=True).update(is_active=False)

def edit_project(request, project_id):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)
    project = get_object_or_404(ManualNewsCurationProject, pk=project_id) 
    basic_fields = ["name", "url", "first_paragraph"]

    if request.method == 'POST':
        form = EditProjectForm(request.POST)
        changes = set()
        if form.is_valid():
            for key in basic_fields:
                if not project.__dict__[key] == form.cleaned_data[key]:
                    project.__dict__[key] = form.cleaned_data[key]
                    changes.add(key)
            # ignore screenshot, too hard
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
            ct.finalize_project(project)
            return render(request, 'core/thanks.html', {"action_description": "editing your tool review", "link": "/apps/tool_review/administer_project/"+str(project.id)})
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path})

    else:
        data = {k: project.__dict__[k] for k in basic_fields}
        current_tags = list(project.tags.all())
        for i, t in enumerate(current_tags):
            if i > 2:
                break
            data["tag"+str(i+1)] = t.get_name()
        form = EditProjectForm(data)
        return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path })

def administer_project(request, project_id):
    project = get_object_or_404(ManualNewsCurationProject, pk=project_id)
    items = NewsArticleItem.objects.filter(participation_project=project)
    return render(request, 'core/project_admin_base.html', {"items": [cv.get_item_details(i, True) for i in items if i.is_active], "project":project, 'site': os.environ["SITE"]})

def participate(request, item_id):
    item = get_object_or_404(NewsArticleItem, pk=item_id)
    project = item.participation_project.manualnewscurationproject
    return redirect(project.url)

