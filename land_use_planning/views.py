from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from land_use_planning.models import LandUseProject, FeedbackGoal, ItemResponse, Question, QuestionResponse, TMCQResponse, LandUseParticipationItem
from .forms import CreateProjectForm, ItemResponseForm
from django.db.models import Count
import os
import sys
import core.models as cm
import core.views as cv
from django.contrib.gis.geos import GEOSGeometry, Polygon, LinearRing

def new_project(request):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)

    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            project = LandUseProject()
            project.name = form.cleaned_data["project_name"]
            # !!! Warning, Google lists geo data lat,lon.
            # everyone else, including better dem portal, does lon, lat
            poly_data = [(x[1], x[0]) for x in form.cleaned_data["polygon_field"]]
            poly_data.append(poly_data[0]) # polygon must be instantiated with a closed ring
            project.polygon = Polygon(LinearRing(tuple(poly_data)))
            project.owner_profile = profile
            project.save()

            goals = FeedbackGoal.objects.all()
            for goal in goals:
                var_name = goal.name + "_pref"
                if form.cleaned_data[var_name]:
                    project.feedback_goals.add(goal)
            
            return render(request, 'core/thanks.html', {"action_description": "creating a new land use planning project", "link": "/apps/land_use_planning/administer_project/"+str(project.id)})
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path})
    else:
        form = CreateProjectForm()
        return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path })

def administer_project(request, project_id):
    project = get_object_or_404(LandUseProject, pk=project_id)
    questions = project.get_questions()
    items = LandUseParticipationItem.objects.filter(participation_project=project,  is_active=True).distinct()

    item_details = []

    for item in items:
        current_item_detail = cv.get_item_details(item, True)

        responses = ItemResponse.objects.filter(participation_item=item)
        num_responses = responses.count()

        question_summaries = []
        for q in questions:
            summary = dict()
            summary["label"] = q.question_text
            try:
                tmcq = q.tmcq                
            except:
                raise Exception("Invalid question type. Only TMCQ supported")
            else:
                response_counts = TMCQResponse.objects.filter(item_response__participation_item=item).filter(question=q).values('option_index').annotate(count=Count("id"))
                rc_option_indices = [x["option_index"] for x in response_counts]
                answers = []
                for i in range(1,6):
                    question = None
                    if i == 1:
                        question = tmcq.option1
                    elif i == 2:
                        question = tmcq.option2
                    elif i == 3:
                        question = tmcq.option3
                    elif i == 4:
                        question = tmcq.option4
                    elif i == 5:
                        question = tmcq.option5

                    rc = [x for x in response_counts if x["option_index"] == i]
                    if len(rc) == 1:
                        answers.append([question, rc[0]["count"]])
                    else:
                        answers.append([question, 0])
                summary["answers"] = answers
            question_summaries.append(summary)

        current_item_detail["question_summaries"] = question_summaries
        current_item_detail["num_responses"] = num_responses
        item_details.append(current_item_detail)

    return render(request, 'land_use_planning/project_results.html', {"items": item_details, "project":project})


def participate(request, item_id):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)

    item = LandUseParticipationItem.objects.get(pk=item_id)
    context = cv.get_default_og_metadata(request, item)
    project = item.participation_project.landuseproject
    title = project.name

    if request.method == 'POST':
        form = ItemResponseForm(project, request.POST )        
        if form.is_valid():
            item_response = ItemResponse()
            item_response.user_profile = profile
            item_response.participation_item = item
            item_response.save()
            
            # TODO: instead, use LandUseProject.get_questions()
            for key in form.cleaned_data:
                if "field_prf_" in key:
                    question_id = key.lstrip("field_prf_")
                    question = get_object_or_404(Question, pk=question_id)
                    try:
                        tmcq = question.tmcq
                    except:
                        raise Exception("Invalid question type. Only TMCQ supported")
                    else:
                        qr = TMCQResponse()
                        qr.item_response = item_response
                        qr.question = question
                        qr.option_index = int(form.cleaned_data[key])
                        qr.save()
                        
            context.update({"action_description": "responding to the land use planning project: "+title})
            return render(request, 'core/thanks.html', context)
        else:
            context.update({'form': form, 'action_path' : request.path, 'title' : title})
            return render(request, 'core/generic_form.html', context)
    else:
        form = ItemResponseForm(project)
        context.update({'form': form, 'action_path' : request.path, 'title' : title})
        return render(request, 'core/generic_form.html', context)



