from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from ballot_decider.models import BallotDeciderProject, BallotDeciderItem, PointOfView
from .forms import CreateProjectForm, ParticipateForm
import os
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
            project = BallotDeciderProject()
            project.name = form.cleaned_data["measure_name"]
            project.owner_profile = profile
            project.ballot_text = form.cleaned_data["ballot_text"]
            project.election_date = form.cleaned_data["election_date"]
            project.election_website = form.cleaned_data["election_website"]
            project.save()

            for i in range(1,4):
                data = form.cleaned_data.get("participation_item_number_"+str(i), None)
                if not data is None and not data=="":
                    item = cm.ParticipationItem.objects.get(id=data, is_active=True)
                    project.basics.add(item)

            for i in range(1,4):
                quote = form.cleaned_data.get("pov_quote_"+str(i), None)
                if not quote is None and not quote=="":
                    pov = PointOfView()
                    pov.quote = quote
                    pov.citation_url = form.cleaned_data["pov_citation_url_"+str(i)]
                    pov.favorability = form.cleaned_data["pov_favorability_"+str(i)]
                    pov.save()
                    project.points_of_view.add(pov)

            t1 = cf.get_best_final_matching_tag(form.cleaned_data["tag1"])
            if not t1 is None:
                project.tags.add(t1)
            t2 = cf.get_best_final_matching_tag(form.cleaned_data["tag2"])
            if not t2 is None:
                project.tags.add(t2)
            t3 = cf.get_best_final_matching_tag(form.cleaned_data["tag3"])
            if not t3 is None:
                project.tags.add(t3)
            
            return render(request, 'core/thanks.html', {"action_description": "creating a new ballot decider project", "link": "/apps/ballot_decider/administer_project/"+str(project.id)})
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path})
    else:
        form = CreateProjectForm()
        return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path })

def administer_project(request, project_id):
    project = get_object_or_404(BallotDeciderProject, pk=project_id) 
    items = BallotDeciderItem.objects.filter(participation_project=project)
    return render(request, 'core/project_admin_base.html', {"items": [cv.get_item_details(i, True) for i in items if i.is_active], "project": project})

def participate(request, item_id):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)
    item = BallotDeciderItem.objects.get(pk=item_id)
    context = cv.get_default_og_metadata(request, item)
    project = item.participation_project.ballotdeciderproject
    context.update({"ballot": project, "items": [cv.get_item_details(i, False) for i in project.basics.all() if i.is_active]})
    if not request.method == "POST":
        return render(request, 'ballot_decider/participate.html', context)
    if request.method == 'POST' and request.is_ajax():
        submission_data = json.loads(request.body.strip())        
        form = ParticipateForm(item, data)


