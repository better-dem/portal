from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, AnonymousUser
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import F, Sum
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, FileResponse, HttpResponseForbidden, HttpResponseRedirect, HttpResponseServerError
from django.core.files.storage import default_storage
from django.db import transaction
from django.conf import settings

import core.models as cm
import core.tasks as tasks
from core.forms import CreateShortcutForm, DeleteProjectConfirmationForm, UploadDataset, AddTagForm, IssueReportForm, get_matching_tags, get_best_final_matching_tag, StripePaymentForm

import sys
import os
import random
import json

import stripe

stripe.api_key = os.environ["STRIPE_API_KEY"]

def get_default_og_metadata(request, participation_item=None):
    ans = {
        "og_type": "website",
        "og_title": "Better Democracy Portal",
        "og_description": "Aggregating and creating opportunities to participate with your government",
        # "og_url": "http://"+get_current_site(request).domain
    }
    if not participation_item is None:
        app = cm.get_app_for_model(participation_item.get_inherited_instance().__class__)
        # app = cm.get_app_for_model(participation_item.get_inherited_instance())
        # ans["og_url"] = "http://"+get_current_site(request).domain+"/apps/"+app.label+"/participate/"+str(participation_item.id)
        if not participation_item.display_image_file is None and not participation_item.display_image_file =="":
            ans["og_image"] = participation_item.display_image_file
    return ans

def get_profile_and_permissions(request):
    """
    returns (profile, permissions, is_default_user)
    assumes no permissions for default user
    """
    user = request.user
    if isinstance(user, AnonymousUser):
        user = cm.get_default_user()
        profile = user.userprofile
        perms = []
        return (profile, perms, True)
    profile = user.userprofile        
    perms = user.get_all_permissions()    
    return (profile, perms, False)

def test_geo(request):
    from django.contrib.gis import gdal
    return HttpResponse(str(gdal.HAS_GDAL))

def shortcut(request, shortcut_str):
    s = get_object_or_404(cm.Shortcut, shortcut_string=shortcut_str)
    item = s.target_item
    app = cm.get_app_for_model(item.get_inherited_instance().__class__)
    link = "/apps/"+app.label+"/participate/"+str(item.pk)
    return HttpResponseRedirect(link)

@transaction.atomic
def create_shortcut(request):
    (profile, permissions, is_default_user) = get_profile_and_permissions(request)
    if is_default_user:
        return render(request, "core/please_login.html")
    app = cm.get_core_app()
    perm = cm.get_provider_permission(app)
    if not app.label+"."+perm.codename in permissions:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = CreateShortcutForm(request.POST)
        if form.is_valid():
            # delete any existing shortcuts with the same string
            num_deleted = cm.Shortcut.objects.filter(shortcut_string=form.cleaned_data["shortcut_string"]).delete()
            deleted_string = "this many existing shortcuts were deleted: "+str(num_deleted)
            # create new shortcut
            s = cm.Shortcut()
            item = get_object_or_404(cm.ParticipationItem, id=form.cleaned_data["item_id"], is_active=True)
            s.shortcut_string = form.cleaned_data["shortcut_string"]
            s.target_item = item
            s.save()
            return render(request, "core/thanks.html", {"action_description": "creating this shortcut. "+deleted_string})
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path, "enctype_data": True})
    else:
        form = CreateShortcutForm()
        return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path, "enctype_data": True})


def upload_dataset(request):
    (profile, permissions, is_default_user) = get_profile_and_permissions(request)
    if is_default_user:
        return render(request, "core/please_login.html")
    app = cm.get_core_app()
    perm = cm.get_provider_permission(app)
    if not app.label+"."+perm.codename in permissions:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = UploadDataset(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data["format_id"] == "uscitieslist_csv_v0":
                tasks.insert_uscitieslist_v0.delay(form.cleaned_data["small_test"])
                return render(request, "core/thanks.html", {"action_description": "uploading this data file"})
            elif form.cleaned_data["format_id"] == "states_v1":
                tasks.insert_states.delay(form.cleaned_data["small_test"])
                return render(request, "core/thanks.html", {"action_description": "uploading this data file"})
            elif form.cleaned_data["format_id"] == "openstates_subjects_v1":
                tasks.insert_openstates_subjects.delay(form.cleaned_data["small_test"])
                return render(request, "core/thanks.html", {"action_description": "uploading this data file"})
            else:
                return HttpResponse("Sorry, this format is not known")
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path, "enctype_data": True})
    else:
        form = UploadDataset()
        return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path, "enctype_data": True})
    

