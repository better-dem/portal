from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from tool_review.models import ToolReviewProject, ToolReviewItem
from .forms import CreateProjectForm
from django.db.models import Count
import os
import sys
import core.models as cm
import core.views as cv
from django.contrib.gis.geos import GEOSGeometry, Polygon, LinearRing
from urlparse import urlsplit

def new_project(request):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)

    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            project = ToolReviewProject()
            project.name = form.cleaned_data["tool_name"]
            screenshot_url = form.cleaned_data["screenshot"]
            sys.stderr.write("screenshotURL:" + screenshot_url + "\n")
            path_with_bucket_and_leading_slash = urlsplit(screenshot_url)[2]
            sys.stderr.write("path with bucket: " + path_with_bucket_and_leading_slash+"\n")
            path_without_bucket = "/".join(path_with_bucket_and_leading_slash.split("/")[2:])
            sys.stderr.write("path without bucket: " + path_without_bucket+"\n")
            project.screenshot_filename = path_without_bucket
            project.summary = form.cleaned_data["summary"]
            project.owner_profile = profile
            project.save()
            
            return render(request, 'core/thanks.html', {"action_description": "creating a new tool review", "link": "/apps/tool_review/administer_project/"+str(project.id)})
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path})
    else:
        form = CreateProjectForm()
        return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path })

def administer_project(request, project_id):
    project = get_object_or_404(ToolReviewProject, pk=project_id) 
    items = ToolReviewItem.objects.filter(participation_project=project)
    return render(request, 'core/generic_project_stats.html', {"items": [cv.get_item_details(i, True) for i in items]})


def participate(request, item_id):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)

    item = ToolReviewItem.objects.get(pk=item_id)
    context = cv.get_default_og_metadata(request, item)
    project = item.participation_project.toolreviewproject

    context.update({"review": project})
    sys.stderr.write("screenshot filename:" + project.screenshot_filename + "\n")
    sys.stderr.flush()
    return render(request, 'tool_review/participate.html', context)


