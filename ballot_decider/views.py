from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from ballot_decider.models import BallotDeciderProject, BallotDeciderItem, PointOfView, POVToolResponse, POVItemResponse
from .forms import CreateProjectForm, ParticipateForm, EditProjectForm
import os
import sys
import core.models as cm
import core.views as cv
import core.forms as cf
import core.tasks as ct
import json
import numpy as np

def new_project(request):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)

    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            project = BallotDeciderProject()
            project.name = form.cleaned_data["measure_name"]
            project.owner_profile = profile
            project.ballot_text = form.cleaned_data["ballot_text"]
            project.election_date = form.cleaned_data["election_date"]
            project.election_website = form.cleaned_data["election_website"]
            if "basics_notes" in form.cleaned_data and not form.cleaned_data["basics_notes"] == "":
                project.basics_notes = form.cleaned_data["basics_notes"]
            if "effects_notes" in form.cleaned_data and not form.cleaned_data["effects_notes"] == "":
                project.effects_notes = form.cleaned_data["effects_notes"]
            project.save()

            for i in range(1,4):
                data = form.cleaned_data.get("basics"+str(i), None)
                if not data is None and not data=="":
                    item = cm.ParticipationItem.objects.get(id=data, is_active=True)
                    project.basics.add(item)

            for i in range(1,4):
                data = form.cleaned_data.get("effects"+str(i), None)
                if not data is None and not data=="":
                    item = cm.ParticipationItem.objects.get(id=data, is_active=True)
                    project.effects.add(item)

            for i in range(1,4):
                quote = form.cleaned_data.get("pov_quote_"+str(i), None)
                if not quote is None and not quote=="":
                    pov = PointOfView()
                    pov.quote = quote
                    pov.is_favorable = form.cleaned_data["pov_is_favorable_"+str(i)]
                    pov.save()
                    project.points_of_view.add(pov)

            # iterate through form adding tags
            for key, val in form.cleaned_data.items():
                if key.startswith("tag"):
                    t = cf.get_best_final_matching_tag(val)
                    if not t is None:
                        project.tags.add(t)

            ct.finalize_project(project)
            
            return render(request, 'core/thanks.html', {"action_description": "creating a new ballot decider project", "link": "/apps/ballot_decider/administer_project/"+str(project.id)})
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path})
    else:
        form = CreateProjectForm()
        return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path })

def edit_project(request, project_id):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)
    project = get_object_or_404(BallotDeciderProject, pk=project_id) 
    basic_fields = {"name": "measure_name", "ballot_text": "ballot_text", "election_date": "election_date", "election_website": "election_website", "basics_notes": "basics_notes", "effects_notes": "effects_notes"}

    if request.method == 'POST':
        form = EditProjectForm(project, request.POST)
        changes = set()
        if form.is_valid():
            for key in basic_fields:
                if not project.__dict__[key] == form.cleaned_data[basic_fields[key]]:
                    project.__dict__[key] = form.cleaned_data[basic_fields[key]]
                    changes.add(key)

            project.save()

            # allow adding more points of view, basics, and effects
            for i in range(1,4):
                data = form.cleaned_data.get("basics"+str(i), None)
                if not data is None and not data=="":
                    item = cm.ParticipationItem.objects.get(id=data, is_active=True)
                    project.basics.add(item)
                    changes.add("basics")

            for i in range(1,4):
                data = form.cleaned_data.get("effects"+str(i), None)
                if not data is None and not data=="":
                    item = cm.ParticipationItem.objects.get(id=data, is_active=True)
                    project.effects.add(item)
                    changes.add("effects")

            for i in range(1,4):
                quote = form.cleaned_data.get("pov_quote_"+str(i), None)
                if not quote is None and not quote=="":
                    pov = PointOfView()
                    pov.quote = quote
                    pov.is_favorable = form.cleaned_data["pov_is_favorable_"+str(i)]
                    pov.save()
                    project.points_of_view.add(pov)
                    changes.add("povs")
            
            # Allow deleting POVs
            for key, val in form.cleaned_data.items():
                if key.startswith("delete_pov_") and val:
                    changes.add("del_povs")
                    pov_id = int(key.replace("delete_pov_", ""))
                    assert(project.points_of_view.filter(id=pov_id).exists())
                    project.points_of_view.filter(id=pov_id).delete()
                    PointOfView.objects.filter(id=pov_id).delete()

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

            if "name" in changes or "tags" in changes:
                ct.finalize_project(project)

            return render(request, 'core/thanks.html', {"action_description": "editing your ballot decider", "link": "/apps/ballot_decider/administer_project/"+str(project.id)})
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path})

    else:
        data = {i[1]: project.__dict__[i[0]] for i in basic_fields.items()}
        current_tags = list(project.tags.all())
        for i, t in enumerate(current_tags):
            if i > 2:
                break
            data["tag"+str(i+1)] = t.get_name()
        form = EditProjectForm(project, data)
        return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path })


