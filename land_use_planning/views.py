from django.shortcuts import render
from django.http import HttpResponse
from land_use_planning.models import LandUseProject, FeedbackGoal, ItemResponse, Question, QuestionResponse, TMCQResponse
from .forms import CreateProjectForm, ItemResponseForm
from django.db.models import Count

import os

def index(request):
    num_projects = LandUseProject.objects.all().count()
    num_responses = ItemResponse.objects.all().count()
    return render(request, 'land_use_planning/index.html', {'num_projects': num_projects, 'num_responses': num_responses})

def new_project(request):
    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            project = LandUseProject()
            project.name = form.cleaned_data["project_name"]
            project.polygon_coords = form.cleaned_data["polygon_field"]
            project.save()

            goals = FeedbackGoal.objects.all()
            for goal in goals:
                var_name = goal.name + "_pref"
                if form.cleaned_data[var_name]:
                    project.feedback_goals.add(goal)
            
            return render(request, 'land_use_planning/thanks.html', {"action_description": "creating a new project", "item_link": "/show_project/"+str(project.id)})
        else:
            return render(request, 'land_use_planning/generic_form.html', {'form': form, 'action_path' : request.path})
    else:
        form = CreateProjectForm()
        return render(request, 'land_use_planning/generic_form.html', {'form': form, 'action_path' : request.path })

def project_response(request, project_id):
    project = LandUseProject.objects.get(pk=project_id)
    title = project.name

    if request.method == 'POST':
        form = ItemResponseForm(project, request.POST )        
        if form.is_valid():
            pr = ItemResponse()
            pr.project = project
            pr.save()
            
            # TODO: instead, use LandUseProject.get_questions()
            for key in form.cleaned_data:
                if "field_prf_" in key:
                    question_id = key.lstrip("field_prf_")
                    question = Question.objects.get(pk=question_id)
                    try:
                        tmcq = question.tmcq
                    except:
                        raise Exception("Invalid question type. Only TMCQ supported")
                    else:
                        qr = TMCQResponse()
                        qr.project_response = pr
                        qr.question = question
                        qr.option_index = int(form.cleaned_data[key])
                        qr.save()
                        
            return render(request, 'land_use_planning/thanks.html', {"action_description": "responding to "+title})
        else:
            return render(request, 'land_use_planning/generic_form.html', {'form': form, 'action_path' : request.path, 'title' : title})
    else:
        form = ItemResponseForm(project)
        return render(request, 'land_use_planning/generic_form.html', {'form': form, 'action_path' : request.path, 'title' : title})


def show_projects(request):
    projects = LandUseProject.objects.all()
    ids = [str(p.id) for p in projects]
    return HttpResponse(','.join(ids))

def show_project(request, project_id):
    project = LandUseProject.objects.get(pk=project_id)
    questions = project.get_questions()
    title = project.name
    
    responses = ItemResponse.objects.filter(project=project)
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
            response_counts = TMCQResponse.objects.filter(project_response__project=project).filter(question=q).values('option_index').annotate(count=Count("id"))
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
    return render(request, 'land_use_planning/project_results.html', {'title' : title, "num_responses": num_responses, "question_summaries": question_summaries})

