from __future__ import unicode_literals
from django.contrib.gis.db import models
from django.db import transaction
from django.db.models.signals import post_save, m2m_changed
from django.contrib.auth.models import User, Permission
from django.contrib.sessions.models import Session
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.apps import apps
import sys, random, string
from django.core.exceptions import ValidationError
from django.db.models import Transform

### Start functions for accessing particpation app API
def get_core_app():
    all_apps = apps.get_app_configs()
    return [a for a in all_apps if a.name=="core" and len(get_app_project_models(a))==1][0]

def get_registered_participation_apps():
    all_apps = apps.get_app_configs()
    participation_apps = [a for a in all_apps if not a.name=="core" and len(get_app_project_models(a))==1]
    return participation_apps

def get_app_project_models(app):
    return [m for m in app.get_models() if issubclass(m, ParticipationProject)]

def get_app_item_models(app):
    return [m for m in app.get_models() if issubclass(m, ParticipationItem)]

def get_app_by_name(name):
    all_apps = apps.get_app_configs()
    participation_apps = [a for a in all_apps if a.name==name and len(get_app_project_models(a))==1]
    return participation_apps[0]

def get_app_for_model(model):
    apps = get_registered_participation_apps()
    for a in apps:
        if model in a.get_models():
            return a
    
def get_item_subclass_test(app):
    item_models = get_app_item_models(app)
    if len(item_models) == 0:
        raise Exception("app"+app.name+" has no Participation Item models")
    m = item_models[0]
    subclass_name = m.__name__.lower().replace("_","")
    return lambda x: getattr(x, subclass_name)

def get_project_subclass_test(app):
    project_models = get_app_project_models(app)
    if len(project_models) == 0:
        raise Exception("app"+app.name+" has no Participation Project models")
    m = project_models[0]
    subclass_name = m.__name__.lower().replace("_","")
    return lambda x: getattr(x, subclass_name)


def get_provider_permission(app):
    project_model = get_app_project_models(app)[0]
    model_name = project_model.__name__.lower().replace("_","")
    app_name = app.name.lower()
    content_type = ContentType.objects.get(app_label=app_name, model=model_name)
    perm = Permission.objects.get(content_type=content_type, codename__startswith="add_")
    return perm

def get_default_user():
    return User.objects.get_or_create(
        username = "default", 
        defaults = {"email":"default@default.default", 
                    "password": ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(20)), 
                    "last_login": "2016-12-15T15:53:48.874Z", 
                    "is_superuser": False, 
                    "first_name": "", 
                    "last_name": "", 
                    "is_staff": False, 
                    "is_active": True, 
                    "date_joined": "2016-11-09T22:26:10.731Z", 
                })[0]

def get_usa():
    return GeoTag.objects.get_or_create(name="United States of America", defaults={"detail": "North America", "feature_type": "CO"})[0]

### Start core models
class ParticipationProject(models.Model):
    name = models.CharField(max_length = 500)
    owner_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def update_items(self):
        raise Exception("Please overwrite the update_items() method for your participation app")

    def get_inherited_instance(self):
        ans = self
        for t in [get_project_subclass_test(app) for app in get_registered_participation_apps()]:
            try:
                ans = t(self)
            except:
                continue
            else:
                return ans
        raise Exception("unknown subclass type")

    def delete_project_link(self):
        app = get_app_for_model(self.get_inherited_instance().__class__)
        return "/apps/"+app.label+"/delete_project/"+str(self.id)

    def edit_project_link(self):
        app = get_app_for_model(self.get_inherited_instance().__class__)
        if app.are_projects_editable:
            return "/apps/"+app.label+"/edit_project/"+str(self.id)

class ParticipationItem(models.Model):
    name = models.CharField(max_length = 500)
    creation_time = models.DateTimeField(auto_now_add=True)
    participation_project = models.ForeignKey('ParticipationProject', on_delete=models.CASCADE)
    display_image_file = models.FilePathField(max_length=500, blank=True)
    visits = models.IntegerField(default=0)
    tags = models.ManyToManyField('Tag')
    is_active = models.BooleanField(default=True)

    def get_inherited_instance(self):
        ans = self
        for t in [get_item_subclass_test(app) for app in get_registered_participation_apps()]:
            try:
                ans = t(self)
            except:
                continue
            else:
                return ans
        raise Exception("unknown subclass type")

    def set_relavent_tags(self):
        raise Exception("set_relevant_tags() method needs to be implemented by all ParticipationItem subclasses.")

    def get_inline_display(self):
        return self.name + " participation item"

    def set_display_image(self):
        """
        Overwrite this function with app-specific method 
        for setting an item's display image.
        It can take a long time, since it will be run by workers, not by web server
        """
        return None

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    tags = models.ManyToManyField('Tag')

