from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, AnonymousUser
from django.db.models import F
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
import core.models as cm
import core.tasks as tasks
from core.forms import UploadGeoTagset, AddTagForm
import sys
from django.core.files.storage import default_storage

def tags(request):
    all_tags = cm.Tag.objects.all()
    first_ten = all_tags[:10]
    ans = ""
    ans += "Number of tags: "+str(all_tags.distinct().count())+"<br>"
    ans += "<br>".join([i.get_name() for i in first_ten])+"<br>"

    cities = cm.GeoTag.objects.filter(feature_type=cm.GeoTag.CITY)
    ans += "<br>"
    ans += "Number of cities:"+str(cities.count())+"<br>"
    ans += "<br>".join([i.get_name() for i in cities[:10]])+"<br>"

    states = cm.GeoTag.objects.filter(feature_type=cm.GeoTag.STATE_OR_PROVINCE)
    ans += "<br>"
    ans += "Number of states:"+str(states.count())+"<br>"
    ans += "<br>".join([i.get_name() for i in states[:10]])+"<br>"

    countries = cm.GeoTag.objects.filter(feature_type=cm.GeoTag.COUNTRY)
    ans += "<br>"
    ans += "Number of countries:"+str(countries.count())+"<br>"
    ans += "<br>".join([i.get_name() for i in countries[:10]])+"<br>"

    other = cm.GeoTag.objects.filter(feature_type=cm.GeoTag.OTHER)
    ans += "<br>"
    ans += "Number of other types of geo-tag:"+str(other.count())+"<br>"
    ans += "<br>".join([i.get_name() for i in other[:10]])+"<br>"

    unk = cm.GeoTag.objects.filter(feature_type=cm.GeoTag.UNKNOWN)
    ans += "<br>"
    ans += "Number of unknown geo-tags:"+str(unk.count())+"<br>"
    ans += "<br>".join([i.get_name() for i in unk[:10]])+"<br>"
    return HttpResponse(ans)

def test_geo(request):
    from django.contrib.gis import gdal
    return HttpResponse(str(gdal.HAS_GDAL))

def upload_dataset(request):
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
                tasks.insert_uscitieslist_v0.delay(form.cleaned_data["small_test"])
                return HttpResponse("Ok, I'm processing this csv file. Thanks")
            elif form.cleaned_data["format_id"] == "usa_and_states_v0":
                tasks.insert_usa_and_states.delay(form.cleaned_data["small_test"])
                return HttpResponse("Ok, I'm processing this csv file. Thanks")
            else:
                return HttpResponse("Sorry, this format is not known")
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path, "enctype_data": True})
    else:
        form = UploadGeoTagset()
        return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path, "enctype_data": True})
    

def show_profile(request):
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

def update_profile_tags(request):
    user = request.user
    profile = user.userprofile

    if request.method == 'POST':
        form = AddTagForm(request.POST)
        if form.is_valid():
            try:
                tag = cm.Tag.objects.get(name=form.cleaned_data["place_name"])
            except:
                return HttpResponse("Sorry, there isn't exactly one tag with this name")
            else:
                profile.tags.add(tag)
                tasks.feed_update_by_user_profile.delay(profile.id)
                return HttpResponse("Ok, I added "+tag.get_name()+" to your profile")
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path})
    else:
        form = AddTagForm()
        return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path})
    

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
        tasks.feed_update_by_user_profile.delay(profile.id)

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

