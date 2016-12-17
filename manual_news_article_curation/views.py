from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from manual_news_article_curation.forms import CreateArticleForm
from manual_news_article_curation.models import ManualNewsCurationProject, NewsArticleItem
import core.views as cv
import core.models as cm

def new_project(request):
    (profile, permissions, is_default) = cv.get_profile_and_permissions(request)

    if request.method == 'POST':
        form = CreateArticleForm(request.POST)
        if form.is_valid():
            
            project = form.save(commit=False)
            project.owner_profile = profile
            project.save()
            
            return render(request, 'core/thanks.html', {"action_description": "creating a new news article project", "link": "/apps/manual_news_article_curation/administer_project/"+str(project.id)+"/-1"})
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path})
    else:
        form = CreateArticleForm()
        return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path })


def administer_project(request, project_id):
    project = get_object_or_404(ManualNewsCurationProject, pk=project_id)
    items = NewsArticleItem.objects.filter(participation_project=project)
    return render(request, 'core/generic_project_stats.html', {"items": [cv.get_item_details(i, True) for i in items]})


def participate(request, item_id):
    item = get_object_or_404(NewsArticleItem, pk=item_id)
    project = item.participation_project.manualnewscurationproject
    return redirect(project.url)

