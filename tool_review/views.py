from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import Template, Context
from tool_review.models import ToolReviewProject, ToolReviewItem, TOOL_CATEGORIES, PROJECT_CATEGORIES
from .forms import CreateProjectForm, EditProjectForm
from django.db.models import Count
import os
import sys
import core.models as cm
import core.views as cv
import core.forms as cf
import core.tasks as ct
from urlparse import urlsplit
import csv, io

def new_project(request):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)

    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            project = ToolReviewProject()
            project.name = form.cleaned_data["tool_name"]
            project.url = form.cleaned_data["tool_url"]
            project.tool_category = form.cleaned_data["tool_category"]
            project.project_category = form.cleaned_data["project_category"]
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
            
            ct.finalize_project(project)
                
            return render(request, 'core/thanks.html', {"action_description": "creating a new tool review", "link": "/apps/tool_review/administer_project/"+str(project.id)})
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
        ToolReviewItem.objects.filter(participation_project=project, is_active=True).update(is_active=False)

def edit_project(request, project_id):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)
    project = get_object_or_404(ToolReviewProject, pk=project_id) 

    if request.method == 'POST':
        form = EditProjectForm(request.POST)
        changes = set()
        if form.is_valid():
            for k in ["tool_name", "tool_url"]:
                if not project.__dict__[k.split("_")[1]] == form.cleaned_data[k]:
                    project.__dict__[k.split("_")[1]] = form.cleaned_data[k]
                    changes.add(k.split("_")[1])

            for k in ["tool_category", "project_category", "summary"]:
                if not project.__dict__[k] == form.cleaned_data[k]:
                    project.__dict__[k] = form.cleaned_data[k]
                    changes.add(k)

            # currently we don't support updating screenshot, too much work

            if "youtube_video_id" in form.cleaned_data and \
               ( project.youtube_video_id is None or \
                 not project.youtube_video_id == form.cleaned_data["youtube_video_id"] ) : 
                project.youtube_video_id = form.cleaned_data["youtube_video_id"]
                changes.add("video")
            elif not project.youtube_video_id is None and not "youtube_video_id" in form.cleaned_data:
                del project.youtube_video_id
                changes.add("video")
            project.save()

            current_tags = set(project.tags.all())
            new_tags = set()
            t1 = cf.get_best_final_matching_tag(form.cleaned_data["tag1"])
            if not t1 is None:
                new_tags.add(t1)
            t2 = cf.get_best_final_matching_tag(form.cleaned_data["tag2"])
            if not t2 is None:
                new_tags.add(t2)
            t3 = cf.get_best_final_matching_tag(form.cleaned_data["tag3"])
            if not t3 is None:
                new_tags.add(t3)

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
        data = {"tool_name": project.name, "tool_url": project.url, "summary": project.summary, "tool_category": project.tool_category, "project_category": project.project_category}
        if not project.youtube_video_id is None:
            data["youtube_video_id"] = project.youtube_video_id
        current_tags = list(project.tags.all())
        for i, t in enumerate(current_tags):
            if i > 2:
                break
            data["tag"+str(i+1)] = t.get_name()
        form = EditProjectForm(data)
        return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path })
    

def administer_project(request, project_id):
    project = get_object_or_404(ToolReviewProject, pk=project_id) 
    items = ToolReviewItem.objects.filter(participation_project=project)
    return render(request, 'core/project_admin_base.html', {"items": [cv.get_item_details(i, True) for i in items if i.is_active], "project": project, 'site':os.environ["SITE"]})


def participate(request, item_id):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)

    item = ToolReviewItem.objects.get(pk=item_id)
    context = cv.get_default_og_metadata(request, item)
    project = item.participation_project.toolreviewproject

    context.update({"review": project, 'item': item})
    return render(request, 'tool_review/participate.html', context)

def overview(request):
    items = ToolReviewItem.objects.all()[:100]
    return render(request, 'tool_review/overview.html', {"items": [cv.get_item_details(i, True) for i in items if i.is_active], 'site':os.environ["SITE"], "tool_categories": [x[1] for x in TOOL_CATEGORIES], "project_categories": [x[1] for x in PROJECT_CATEGORIES]})

def customActionDownloadOverviewCsv(request, ignore):
    projects = ToolReviewProject.objects.filter(is_active=True)
    csv_data = None
    with io.BytesIO() as s:
        w = csv.writer(s, dialect='excel', delimiter=',')
        w.writerow(["id","name","url", "summary","tool category","project category"])
        for p in projects:
            w.writerow([unicode(x).encode("utf-8") for x in [p.id, p.name, p.url, p.summary, p.get_tool_category_display(), p.get_project_category_display()]])
        csv_data = s.getvalue()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tool_review_overview.csv"'
    t = Template("{{ data }}")
    response.write(t.render(Context({"data": csv_data})))
    return response


