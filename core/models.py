from __future__ import unicode_literals
from django.contrib.gis.db import models
from django.db import transaction
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
import sys

### Start functions for accessing particpation app API
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
    participation_apps = [a for a in all_apps if not a.name=="core" and a.name==name and len(get_app_project_models(a))==1]
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

def get_provider_permission(app):
    project_model = get_app_project_models(app)[0]
    model_name = project_model.__name__.lower().replace("_","")
    app_name = app.name.lower()
    content_type = ContentType.objects.get(app_label=app_name, model=model_name)
    perm = Permission.objects.get(content_type=content_type, codename__startswith="add_")
    return perm

### Start core models
class ParticipationProject(models.Model):
    name = models.CharField(max_length = 100)
    owner_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)

    def update_items(self):
        raise Exception("Please overwrite the update_items() method for your participation app")


class ParticipationItem(models.Model):
    name = models.CharField(max_length = 100)
    participation_project = models.ForeignKey('ParticipationProject', on_delete=models.CASCADE)
    display_image_url = models.URLField(blank=True)
    visits = models.IntegerField(default=0)

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

    def get_description(self):
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
    
class FeedMatch(models.Model):
    participation_item = models.ForeignKey('ParticipationItem', on_delete = models.CASCADE)
    user_profile = models.ForeignKey('UserProfile', on_delete = models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    has_been_visited = models.BooleanField(default=False)

class Tag(models.Model):
    tag_name = models.CharField(max_length = 300)

class GeoTag(Tag):
    polygon = models.PolygonField(geography = True)


### Signal handling

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


def set_image(sender, instance, created, **kwargs):
    if created:
        instance.set_display_image()
        instance.save()
    sys.stderr.flush()

def register_participation_item_subclass(cls):
    post_save.connect(set_image, sender=cls)