class Donation(models.Model):
    userprofile = models.ForeignKey(UserProfile, blank=True, null=True, on_delete = models.SET_NULL)
    amount = models.FloatField()
    is_recurring = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    stripe_customer_id = models.CharField(max_length=100)
    stripe_full_response = models.TextField() # json object returned by stripe    

class FeedMatch(models.Model):
    participation_item = models.ForeignKey('ParticipationItem', on_delete = models.CASCADE)
    user_profile = models.ForeignKey('UserProfile', on_delete = models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    has_been_visited = models.BooleanField(default=False)

class Tag(models.Model):
    name = models.CharField(max_length = 300)
    # ex: county + state + country name if the tag is a city
    detail = models.CharField(max_length = 300, blank=True, null=True)

    class Meta:
        unique_together = (("name", "detail"),)

    def get_name(self):
        if not self.detail is None:
            return self.name + ", " + self.detail
        return self.name

class GeoTag(Tag):
    polygon = models.PolygonField(geography = True, blank=True, null=True)
    polygon_area = models.FloatField(blank = True, null=True)
    point = models.PointField(geography = True, blank=True, null=True)
    population = models.PositiveIntegerField(blank=True, null=True)

    COUNTRY="CO"
    STATE_OR_PROVINCE="SP"
    CITY="CI"
    OTHER="OT"
    UNKNOWN="UN"

    FEATURE_TYPE_CHOICES = ((COUNTRY, "Country"),(STATE_OR_PROVINCE, "State or Province"),(CITY, "City or town"),(OTHER, "Other"),(UNKNOWN, "Unknown"))

    feature_type = models.CharField(max_length=2, choices=FEATURE_TYPE_CHOICES, default=UNKNOWN)

class Event(models.Model):
    """
    Event model used to record the context for various events such as key performance indicators
    (issue reports, donate button clicks)
    """
    user_profile = models.ForeignKey(UserProfile)
    ip_addr = models.CharField(max_length = 100, blank=True, null=True)
    referring_url = models.CharField(max_length = 500, blank=True, null=True)
    path = models.CharField(max_length=500, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class IssueReport(models.Model):
    event = models.ForeignKey(Event)
    title = models.CharField(max_length = 100)
    description = models.TextField()
    issue_type = models.CharField(max_length=2, choices=(("PC", "Propaganda, campaigning, or biased content"), ("BR", "Bug or website error"), ("IA", "Inaccurate content"), ("FR", "Request a feature"), ))

def validate_shortcut_string(s):
    if "/" in s or "." in s:
        raise ValidationError("shortcut cannot contain slashes or periods")
    if not all([char.isalpha() or char.isdigit() or char in ["_", "-"] for char in s]):
        raise ValidationError("shortcuts must be letters, numbers, underscores or dashes")
    if not s.lower() == s:
        raise ValidationError("shortcut must be all lowercase")

class Shortcut(models.Model):
    shortcut_string = models.CharField(max_length=500, unique=True, validators=[validate_shortcut_string])
    target_item = models.ForeignKey(ParticipationItem)

### Signal handling

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        new_profile = UserProfile()
        new_profile.user = instance
        new_profile.save()
        new_profile.tags.add(get_usa())

post_save.connect(create_user_profile, sender=User)

def process_new_item(sender, instance, created, **kwargs):
    if created:
        # process display image
        instance.set_display_image()
        instance.save()
        # tag the item
        instance.set_relevant_tags()

def register_participation_item_subclass(cls):
    post_save.connect(process_new_item, sender=cls)


### Custom sql

class AbsoluteValue(Transform):
    lookup_name = 'abs'
    function = 'ABS'

models.FloatField.register_lookup(AbsoluteValue)
