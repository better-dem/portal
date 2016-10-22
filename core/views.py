from django.contrib.auth.models import Permission, AnonymousUser
from django.shortcuts import render
from django.http import HttpResponse
import core.models as cm
import sys
import pkgutil

from django.contrib.contenttypes.models import ContentType

def show_profile(request):
    cts = ContentType.objects.all()

    user = request.user
    profile = user.userprofile

    profile_apps = []
    for app in cm.get_registered_participation_apps():
        profile_app = dict()
        profile_app["label"] = app.label
        profile_app["existing_projects"] = []

        perm = cm.get_provider_permission(app)
        sys.stderr.write(str(user.username)+"\n")
        sys.stderr.flush()
        sys.stderr.write(str(user.get_all_permissions())+"\n")        
        sys.stderr.flush()
        sys.stderr.write(str(user.has_perm(perm))+"\n")        
        sys.stderr.flush()
        sys.stderr.write(str(perm.codename)+"\n")        
        sys.stderr.flush()
        
        if not app.label+"."+perm.codename in user.get_all_permissions():
            profile_app["label"] = profile_app["label"] + " -- No Permissions"
        else:
            profile_app["label"] = profile_app["label"]
            profile_app["new_project_link"] = "/apps/"+app.label+"/new_project/-1/-1"
            existing_projects = cm.get_app_project_models(app)[0].objects.filter(owner_profile=profile)
            for ep in existing_projects:
                proj = dict()
                proj["name"] = ep.name
                proj["administer_project_link"] = "/apps/"+app.label+"/administer_project/"+str(ep.id)+"/-1"
                profile_app["existing_projects"].append(proj)
                
        profile_apps.append(profile_app)

    return render(request, 'core/profile.html', {'profile_apps': profile_apps})

def app_view_relay(request, app_name, action_name, project_id, item_id):
    if not app_name in [app.label for app in cm.get_registered_participation_apps()]:
        raise Exception("app not registered or does not exist:" + str(app_name))
    else:
        app = [a for a in cm.get_registered_participation_apps() if a.name == app_name][0]
        if action_name == "new_project":
            return app.views_module.new_project(request) 
        elif action_name == "administer_project":
            return app.views_module.administer_project(request, project_id) 
        elif action_name == "participate":
            return app.views_module.participate(request, item_id) 
        else:
            raise Exception("invalid action:" + str(action_name))

def feed(request):
    items = None
    user = request.user
    if isinstance(user, AnonymousUser):
        items = []
    else:
        profile = user.userprofile
        recent_matches = cm.FeedMatch.objects.filter(user_profile=profile).order_by('-creation_time')[:100]
        sys.stdout.write("num matches:" + str(len(recent_matches)) + "\n")
        sys.stdout.flush()
        items = [get_item_details(i) for i in map(lambda x: x.participation_item, recent_matches)]

    return render(request, 'core/feed.html', {'items':items})

def get_item_details(item, count_matches=False):
    ans = {"label": item.name, "description": item.get_inherited_instance().get_description()}
    if count_matches:
        ans["num_matches"] = cm.FeedMatch.objects.filter(participation_item=item).count()
    return ans
