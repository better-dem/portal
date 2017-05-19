from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from reading_assignment.models import ReadingAssignmentProject, ReadingAssignmentItem, Submission
from .forms import CreateProjectForm, SubmitAssignmentForm
from django.db.models import Count
import os
import sys
import core.models as cm
import core.views as cv
import core.tasks as ct
from django.contrib.gis.geos import GEOSGeometry, Polygon, LinearRing

def new_project(request):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)

    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            project = ReadingAssignmentProject()
            num = 0
            for k in form.cleaned_data.keys():
                if k.startswith("text_question_"):
                    num += 1
                    q = TextQuestion()
                    q.question_text = form.cleaned_data[k]
                    q.save()
                    oai = OrderedAssignmentItem()
                    oai.number = num
                    oai.text_question = q
                    oai.assignment=project
                    oai.save()
                elif k.startswith("participation_item_"):
                    num += 1
                    oai = OrderedAssignmentItem()
                    oai.number = num
                    oai.text_question = q
                    oai.participation_item = cm.ParticipationItem.get(id=form.cleaned_data[k], is_active=True)
                    oai.assignment=project
                    oai.save()
            
            project.owner_profile = profile
            project.name = form.cleaned_data["assignment_name"]
            project.save()

            ct.finalize_project(project)
            
            return render(request, 'core/thanks.html', {"action_description": "creating a new reading assignment", "link": "/apps/reading_assignment/administer_project/"+str(project.id)})
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path})
    else:
        form = CreateProjectForm()
        return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path })

def administer_project(request, project_id):
    project = get_object_or_404(ReadingAssignmentProject, pk=project_id)
    items = ReadingAssignmentItem.objects.filter(participation_project=project,  is_active=True).distinct()
    item_details = []

    for item in items:
        current_item_detail = cv.get_item_details(item, True)
        responses = ItemResponse.objects.filter(participation_item=item)
        num_responses = responses.count()
        current_item_detail["question_summaries"] = question_summaries
        current_item_detail["num_responses"] = num_responses
        item_details.append(current_item_detail)

    return render(request, 'reading_assignment/project_results.html', {"items": item_details, "project":project, 'site': os.environ["SITE"]})


def participate(request, item_id):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)

    item = ReadingAssignmentItem.objects.get(pk=item_id)
    context = cv.get_default_og_metadata(request, item)
    project = item.participation_project.landuseproject
    title = project.name

    if request.method == 'POST':
        form = SubmitAssignmentForm(project, request.POST )        
        if form.is_valid():
            item_response = ItemResponse()
            item_response.user_profile = profile
            item_response.participation_item = item
            item_response.save()
            
            # TODO: instead, use ReadingAssignmentProject.get_questions()
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
                        
            context.update({"action_description": "submitting this reading assignment", "item": item})
            return render(request, 'core/thanks_participate.html', context)
        else:
            context.update({'form': form, 'action_path' : request.path, 'title' : title, 'item':item})
            return render(request, 'core/generic_form_participate.html', context)
    else:
        form = SubmitAssignmentForm(project)
        context.update({'form': form, 'action_path' : request.path, 'title' : title, 'item': item})
        return render(request, 'core/generic_form_participate.html', context)



