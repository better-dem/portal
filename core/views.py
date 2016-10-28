from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, AnonymousUser
from django.db.models import F
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
import core.models as cm
import core.tasks as tasks
from core.forms import UploadGeoTagset
import sys
from django.core.files.storage import default_storage

def tags(request):
    tasks.marco.delay()
    all_tags = cm.Tag.objects.all()
    first_ten = all_tags[:10]
    return HttpResponse("Number of tags: "+str(all_tags.distinct().count())+"\n"+"\n".join([i.get_name() for i in first_ten]))

def test_geo(request):
    from django.contrib.gis import gdal
    return HttpResponse(str(gdal.HAS_GDAL))

def upload_geo_tagset(request):
    user = request.user
    profile = user.userprofile

    app = cm.get_core_app()
    perm = cm.get_provider_permission(app)
    if not app.label+"."+perm.codename in user.get_all_permissions():
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = UploadGeoTagset(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data["format_id"] == "uscitieslist_csv_v0":
                tasks.insert_csv1.delay(form.cleaned_data["small_test"])
                return HttpResponse("Ok, I'm processing this csv file. Thanks")
            else:
                return HttpResponse("Sorry, this format is not known")
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path, "enctype_data": True})
    else:
        form = UploadGeoTagset()
        return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path, "enctype_data": True})
    

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
    user = request.user
    profile = user.userprofile
    if not app_name in [app.label for app in cm.get_registered_participation_apps()]:
        raise Exception("app not registered or does not exist:" + str(app_name))
    else:
        app = [a for a in cm.get_registered_participation_apps() if a.name == app_name][0]
        perm = cm.get_provider_permission(app)
        has_perm = app.label+"."+perm.codename in user.get_all_permissions()
        
        if action_name == "new_project":
            if has_perm:
                return app.views_module.new_project(request) 
            else:
                return render(request, 'core/no_permissions.html', {"title": "No Permission", "app_name": app_name, "action_description": "create a new project"})
        elif action_name == "administer_project":
            if has_perm:
                return app.views_module.administer_project(request, project_id)
            else:
                return render(request, 'core/no_permissions.html', {"title": "No Permission", "app_name": app_name, "action_description": "administer a project"})
        elif action_name == "participate":
            cm.ParticipationItem.objects.filter(pk=item_id).distinct().update(visits=F('visits')+1)
            cm.FeedMatch.objects.filter(user_profile=profile, participation_item__pk=item_id).update(has_been_visited=True)
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
        items = [get_item_details(i) for i in map(lambda x: x.participation_item, recent_matches)]

    return render(request, 'core/feed.html', {'items':items})

def get_item_details(item, get_activity=False):
    app = cm.get_app_for_model(item.get_inherited_instance().__class__)
    project_id = item.participation_project.pk
    ans = {"label": item.name, "description": item.get_inherited_instance().get_description(), "link": "/apps/"+app.label+"/participate/"+str(project_id)+"/"+str(item.pk)}
    if not item.display_image_url == "":
        ans["display_image_url"] = item.display_image_url
    if get_activity:
        ans["num_matches"] = cm.FeedMatch.objects.filter(participation_item=item).count()
        ans["num_visits"] = item.visits
    return ans

