from django.shortcuts import render
from django.http import HttpResponse
from city_budgeting.models import CityBudgetingProject, QuizResponse, Question, QuestionResponse, TMCQResponse, CityBudgetQuiz
from .forms import CreateProjectForm, QuizResponseForm
from django.db.models import Count
import os
import sys
from core.views import get_item_details
import core.forms as cf

def new_project(request):
    u = request.user
    p = u.userprofile

    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            project = CityBudgetingProject()
            project.city = cf.get_best_final_matching_tag(form.cleaned_data["place_name"]).geotag
            project.fiscal_year_end_date = form.cleaned_data["fiscal_year_end_date"]
            project.name = "City Budget Outreach Project for "+project.city.get_name()
            project.total_expected_revenue = form.cleaned_data["total_expected_revenue"]
            project.total_expected_expenditure = form.cleaned_data["total_expected_expenditure"]
            project.mayor_name = form.cleaned_data["mayor_name"]
            project.council_members = form.cleaned_data["council_members"]
            project.budget_url = form.cleaned_data["budget_url"]
            project.owner_profile = p
            project.save()
            
            return render(request, 'core/thanks.html', {"action_description": "creating a new city budget project", "link": "/apps/land_use_planning/administer_project/"+str(project.id)+"/-1"})
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path})
    else:
        form = CreateProjectForm()
        return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path })

def administer_project(request, project_id):
    project = CityBudgetingProject.objects.get(pk=project_id)
    items = CityBudgetQuiz.objects.filter(participation_project=project).distinct()

    item_details = []

    for item in items:
        questions = Question.objects.filter(item=item).distinct()

        current_item_detail = get_item_details(item, True)

        responses = QuizResponse.objects.filter(participation_item=item)
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
                # response_counts looks like: [{'option_index':1, 'count':13}, {...}, ...]
                response_counts = TMCQResponse.objects.filter(item_response__participation_item=item).filter(question=q).values('option_index').annotate(count=Count("id"))
                answers = []
                for i in range(1,6):
                    question = tmcq.__dict__["option{}".format(i)]

                    rc = [x for x in response_counts if x["option_index"] == i]
                    if len(rc) == 1:
                        answers.append([question, rc[0]["count"]])
                    else:
                        answers.append([question, 0])
                summary["answers"] = answers
                summary["correct_answer"] = tmcq.__dict__["option{}".format(tmcq.correct_answer_index)]
            question_summaries.append(summary)

        current_item_detail["question_summaries"] = question_summaries
        current_item_detail["num_responses"] = num_responses
        item_details.append(current_item_detail)

    return render(request, 'city_budgeting/project_results.html', {"items": item_details})


def participate(request, item_id):
    u = request.user
    p = u.userprofile

    item = CityBudgetQuiz.objects.get(pk=item_id)
    # project = item.participation_project.landuseproject
    title = item.name

    if request.method == 'POST':
        form = QuizResponseForm(item, request.POST )        
        if form.is_valid():
            item_response = QuizResponse()
            item_response.user_profile = p
            item_response.participation_item = item
            item_response.save()
            
            # TODO: instead, use CityBudgetingProject.get_questions()
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
                        qr.item_response = item_response
                        qr.question = question
                        qr.option_index = int(form.cleaned_data[key])
                        qr.save()
                        
            return render(request, 'core/thanks.html', {"action_description": "taking "+title})
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path, 'title' : title})
    else:
        form = QuizResponseForm(item)
        return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path, 'title' : title})