@ensure_csrf_cookie
def show_profile(request):
    (profile, permissions, is_default_user) = get_profile_and_permissions(request)
    if is_default_user:
        return render(request, "core/please_login.html")
    tags = [t.name for t in profile.tags.all()[:100]]

    profile_apps = []
    for app in cm.get_registered_participation_apps():
        perm = cm.get_provider_permission(app)
        if app.label+"."+perm.codename in permissions:
            profile_app = dict()
            profile_app["label"] = app.label.replace("_", " ").title()
            profile_app["existing_projects"] = []
            profile_app["label"] = profile_app["label"]
            profile_app["new_project_link"] = "/apps/"+app.label+"/new_project/-1"
            existing_projects = cm.get_app_project_models(app)[0].objects.filter(owner_profile=profile, is_active=True)
            for ep in existing_projects:
                proj = dict()
                proj["name"] = ep.name
                proj["administer_project_link"] = "/apps/"+app.label+"/administer_project/"+str(ep.id)
                profile_app["existing_projects"].append(proj)
                
            profile_apps.append(profile_app)

    content = {'profile_apps': profile_apps, 'tags': tags}
    # add "core" if the user has core permission
    app = cm.get_core_app()
    perm = cm.get_provider_permission(app)
    if app.label+"."+perm.codename in permissions:
        content["core"] = True
    return render(request, 'core/profile.html', content)

def update_profile_tags(request):
    (profile, permissions, is_default_user) = get_profile_and_permissions(request)
    if is_default_user:
        return render(request, "core/please_login.html")
    if request.method == 'POST':
        form = AddTagForm(request.POST)
        if form.is_valid():
            match = get_best_final_matching_tag(form.cleaned_data["place_name"])
            if match is None: 
                return HttpResponse("Sorry, there isn't a tag with this name")
            profile.tags.add(match)
            tasks.feed_update_by_user_profile.delay(profile.id)
            return render(request, "core/thanks.html", {"action_description": "adding "+match.get_name()+" to your profile"})
        else:
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path})
    else:
        form = AddTagForm()
        return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path})
    
@ensure_csrf_cookie
@transaction.atomic
def app_view_relay(request, app_name, action_name, object_id):
    """
    The primary routing view for the major portal actions involving participation projects and items:
    creating projects, administering project, participating in items, and deleting projects

    This view checks permissions, then routes the request to app-specific views.
    """

    (profile, permissions, is_default_user) = get_profile_and_permissions(request)
    if not app_name in [app.label for app in cm.get_registered_participation_apps()]:
        raise Exception("no such app")
    else:
        app = [a for a in cm.get_registered_participation_apps() if a.name == app_name][0]
        perm = cm.get_provider_permission(app)
        has_app_perm = app.label+"."+perm.codename in permissions
        
        if action_name == "new_project":
            if has_app_perm:
                return app.views_module.new_project(request) 
            else:
                return render(request, 'core/no_permissions.html', {"title": "No Permission", "app_name": app_name, "action_description": "create a new project"})

        elif action_name == "administer_project":
            if has_app_perm:
                get_object_or_404(cm.ParticipationProject, pk=object_id, owner_profile=profile, is_active=True)
                return app.views_module.administer_project(request, object_id)
            else:
                return render(request, 'core/no_permissions.html', {"title": "No Permission", "app_name": app_name, "action_description": "administer a project"})

        elif action_name == "participate":
            get_object_or_404(cm.ParticipationItem, pk=object_id, is_active=True)
            cm.ParticipationItem.objects.filter(pk=object_id).distinct().update(visits=F('visits')+1)
            cm.FeedMatch.objects.filter(user_profile=profile, participation_item__pk=object_id).update(has_been_visited=True) 
            return app.views_module.participate(request, object_id) 

        elif action_name == "overview":
            return app.views_module.overview(request, object_id) 

        elif action_name == "delete_project":
            if has_app_perm:
                project = get_object_or_404(cm.ParticipationProject, pk=object_id, is_active=True, owner_profile=profile)
                if request.method == 'POST':
                    form = DeleteProjectConfirmationForm(request.POST)
                    if form.is_valid():
                        project.participationitem_set.update(is_active=False)
                        project.is_active = False
                        project.save()
                        return render(request, "core/thanks.html", {"action_description": "removing "+project.name})
                    else:
                        return HttpResponse(status=500)
                else:
                    form = DeleteProjectConfirmationForm()
                    items = cm.ParticipationItem.objects.filter(participation_project=project, is_active=True)
                    items = [get_item_details(i, True) for i in items]
                    return render(request, 'core/delete_project_confirmation.html', {'form': form, 'action_path' : request.path, "items": items, 'site': os.environ["SITE"]})
            else:
                return render(request, 'core/no_permissions.html', {"title": "No Permission", "app_name": app_name, "action_description": "delete a project"})

        elif action_name == "edit_project":
            if not app.are_projects_editable:
                return HttpResponse(status=500)
            if has_app_perm:
                project = get_object_or_404(cm.ParticipationProject, pk=object_id, is_active=True, owner_profile=profile)
                return app.views_module.edit_project(request, object_id) 
            else:
                return render(request, 'core/no_permissions.html', {"title": "No Permission", "app_name": app_name, "action_description": "delete a project"})

        elif action_name.startswith("customAction") and action_name.isalpha() and len(action_name) < 50 and action_name in app.views_module.__dict__:
            return app.views_module.__dict__[action_name](request, object_id) 
            
        else:
            raise Exception("invalid action:" + str(action_name))

