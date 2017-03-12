from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from beat_the_bullshit.models import BeatTheBullshitProject, BeatTheBullshitItem, Quote, Fallacy, QuoteFallacyAssociation, QuoteFallacyQuizItemResponse
from .forms import CreateProjectForm, EditProjectForm
import os
import sys
import core.models as cm
import core.views as cv
import core.forms as cf
import core.tasks as ct
import json
import numpy as np
from urlparse import urlsplit

def new_project(request):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)
    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            project = BeatTheBullshitProject()
            project.name = form.cleaned_data["name"]
            project.owner_profile = profile
            project.topic_overview = form.cleaned_data["topic_overview"]
            project.save()

            for i in range(1,4):
                q_string = form.cleaned_data.get("quote"+str(i), None)
                if not q_string is None and not q_string=="":
                    q = Quote()
                    q.quote_string = q_string
                    q.speaker_name = form.cleaned_data["speaker_name"+str(i)]
                    q.reference = form.cleaned_data["reference"+str(i)]
                    screenshot_url = form.cleaned_data["screenshot_filename"+str(i)]
                    path_with_bucket_and_leading_slash = urlsplit(screenshot_url)[2]
                    path_without_bucket = "/".join(path_with_bucket_and_leading_slash.split("/")[2:])
                    q.screenshot_filename = path_without_bucket
                    if "youtube_video_id"+str(i) in form.cleaned_data:
                        q.youtube_video_id = form.cleaned_data["youtube_video_id"+str(i)]

                    q.project = project;
                    q.save()
                    
                    qfa = QuoteFallacyAssociation()
                    qfa.quote = q
                    qfa.fallacy = form.cleaned_data["fallacy"+str(i)]
                    qfa.explanation = form.cleaned_data["fallacy_association_explanation"+str(i)]
                    qfa.improvement = form.cleaned_data["fallacy_association_improvement"+str(i)]
                    qfa.save()

            # iterate through form adding tags
            for key, val in form.cleaned_data.items():
                if key.startswith("tag"):
                    t = cf.get_best_final_matching_tag(val)
                    if not t is None:
                        project.tags.add(t)

            ct.finalize_project(project)
            
            return render(request, 'core/thanks.html', {"action_description": "creating a new ballot decider project", "link": "/apps/beat_the_bullshit/administer_project/"+str(project.id)})
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
        BeatTheBullshitItem.objects.filter(participation_project=project, is_active=True).update(is_active=False)

def edit_project(request, project_id):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)
    project = get_object_or_404(BeatTheBullshitProject, pk=project_id) 
    basic_fields = ["name", "topic_overview"]

    if request.method == 'POST':
        form = EditProjectForm(project, request.POST)
        changes = set()
        if form.is_valid():
            for key in basic_fields:
                if not project.__dict__[key] == form.cleaned_data[key]:
                    project.__dict__[key] = form.cleaned_data[key]
                    changes.add(key)

            project.save()

            # allow adding more points of view, basics, and effects
            for i in range(1,4):
                quote = form.cleaned_data.get("quote"+str(i), None)
                if not quote is None and not quote=="":
                    q = Quote()
                    q.quote_string = quote
                    q.speaker_name = form.cleaned_data["speaker_name"+str(i)]
                    q.reference = form.cleaned_data["reference"+str(i)]
                    screenshot_url = form.cleaned_data["screenshot_filename"+str(i)]
                    path_with_bucket_and_leading_slash = urlsplit(screenshot_url)[2]
                    path_without_bucket = "/".join(path_with_bucket_and_leading_slash.split("/")[2:])
                    q.screenshot_filename = path_without_bucket
                    if "youtube_video_id"+str(i) in form.cleaned_data:
                        q.youtube_video_id = form.cleaned_data["youtube_video_id"+str(i)]

                    q.project = project;
                    q.save()
                    
                    qfa = QuoteFallacyAssociation()
                    qfa.quote = q
                    qfa.fallacy = form.cleaned_data["fallacy"+str(i)]
                    qfa.explanation = form.cleaned_data["fallacy_association_explanation"+str(i)]
                    qfa.improvement = form.cleaned_data["fallacy_association_improvement"+str(i)]
                    qfa.save()
            
            # Allow deleting quotes
            for key, val in form.cleaned_data.items():
                if key.startswith("delete_quote_") and val:
                    changes.add("del_quotes")
                    quote_id = int(key.replace("delete_quote_", ""))
                    assert(project.quote_set.filter(id=quote_id).exists())
                    project.quote_set.filter(id=quote_id).delete()
                    Quote.objects.filter(id=quote_id).delete() 
                    # quote-filter-assiciation is deleted with cascade

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

            return render(request, 'core/thanks.html', {"action_description": "editing your beat-the-bullshit project", "link": "/apps/beat_the_bullshit/administer_project/"+str(project.id)})
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path})

    else:
        data = {k: project.__dict__[k] for k in basic_fields}
        current_tags = list(project.tags.all())
        for i, t in enumerate(current_tags):
            if i > 2:
                break
            data["tag"+str(i+1)] = t.get_name()
        sys.stderr.write(str(data))
        sys.stderr.flush()
        form = EditProjectForm(project, data)
        return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path })


def administer_project(request, project_id):
    project = get_object_or_404(BeatTheBullshitProject, pk=project_id) 
    items = BeatTheBullshitItem.objects.filter(participation_project=project, is_active=True).distinct()
    return render(request, 'core/project_admin_base.html', {"items": [cv.get_item_details(i, True) for i in items if i.is_active], "project":project, 'site': os.environ["SITE"]})


def participate(request, item_id):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)
    item = BeatTheBullshitItem.objects.get(pk=item_id)
    context = cv.get_default_og_metadata(request, item)
    project = item.participation_project.beatthebullshitproject
    context.update({"project": project, 'site': os.environ["SITE"], "item": item, "fallacies": Fallacy.objects.all()})
    if not request.method == "POST":
        return render(request, 'beat_the_bullshit/participate.html', context)
    if request.method == 'POST' and request.is_ajax():
        submission_data = json.loads(request.body.strip())
        sys.stderr.write(str(submission_data))
        sys.stderr.flush()
        if "type" in submission_data and submission_data["type"] == "quote_fallacy_quiz_item_submit":
            qid = submission_data["quote_id"]
            quote = get_object_or_404(Quote, pk=qid, project=project)
            fid = submission_data["fallacy_id"]
            fallacy = get_object_or_404(Fallacy, pk=fid)
            response = QuoteFallacyQuizItemResponse()
            response.user_profile = profile
            response.participation_item = item
            response.choice = fallacy
            association = QuoteFallacyAssociation.objects.get(quote=quote) # assumes there is only one fallacy associated with this quote
            is_correct = (association.fallacy.id == fallacy.id)
            response.is_correct = is_correct
            response.save()

            content = dict()
            content["correct_fallacy_name"] = association.fallacy.name
            content["is_correct"] = is_correct
            content["explanation"] = association.explanation
            content["improvement"] = association.improvement
            return JsonResponse(content)
        else:
            return HttpResponse(status=500)


