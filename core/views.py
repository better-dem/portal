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

    items = [{"label": m.participation_item.name, "description": m.participation_item.get_inherited_instance().get_description()} for m in recent_matches]
    return render(request, 'core/feed.html', {'items':items})