def home(request):
    return render(request, "core/splash.html")

@ensure_csrf_cookie
def feed(request):
    (profile, permissions, is_default_user) = get_profile_and_permissions(request)
    num_tags_followed = profile.tags.count()
    recent_matches = cm.FeedMatch.objects.filter(user_profile=profile).order_by('-creation_time')[:100]
    items = [get_item_details(i) for i in map(lambda x: x.participation_item, recent_matches) if i.is_active]
    tasks.feed_update_by_user_profile.delay(profile.id)
    context = {'items': items, 'num_tags_followed': num_tags_followed, 'site': os.environ["SITE"]}
    context.update(get_default_og_metadata(request))
    return render(request, 'core/feed.html', context)


@ensure_csrf_cookie
def feed2(request):
    (profile, permissions, is_default_user) = get_profile_and_permissions(request)
    context = {'site': os.environ["SITE"]}
    context.update(get_default_og_metadata(request))
    return render(request, 'core/feed2.html', context)

def get_item_details(item, get_activity=False):
    """
    Return a dict describing the properties of some ParticipationItem,
    used to render the item with templates/core/feed_item.html
    """
    app = cm.get_app_for_model(item.get_inherited_instance().__class__)
    project_id = item.participation_project.pk
    project = item.participation_project.get_inherited_instance()
    ans = {"label": item.name, "display": item.get_inherited_instance().get_inline_display(), "link": "/apps/"+app.label+"/participate/"+str(item.pk), "tags": [t.name for t in item.tags.all()[:5]], "id":item.pk, "itemobj":item.get_inherited_instance(), "projectobj":project}
    if not item.display_image_file == "":
        ans["display_image_file"] = item.display_image_file
    if get_activity:
        ans["num_matches"] = cm.FeedMatch.objects.filter(participation_item=item).count()
        ans["num_visits"] = item.visits
    if app.custom_feed_item_template:
        ans["custom_template"] = app.custom_feed_item_template
    return ans

def tags(request):
    (profile, permissions, is_default_user) = get_profile_and_permissions(request)
    app = cm.get_core_app()
    perm = cm.get_provider_permission(app)
    if not app.label+"."+perm.codename in permissions:
        return HttpResponseForbidden()
    reports = []
    all_tags = cm.Tag.objects.all()
    reports.append({"label": "Tags", "num": all_tags.distinct().count(), "top10": all_tags[:10]})
    cities = cm.GeoTag.objects.filter(feature_type=cm.GeoTag.CITY)
    reports.append({"label": "Cities", "num": cities.distinct().count(), "top10": cities[:10]})
    states = cm.GeoTag.objects.filter(feature_type=cm.GeoTag.STATE_OR_PROVINCE)
    reports.append({"label": "States", "num": states.distinct().count(), "top10": states[:10]})
    countries = cm.GeoTag.objects.filter(feature_type=cm.GeoTag.COUNTRY)
    reports.append({"label": "Countries", "num": countries.distinct().count(), "top10": countries[:10]})
    other = cm.GeoTag.objects.filter(feature_type=cm.GeoTag.OTHER)
    reports.append({"label": "Other", "num": other.distinct().count(), "top10": other[:10]})
    unk = cm.GeoTag.objects.filter(feature_type=cm.GeoTag.UNKNOWN)
    reports.append({"label": "Unknown", "num": unk.distinct().count(), "top10": unk[:10]})

    return render(request, 'core/tags.html', {'reports': reports})

