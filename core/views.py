from django.shortcuts import render
from django.http import HttpResponse
import core.models as cm
from cm import UserProfile, FeedMatch
import sys

def show_profile(request):
    user = request.user
    profile = user.userprofile

    sys.stdout.write(dir(user))

    apps = []
    for app in cm.registered_apps:
        if app.provider_permission in user.user_permission:
            
            

    return render(request, 'core/profile.html', {'apps':apps})
    
    return HttpResponse("user email: "+str(user.email))

def feed(request):
    user = request.user
    profile = user.userprofile
    
    recent_matches = FeedMatch.objects.filter(user_profile=profile).order_by('-creation_time')[:10]

    items = [{"label": m.participation_item.name, "description": m.participation_item.get_inherited_instance().get_description()} for m in recent_matches]
    return render(request, 'core/feed.html', {'items':items})


    
