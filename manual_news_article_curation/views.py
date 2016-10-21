from django.shortcuts import render, redirect
from django.http import HttpResponse
from manual_news_article_curation.forms import CreateArticleForm
from manual_news_article_curation.models import ManualNewsCurationProject, NewsArticleItem
from core.views import get_item_details
from core import models as cm

def new_project(request):
    u = request.user
    p = u.userprofile

    if request.method == 'POST':
        form = CreateArticleForm(request.POST)
        if form.is_valid():
            
            project = form.save(commit=False)
            project.owner_profile = p
            project.save()
            
            return render(request, 'core/thanks.html', {"action_description": "creating a new news article project", "link": "/apps/"+app.app_name+"/administer_project/"+str(project.id)+"/-1"})
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path})
    else:
        form = CreateArticleForm()
        return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path })


def administer_project(request, project_id):
    project = ManualNewsCurationProject.objects.get(pk=project_id)
    items = NewsArticleItem.objects.filter(participation_project=project)
    return render(request, 'core/generic_project_stats.html', {"items": [get_item_details(i, True) for i in items]})


def participate(request, item_id):
    item = NewsArticleItem.objects.get(pk=item_id)
    return redirect(item.url)