@transaction.atomic
def event_from_request(request):
    """
    create a cm.Event object from the request and return its ID
    """
    (profile, permissions, is_default_user) = get_profile_and_permissions(request)
    e = cm.Event()
    e.user_profile = profile
    e.path = request.path
    if "REMOTE_ADDR" in request.META:
        e.ip_addr = request.META["REMOTE_ADDR"]
    if "HTTP_REFERER" in request.META:
        e.referring_url = request.META["HTTP_REFERER"]
    e.save()
    return e.pk

def volunteer(request):
    return render(request, 'core/contact.html', {"message": "We are looking for volunteers to help with issue research, content creation, and software development. If you're interested, please contact us via email.", "email":os.environ["FROM_EMAIL"], "subject": "Volunteering at Better Democracy Network", "title":"Volunteer at Better Democracy Network"})

def donate(request):
    (profile, permissions, is_default_user) = get_profile_and_permissions(request)

    if request.method == 'POST':
        form = StripePaymentForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data["stripeToken"]
            amt = int(form.cleaned_data["donation_amount"])
            recurring = form.cleaned_data["recurring"] =="True"
            email = form.cleaned_data["email"]
            customer = stripe.Customer.create(source=token, email=email)

            donation = cm.Donation()
            donation.userprofile = profile
            donation.amount = amt / 100.0 # convert to dollars
            donation.stripe_customer_id = customer.id

            if not recurring:
                charge = stripe.Charge.create(amount=amt, currency="usd", description="Better Democracy Portal one-time donation", customer=customer.id)
                donation.stripe_full_response = charge

            else:
                plan_id = "sustaining_"+str(amt/100) # plan id from stripe
                resp = stripe.Subscription.create(customer=customer.id, plan=plan_id)
                donation.stripe_full_response = resp

            donation.save()
            return render(request, "core/thanks.html", {"action_description": "your generous contribution. Please check your email for a receipt"})

        else:
            return HttpResponse(status=500)
    else:
        return render(request, 'core/donate.html', {"stripe_publishable_api_key": os.environ["STRIPE_PUBLISHABLE_KEY"]})


    context = get_default_og_metadata(request)
    return render(request, 'core/coming_soon.html', context)

def nonpartisanship(request):
    (profile, permissions, is_default_user) = get_profile_and_permissions(request)
    context = get_default_og_metadata(request)
    return render(request, 'core/coming_soon.html', context)

@transaction.atomic
def report_issues(request, *args, **kwargs):
    if request.method == 'POST':
        form = IssueReportForm(request.POST)
        if form.is_valid():
            issue = cm.IssueReport()
            event = get_object_or_404(cm.Event, id=form.cleaned_data["event_id"])
            issue.event = event
            issue.title = form.cleaned_data["issue_title"]
            issue.description = form.cleaned_data["description"]
            issue.issue_type = form.cleaned_data["issue_type"]
            issue.save()
            return render(request, "core/thanks.html", {"action_description": "submitting this issue report"})
        else:
            if not "event_id" in form.cleaned_data:
                return HttpResponse(status=500)
            return render(request, 'core/generic_form.html', {'form': form, 'action_path' : request.path})
    else:
        event_id = event_from_request(request)
        form = IssueReportForm(initial={"event_id":event_id})
        return render(request, 'core/generic_form.html', {"title": "Report an Issue", 'form': form, 'action_path' : request.path})


def moderate_issues(request):
    (profile, permissions, is_default_user) = get_profile_and_permissions(request)
    app = cm.get_core_app()
    perm = cm.get_provider_permission(app)
    if not app.label+"."+perm.codename in permissions:
        return HttpResponseForbidden()
    recent_events = cm.Event.objects.order_by('-timestamp')[:100]
    recent_events = [(str(i.path), str(i.timestamp)) for i in recent_events]
    recent_issues = cm.IssueReport.objects.order_by('-event__timestamp')[:100]
    recent_issues = [(str(i.title), str(i.issue_type), str(i.event.path), str(i.event.timestamp)) for i in recent_issues]
    return render(request, 'core/moderate_issues.html', {"recent_issues": recent_issues, "recent_events": recent_events})