def administer_project(request, project_id):
    project = get_object_or_404(BallotDeciderProject, pk=project_id) 
    items = BallotDeciderItem.objects.filter(participation_project=project, is_active=True).distinct()

    item_details = []
    for item in items:
        current_item_detail = cv.get_item_details(item, True)
        responses = POVToolResponse.objects.filter(participation_item=item).distinct()
        num_responses = responses.count()
        num_yes = responses.filter(final_decision__gt = 0).count()
        num_no = responses.filter(final_decision__lt = 0).count()
        num_undecided = responses.filter(final_decision = 0).count()
        num_extreme = responses.filter(final_decision__abs__gt = .15).count()
        current_item_detail["num_decisions"] = num_responses
        current_item_detail["outcome"] = "Num Yes:"+str(num_yes)+", Num No:"+str(num_no)+", Num undecided:"+str(num_undecided)
        if num_responses == 0:
            current_item_detail["fraction_strong"] = 0.0
        else:
            current_item_detail["fraction_strong"] = 1.0 * num_extreme / responses.count()

        pov_details = []
        for pov in PointOfView.objects.filter(ballotdeciderproject=project).distinct():
            current_pov_detail = dict()
            current_pov_detail["quote"] = pov.quote
            pov_item_responses = POVItemResponse.objects.filter(point_of_view=pov)
            scores = [x.score for x in pov_item_responses]
            current_pov_detail["num"] = len(scores)
            current_pov_detail["avg"] = np.mean(scores)
            current_pov_detail["stdev"] = np.std(scores)
            pov_details.append(current_pov_detail)

        current_item_detail["povs"] = pov_details
        item_details.append(current_item_detail)

    return render(request, 'ballot_decider/project_results.html', {"items": item_details, "project": project, 'site': os.environ["SITE"]})





def participate(request, item_id):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)
    item = BallotDeciderItem.objects.get(pk=item_id)
    context = cv.get_default_og_metadata(request, item)
    project = item.participation_project.ballotdeciderproject
    context.update({"ballot": project, "basics": [cv.get_item_details(i, False) for i in project.basics.all() if i.is_active], "effects": [cv.get_item_details(i, False) for i in project.effects.all() if i.is_active], 'site': os.environ["SITE"], "item": item})
    if not request.method == "POST":
        return render(request, 'ballot_decider/participate.html', context)
    if request.method == 'POST' and request.is_ajax():
        submission_data = json.loads(request.body.strip())
        form = ParticipateForm(item, submission_data)
        if form.is_valid():
            submission = POVToolResponse()
            submission.user_profile = profile
            submission.participation_item = item
            submission.save()
            for k in form.cleaned_data.keys():
                if "pov_weight" in k:
                    pov_id = int(k.replace("pov_weight_", ""))
                    pov = PointOfView.objects.get(id=pov_id)
                    item_response = POVItemResponse()
                    item_response.point_of_view = pov
                    item_response.score = int(form.cleaned_data[k])
                    item_response.tool_response = submission
                    item_response.save()

            decision, explanation = submission.generate_decision()
            submission.final_decision = decision
            submission.save()
            
            content = dict()
            content["reveal"] = ["response"]
            content["hide"] = ["ajax_form"]
            content["explanation"] = explanation
            if decision == 0:
                content["reveal"].append("no-decision")
            elif decision >= .15:
                content["reveal"].append("strong-yes")
            elif decision > 0:
                content["reveal"].append("lean-yes")
            elif decision <= -.15:
                content["reveal"].append("strong-no")
            elif decision < 0:
                content["reveal"].append("lean-no")

            return JsonResponse(content)
        else:
            return HttpResponse("sorry, the form isn't valid")

