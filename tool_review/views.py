from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from tool_review.models import ToolReviewProject, ToolReviewItem
from .forms import CreateProjectForm
from django.db.models import Count
import os
import sys
import core.models as cm
import core.views as cv
import core.forms as cf
from django.contrib.gis.geos import GEOSGeometry, Polygon, LinearRing
from urlparse import urlsplit

def new_project(request):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)

    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            project = ToolReviewProject()
            project.name = form.cleaned_data["tool_name"]
            project.url = form.cleaned_data["tool_url"]
            screenshot_url = form.cleaned_data["screenshot"]
            path_with_bucket_and_leading_slash = urlsplit(screenshot_url)[2]
            path_without_bucket = "/".join(path_with_bucket_and_leading_slash.split("/")[2:])
            project.screenshot_filename = path_without_bucket

            if "youtube_video_id" in form.cleaned_data:
                project.youtube_video_id = form.cleaned_data["youtube_video_id"]

            project.summary = form.cleaned_data["summary"]
            project.owner_profile = profile
            project.save()

            t1 = cf.get_best_final_matching_tag(form.cleaned_data["tag1"])
            if not t1 is None:
                project.tags.add(t1)
            t2 = cf.get_best_final_matching_tag(form.cleaned_data["tag2"])
            if not t2 is None:
                project.tags.add(t2)
            t3 = cf.get_best_final_matching_tag(form.cleaned_data["tag3"])
            if not t3 is None:
                project.tags.add(t3)
            
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
    return render(request, 'tool_review/participate.html', context)


