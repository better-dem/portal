from django.shortcuts import render
from django.http import HttpResponse
from manual_news_article_curation.forms import CreateArticleForm
from manual_news_article_curation.models import ManualNewsCurationProject, NewsArticleItem

def new_project(request):
    u = request.user
    p = u.userprofile

    if request.method == 'POST':
        form = CreateArticleForm(request.POST)
        if form.is_valid():
            
            project = form.save(commit=False)
            project.owner_profile = p
            project.save()
            
            return render(request, 'survey/thanks.html', {"action_description": "creating a new project", "item_link": "/show_project/"+str(project.id)})
        else:
            return render(request, 'survey/generic_form.html', {'form': form, 'action_path' : request.path})
    else:
        form = CreateArticleForm()
        return render(request, 'survey/generic_form.html', {'form': form, 'action_path' : request.path })


def administer_project(request, project_id):
    return HttpResponse(request, "manual news curation app's administer project view -- not yet implemented")

def participate(request, item_id):
    # log the click? use for improving recommendation

    # redirect 
    return HttpResponse(request, "manual news curation app's participate view"+str(item_id)+" -- not yet implemented")
