from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from city_budgeting.models import CityBudgetingProject, QuizResponse, Question, QuestionResponse, TMCQResponse, CityBudgetQuiz, Service
from .forms import CreateProjectForm, QuizResponseForm
from django.db.models import Count
import os
import sys
import core.views as cv
import core.forms as cf
import core.models as cm
import core.tasks as ct

def new_project(request):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)

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
            project.owner_profile = profile
            project.save()

            for st in Service.SERVICE_TYPES:
                s = Service()
                s.city_budget = project
                s.service_type = st[0]
                s.source = form.cleaned_data[st[0]+"_source"]
                if st[0]+"_expenditure" in form.cleaned_data:
                    s.expected_expenditure = form.cleaned_data[st[0]+"_expenditure"]
                s.save()

            ct.finalize_project(project)
            
            return render(request, 'core/thanks.html', {"action_description": "creating a new city budget project", "link": "/apps/land_use_planning/administer_project/"+str(project.id)})
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path})
    else:
        form = CreateProjectForm()
        return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path })


def administer_project(request, project_id):
    project = get_object_or_404(CityBudgetingProject, pk=project_id)
    items = CityBudgetQuiz.objects.filter(participation_project=project,  is_active=True).distinct()

    item_details = []

    for item in items:
        questions = Question.objects.filter(item=item).distinct()

        current_item_detail = cv.get_item_details(item, True)

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

    return render(request, 'city_budgeting/project_results.html', {"items": item_details, "project":project})


def participate(request, item_id):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)

    item = get_object_or_404(CityBudgetQuiz, pk=item_id)
    context = cv.get_default_og_metadata(request, item)
    # project = item.participation_project.landuseproject
    title = item.name

    if request.method == 'POST':
        form = QuizResponseForm(item, request.POST )        
        if form.is_valid():
            item_response = QuizResponse()
            item_response.user_profile = profile
            item_response.participation_item = item
            item_response.save()
            
            question_summaries = []
            
            # TODO: instead, use CityBudgetingProject.get_questions()
            for key in form.cleaned_data:
                if "field_prf_" in key:
                    question_id = key.lstrip("field_prf_")
                    question = get_object_or_404(Question, pk=question_id)
                    question_summary=dict()
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

                        question_summary["label"] = tmcq.question_text
                        question_summary["correct"] = tmcq.correct_answer_index == qr.option_index
                        answers = []
                        for i in range(1,6):
                            a = dict()
                            a["correct_answer"] = tmcq.correct_answer_index == i
                            a["user_answer"] = qr.option_index == i
                            a["option_text"] = tmcq.__dict__["option"+str(i)]
                            answers.append(a)
                        question_summary["answers"] = answers

                    question_summaries.append(question_summary)

            s = score_quiz_response(item_response)
            all_scores = sorted([score_quiz_response(i) for i in QuizResponse.objects.filter(participation_item=item)], reverse=True)
            rank = all_scores.index(s)+1
            rank_str = "Your rank: {} out of {} total participants".format(rank, len(all_scores))
            score = str(round(100*s))+"%"
            context.update({"action_description": "taking "+title, "score": score, "rank": rank_str, "question_summaries": question_summaries})
            return render(request, 'city_budgeting/thanks.html', context)
        else:
            context.update({'form': form, 'action_path' : request.path, 'title' : title})
            return render(request, 'core/generic_form.html', context)
    else:
        form = QuizResponseForm(item)
        context.update({'form': form, 'action_path' : request.path, 'title' : title})
        return render(request, 'core/generic_form.html', context)



def score_quiz_response(response):
    """
    Give a score, 0-1
    response is a models.QuizResponse object
    """
    question_responses = QuestionResponse.objects.filter(item_response=response)
    num_questions = question_responses.count()
    num_correct = 0
    for r in question_responses:
        try:
            tmcqr = r.tmcqresponse
        except:
            raise Exception("Invalid question type. Only TMCQ supported")
        else:
            if tmcqr.option_index == r.question.tmcq.correct_answer_index:
                num_correct += 1
    if num_questions == 0:
        return 0
    return 1.0*num_correct/num_questions
    
