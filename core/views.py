from django.shortcuts import render
from django.http import HttpResponse
from core.models import UserProfile, FeedMatch

def show_profile(request):
    user = request.user
    profile = user.userprofile
    return HttpResponse("user email: "+str(user.email))

def feed(request):
    user = request.user
    profile = user.userprofile
    
    recent_matches = FeedMatch.objects.filter(user_profile=profile).order_by('-creation_time')[:10]

    matches = [{"label": m.name, "description": "description of" + str(m.name)} for m in recent_matches]
    return render(request, 'core/feed.html', {'matches':matches})