def portal_stats(request):
    (profile, permissions, is_default_user) = get_profile_and_permissions(request)
    app = cm.get_core_app()
    perm = cm.get_provider_permission(app)
    if not app.label+"."+perm.codename in permissions:
        return HttpResponseForbidden()
    num_users = cm.UserProfile.objects.count()
    num_projects = cm.ParticipationProject.objects.filter(is_active=True).count()
    num_items = cm.ParticipationItem.objects.filter(is_active=True).count()
    num_tags = cm.Tag.objects.count()
    num_visits = cm.ParticipationItem.objects.aggregate(Sum('visits'))["visits__sum"]

    return render(request, 'core/portal_stats.html', {"num_users": num_users, "num_projects": num_projects, "num_items": num_items, "num_tags": num_tags, "num_visits": num_visits})


def item_info(request, item_id):
    if not request.is_ajax() or not request.method == "POST":
        return HttpResponse(status=500)
    item = get_object_or_404(cm.ParticipationItem, pk=item_id)
    app = cm.get_app_for_model(item.get_inherited_instance().__class__)
    external_link = getattr(app, "external_link")
    ans = {"img_url": settings.STATIC_URL+item.display_image_file, "link": item.participate_link(), "title": item.name, "external_link": external_link}
    return JsonResponse(ans)

def feed_recommendations(request):
    """
    recommend items as a user arrives to go at the top of their feed 
    """
    (profile, permissions, is_default_user) = get_profile_and_permissions(request)
    if not request.is_ajax() or not request.method == "POST":
        return HttpResponse(status=500)

    #### extract content from current_feed_contents
    sys.stderr.write("Request body: {}\n".format(request.body.strip()))
    sys.stderr.flush()
    submission_data = json.loads(request.body.strip())
    current_feed_contents = set(submission_data.get("current_feed_contents", []))
    # feed size maxes out at 100
    if len(current_feed_contents) >= 100:
        return JsonResponse({"recommendations":[]})

    ### recommend diverse content to the user which doesn't overlap with current feed contents
    recommendations = set()
    subjects_of_interest = set()
    places_of_interest = set()
    for t in profile.tags.all():
        try:
            geo = t.geotag
            places_of_interest.add(t)
        except:
            subjects_of_interest.add(t)

    for t in places_of_interest:
        for app in cm.get_registered_participation_apps():
            for item_model in cm.get_app_item_models(app):
                recommendations.update([x.participationitem_ptr.pk for x in item_model.objects.filter(is_active=True, tags__in=[t]).order_by('-creation_time')[:3]])

    # TODO: make use of subjects of interest
    recommendations = recommendations - current_feed_contents
    recommendations = random.sample(recommendations, min(10, len(recommendations)))
    content = {"recommendations": recommendations}
    return JsonResponse(content)



def recommend_related(request, item_id):
    """
    recommend related items to put at the bottom of a participation page
    """
    if not request.is_ajax() or not request.method == "POST":
        return HttpResponse(status=500)
    item = get_object_or_404(cm.ParticipationItem, pk=item_id)
    candidates = []
    recommendations = []
    for t in item.tags.all():
        recent_items = t.participationitem_set.filter(is_active=True).order_by('-creation_time')[:100]
        candidates.extend([i for i in recent_items if not i.pk == item.pk])

    if len(candidates) < 3:
        t = cm.get_usa()
        recent_items = t.participationitem_set.filter(is_active=True).order_by('-creation_time')[:100]
        candidates.extend([i for i in recent_items if not i.pk == item.pk])

    recommendations = random.sample(candidates, min(10, len(candidates)))
    content = {"recommendations": [r.id for r in recommendations]}
    return JsonResponse(content)

def js_templates(request, item_name):
    if item_name == "feed_item_nunjucks.html":
        return FileResponse(open("core/templates/core/feed_item_nunjucks.html"))
    else:
        sys.stderr.write("Unknown template requested: {}\n".format(item_name))
        sys.stderr.flush()
        return HttpResponse("")
