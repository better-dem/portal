from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from reading_assignment.models import ReadingAssignmentProject, OrderedAssignmentItem, ReadingAssignmentItem, TextQuestion, TextQuestionResponse, Submission
from .forms import SubmitAssignmentForm, CreateProjectForm, AssignmentItemForm
from django import forms
from django.db.models import Count
import os
import sys
import core.models as cm
import core.views as cv
import core.tasks as ct
from django.contrib.gis.geos import GEOSGeometry, Polygon, LinearRing
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def new_project(request, group=None):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)
    AssignmentItemsFormset = forms.formset_factory(AssignmentItemForm, can_delete=True)
    if request.method == 'POST':
        formset = AssignmentItemsFormset(request.POST, form_kwargs={'userprofile':profile})
        project_form = CreateProjectForm(request.POST)
        if formset.is_valid() and project_form.is_valid():
            sys.stderr.write("formset data:\n{}\n".format(formset.cleaned_data))
            sys.stderr.flush()
            project = ReadingAssignmentProject()
            project.owner_profile = profile
            project.name = project_form.cleaned_data["assignment_name"]
            project.group = group
            project.save()
            num = 0
            for item in formset.cleaned_data:
                if item.get("text_question", u'') != u'':                    
                    num += 1
                    q = TextQuestion()
                    q.question_text = item["text_question"]
                    q.save()
                    oai = OrderedAssignmentItem()
                    oai.number = num
                    oai.text_question = q
                    oai.assignment=project
                    oai.save()
                elif not item.get("participation_item", None) is None:
                    num += 1
                    oai = OrderedAssignmentItem()
                    oai.number = num
                    oai.participation_item = cm.ParticipationItem.objects.get(id=item["participation_item"], is_active=True)
                    oai.assignment=project
                    oai.save()
                else:
                    # this item is blank, ignore it
                    pass                

            ct.finalize_project(project)
            return render(request, 'core/thanks.html', {"action_description": "creating a new reading assignment", "link": "/apps/reading_assignment/administer_project/"+str(project.id)})

        else:
            sys.stderr.write("formset errors:\n{}\n".format(formset.errors))
            sys.stderr.write("project form errors:\n{}\n".format(project_form.errors))
            sys.stderr.flush()
            raise Exception()
    else:
        project_form = CreateProjectForm()
        formset = AssignmentItemsFormset(form_kwargs={'userprofile':profile})
        return render(request, 'reading_assignment/new_project.html', {'project_form': project_form, 'items_formset': formset})

def administer_project(request, project_id):
    project = get_object_or_404(ReadingAssignmentProject, pk=project_id)
    items = ReadingAssignmentItem.objects.filter(participation_project=project, is_active=True).distinct()
    item_details = []

    for item in items:
        current_item_detail = cv.get_item_details(item, True)
        submissions = Submission.objects.filter(participation_item=item)
        num_submissions = submissions.count()
        current_item_detail["num_submissions"] = num_submissions
        submission_details = []
        for s in submissions:
            user_id = s.user_profile.user.email
            if project.group:
                try:
                    user_id = cm.GroupMembership.objects.get(group=project.group, member=s.user_profile).member_name
                except ObjectDoesNotExist:
                    pass
                except MultipleObjectsReturned:
                    user_id = "{}: WARNING: this user is registered multiple times for this {}".format(user_id, project.group.group_type)

            submission_detail = {"user_id": user_id, "responses": []}
            for tqr in s.textquestionresponse_set.all():
                qr_detail = {"question": tqr.question.question_text, "response":tqr.response}
                submission_detail["responses"].append(qr_detail)
            submission_details.append(submission_detail)
        current_item_detail["submission_details"] = submission_details
        item_details.append(current_item_detail)

    return render(request, 'reading_assignment/project_results.html', {"items": item_details, "project":project, 'site': os.environ["SITE"]})


def participate(request, item_id):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)

    item = ReadingAssignmentItem.objects.get(pk=item_id)
    context = cv.get_default_og_metadata(request, item)
    project = item.participation_project.readingassignmentproject
    title = project.name

    if request.method == 'POST':
        form = SubmitAssignmentForm(project, request.POST )        
        if form.is_valid():
            sub = Submission()
            sub.user_profile = profile
            sub.participation_item = item
            sub.save()

            for k in form.cleaned_data.keys():
                if k.startswith("text_question_"):
                    qid = int(k[14:])
                    question = TextQuestion.objects.get(id=qid)
                    item_response = TextQuestionResponse(question=question, response=form.cleaned_data[k], submission=sub)
                    item_response.save()
            
            # save responses to questions
            context.update({"action_description": "submitting this reading assignment", "item": item})
            return render(request, 'core/thanks_participate.html', context)
        else:
            context.update({'form': form, 'action_path' : request.path, 'title' : title, 'item':item})
            return render(request, 'reading_assignment/participate.html', context)
    else:
        form = SubmitAssignmentForm(project)
        context.update({'form': form, 'action_path' : request.path, 'title' : title, 'item': item})
        return render(request, 'reading_assignment/participate.html', context)



