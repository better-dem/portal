from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from single_quiz.models import SingleQuizProject, SingleQuizItem
from .forms import CreateProjectForm, ParticipateForm
import os
import sys
import core.models as cm
import core.views as cv
import core.forms as cf
import core.tasks as ct
import json

def new_project(request):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)

    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            project = SingleQuizProject()
            project.name = form.cleaned_data["question_text"]
            project.question_text = form.cleaned_data["question_text"]

            project.option1=form.cleaned_data["option1"]
            project.option2=form.cleaned_data["option2"]
            if "option3" in form.cleaned_data:
                project.option3=form.cleaned_data["option3"]
            if "option4" in form.cleaned_data:
                project.option4=form.cleaned_data["option4"]
            if "option5" in form.cleaned_data:
                project.option5=form.cleaned_data["option5"]

            project.correct_answer_index = form.cleaned_data["correct_answer_index"]
            project.citation_url = form.cleaned_data["citation_url"]
            project.explanation = form.cleaned_data["explanation"]
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
            return render(request, 'core/thanks.html', {"action_description": "creating a new single quiz", "link": "/apps/single_quiz/administer_project/"+str(project.id)})
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path})
    else:
        form = CreateProjectForm()
        return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path })

def administer_project(request, project_id):
    project = get_object_or_404(SingleQuizProject, pk=project_id) 
    items = SingleQuizItem.objects.filter(participation_project=project)
    return render(request, 'core/project_admin_base.html', {"items": [cv.get_item_details(i, True) for i in items if i.is_active], "project": project})

def participate(request, item_id):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)

    item = SingleQuizItem.objects.get(pk=item_id)
    context = cv.get_default_og_metadata(request, item)
    project = item.participation_project.singlequizproject

    if request.method == 'POST':
        form = None

        # populate the form differently depending on whether data is from ajax
        if request.is_ajax():
            submission = request.body.strip()
            submission = json.loads(submission)
            assert(len(submission) == 1)
            data = {"choice":submission.values()[0]}
            form = ParticipateForm(item, data)
        else:
            form = ParticipateForm(item, request.POST)

        # respond differently
        if form.is_valid():
            if form.cleaned_data["choice"] == str(project.correct_answer_index):
                content = {"reveal": ["correct", "sources"], "hide": ["incorrect", "single_quiz_ajax_form"], "response": "Correct!", "explanation": project.explanation}
                if request.is_ajax():
                    return JsonResponse(content)
                else:
                    content.update({'action_description': "responding to this mini-quiz", "ans_correct": True, "source": project.citation_url})
                    return render(request, 'single_quiz/thanks.html', content)
            else:
                content = {"reveal": ["incorrect", "sources"], "hide": ["correct", "single_quiz_ajax_form"], "response": "Sorry, the correct answer was: "+project.__dict__["option"+str(project.correct_answer_index)], "explanation": project.explanation}
                if request.is_ajax():
                    return JsonResponse(content)
                else:
                    content.update({'action_description': "responding to this mini-quiz", "ans_correct": False, "source": project.citation_url})
                    return render(request, 'single_quiz/thanks.html', content)
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path': request.path, "form_title": project.question_text})
    else:
        form = ParticipateForm(item)
        return render(request, 'core/generic_form.html', {'form': form, 'action_path': request.path, "form_title": project.question_text})
